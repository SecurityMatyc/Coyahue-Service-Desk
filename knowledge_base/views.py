from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Q
from django.contrib import messages

from .models import ArticuloFAQ, VotoFAQ, ArchivoFAQ
from tickets.models import Categoria


# -------------------------------------------------------------------
# VISTAS PARA USUARIOS (Ver FAQ)
# -------------------------------------------------------------------

@login_required
def faq_listar(request):
    """Lista de artículos FAQ para usuarios (solo lectura)"""
    # Buscar
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria')
    
    # Base queryset (solo publicados)
    articulos = ArticuloFAQ.objects.filter(publicado=True).select_related('categoria', 'creado_por')
    
    # Filtrar por búsqueda
    if query:
        articulos = articulos.filter(
            Q(titulo__icontains=query) |
            Q(problema__icontains=query) |
            Q(solucion__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Filtrar por categoría
    if categoria_id:
        articulos = articulos.filter(categoria_id=categoria_id)
    
    # Artículos destacados
    destacados = ArticuloFAQ.objects.filter(publicado=True, destacado=True)[:5]
    
    # Categorías para filtro
    categorias = Categoria.objects.filter(activo=True)
    
    return render(request, 'knowledge_base/faq_listar.html', {
        'articulos': articulos,
        'destacados': destacados,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id,
    })


@login_required
def faq_detalle(request, articulo_id):
    """Detalle de un artículo FAQ"""
    articulo = get_object_or_404(
        ArticuloFAQ.objects.select_related('categoria', 'creado_por'),
        id=articulo_id,
        publicado=True
    )
    
    # Incrementar vistas
    articulo.vistas += 1
    articulo.save(update_fields=['vistas'])
    
    # Verificar si el usuario ya votó
    voto_existente = VotoFAQ.objects.filter(
        usuario=request.user,
        articulo=articulo
    ).first()
    
    return render(request, 'knowledge_base/faq_detalle.html', {
        'articulo': articulo,
        'voto_existente': voto_existente,
    })


@login_required
def faq_votar(request, articulo_id):
    """Votar si un artículo fue útil o no (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    articulo = get_object_or_404(ArticuloFAQ, id=articulo_id, publicado=True)
    voto = request.POST.get('voto')  # 'si' o 'no'
    
    if voto not in ['si', 'no']:
        return JsonResponse({'error': 'Voto inválido'}, status=400)
    
    # Verificar si ya votó
    voto_existente = VotoFAQ.objects.filter(
        usuario=request.user,
        articulo=articulo
    ).first()
    
    if voto_existente:
        return JsonResponse({
            'error': 'Ya has votado en este artículo',
            'ya_voto': True,
            'voto_anterior': voto_existente.voto
        }, status=400)
    
    # Registrar voto
    VotoFAQ.objects.create(
        usuario=request.user,
        articulo=articulo,
        voto=voto
    )
    
    # Actualizar contador
    if voto == 'si':
        articulo.util_si += 1
        articulo.save(update_fields=['util_si'])
        mensaje = '¡Gracias! Nos alegra que te haya sido útil.'
    else:
        articulo.util_no += 1
        articulo.save(update_fields=['util_no'])
        mensaje = 'Gracias por tu feedback. Trabajaremos en mejorar este artículo.'
    
    return JsonResponse({
        'success': True,
        'mensaje': mensaje,
        'util_si': articulo.util_si,
        'util_no': articulo.util_no,
    })


# -------------------------------------------------------------------
# VISTAS PARA ADMIN/TÉCNICO (Gestión FAQ)
# -------------------------------------------------------------------

def require_role(user, rol_nombre: str) -> bool:
    """Helper para verificar rol"""
    return (
        user.is_authenticated
        and hasattr(user, "rol")
        and user.rol
        and user.rol.nombre_rol.upper() == rol_nombre.upper()
    )


@login_required
def faq_admin_listar(request):
    """Lista de artículos FAQ para admin/técnico con opciones de gestión"""
    if not (require_role(request.user, "ADMIN") or require_role(request.user, "TECNICO")):
        return HttpResponseForbidden("No tienes permiso para gestionar artículos FAQ.")
    
    articulos = ArticuloFAQ.objects.select_related('categoria', 'creado_por').order_by('-fecha_actualizacion')
    
    return render(request, 'knowledge_base/faq_admin_listar.html', {
        'articulos': articulos,
    })


@login_required
def faq_admin_crear(request):
    """Crear nuevo artículo FAQ"""
    if not (require_role(request.user, "ADMIN") or require_role(request.user, "TECNICO")):
        return HttpResponseForbidden("No tienes permiso para crear artículos FAQ.")
    
    categorias = Categoria.objects.filter(activo=True)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        problema = request.POST.get('problema', '').strip()
        solucion = request.POST.get('solucion', '').strip()
        categoria_id = request.POST.get('categoria')
        tags = request.POST.get('tags', '').strip()
        publicado = request.POST.get('publicado') == 'on'
        destacado = request.POST.get('destacado') == 'on'
        
        if not titulo or not problema or not solucion:
            messages.error(request, "Título, problema y solución son obligatorios.")
            return render(request, 'knowledge_base/faq_admin_crear.html', {'categorias': categorias})
        
        articulo = ArticuloFAQ.objects.create(
            titulo=titulo,
            problema=problema,
            solucion=solucion,
            categoria_id=categoria_id if categoria_id else None,
            tags=tags,
            publicado=publicado,
            destacado=destacado,
            creado_por=request.user,
        )
        
        # Procesar archivos adjuntos
        archivos = request.FILES.getlist('archivos')
        descripciones = request.POST.getlist('descripciones')
        
        for i, archivo in enumerate(archivos):
            descripcion = descripciones[i] if i < len(descripciones) else f"Archivo {i+1}"
            ArchivoFAQ.objects.create(
                articulo=articulo,
                archivo=archivo,
                descripcion=descripcion.strip(),
                orden=i,
                subido_por=request.user
            )
        
        messages.success(request, "Artículo FAQ creado correctamente.")
        return redirect('faq_admin_listar')
    
    return render(request, 'knowledge_base/faq_admin_crear.html', {
        'categorias': categorias,
    })


@login_required
def faq_admin_editar(request, articulo_id):
    """Editar artículo FAQ existente"""
    if not (require_role(request.user, "ADMIN") or require_role(request.user, "TECNICO")):
        return HttpResponseForbidden("No tienes permiso para editar artículos FAQ.")
    
    articulo = get_object_or_404(ArticuloFAQ, id=articulo_id)
    categorias = Categoria.objects.filter(activo=True)
    archivos_existentes = articulo.archivos.all()
    
    if request.method == 'POST':
        articulo.titulo = request.POST.get('titulo', '').strip()
        articulo.problema = request.POST.get('problema', '').strip()
        articulo.solucion = request.POST.get('solucion', '').strip()
        categoria_id = request.POST.get('categoria')
        articulo.categoria_id = categoria_id if categoria_id else None
        articulo.tags = request.POST.get('tags', '').strip()
        articulo.publicado = request.POST.get('publicado') == 'on'
        articulo.destacado = request.POST.get('destacado') == 'on'
        
        articulo.save()
        
        # Procesar nuevos archivos adjuntos
        archivos = request.FILES.getlist('archivos')
        descripciones = request.POST.getlist('descripciones')
        
        # Obtener el orden máximo actual
        max_orden = articulo.archivos.count()
        
        for i, archivo in enumerate(archivos):
            descripcion = descripciones[i] if i < len(descripciones) else f"Archivo {i+1}"
            ArchivoFAQ.objects.create(
                articulo=articulo,
                archivo=archivo,
                descripcion=descripcion.strip(),
                orden=max_orden + i,
                subido_por=request.user
            )
        
        messages.success(request, "Artículo FAQ actualizado correctamente.")
        return redirect('faq_admin_listar')
    
    return render(request, 'knowledge_base/faq_admin_editar.html', {
        'articulo': articulo,
        'categorias': categorias,
        'archivos_existentes': archivos_existentes,
    })


@login_required
def faq_admin_eliminar(request, articulo_id):
    """Eliminar artículo FAQ"""
    if not (require_role(request.user, "ADMIN") or require_role(request.user, "TECNICO")):
        return HttpResponseForbidden("No tienes permiso para eliminar artículos FAQ.")
    
    articulo = get_object_or_404(ArticuloFAQ, id=articulo_id)
    
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, "Artículo FAQ eliminado correctamente.")
        return redirect('faq_admin_listar')
    
    return render(request, 'knowledge_base/faq_admin_eliminar.html', {
        'articulo': articulo,
    })


@login_required
def faq_admin_eliminar_archivo(request, archivo_id):
    """Eliminar archivo adjunto de un artículo FAQ"""
    if not (require_role(request.user, "ADMIN") or require_role(request.user, "TECNICO")):
        return HttpResponseForbidden("No tienes permiso para eliminar archivos.")
    
    archivo = get_object_or_404(ArchivoFAQ, id=archivo_id)
    articulo_id = archivo.articulo.id
    
    # Eliminar el archivo del sistema de archivos
    if archivo.archivo:
        archivo.archivo.delete(save=False)
    
    archivo.delete()
    messages.success(request, "Archivo eliminado correctamente.")
    
    return redirect('faq_admin_editar', articulo_id=articulo_id)

