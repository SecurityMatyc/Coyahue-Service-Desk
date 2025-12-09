from django.contrib import admin
from .models import ArticuloFAQ, VotoFAQ, ArchivoFAQ


@admin.register(ArticuloFAQ)
class ArticuloFAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'categoria', 'publicado', 'destacado', 'vistas', 'porcentaje_utilidad', 'fecha_actualizacion']
    list_filter = ['publicado', 'destacado', 'categoria', 'fecha_creacion']
    search_fields = ['titulo', 'problema', 'solucion', 'tags']
    readonly_fields = ['vistas', 'util_si', 'util_no', 'fecha_creacion', 'fecha_actualizacion']
    list_editable = ['publicado', 'destacado']
    
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'problema', 'solucion')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'tags')
        }),
        ('Estado', {
            'fields': ('publicado', 'destacado', 'creado_por')
        }),
        ('Métricas', {
            'fields': ('vistas', 'util_si', 'util_no', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VotoFAQ)
class VotoFAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'articulo', 'voto', 'fecha_voto']
    list_filter = ['voto', 'fecha_voto']
    search_fields = ['usuario__email', 'articulo__titulo']
    readonly_fields = ['usuario', 'articulo', 'voto', 'fecha_voto']
    
    def has_add_permission(self, request):
        return False  # No se crean votos manualmente desde admin


@admin.register(ArchivoFAQ)
class ArchivoFAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'articulo', 'descripcion', 'orden', 'subido_por', 'fecha_subida']
    list_filter = ['fecha_subida']
    search_fields = ['articulo__titulo', 'descripcion']
    readonly_fields = ['fecha_subida']
    list_editable = ['orden']
    
    fieldsets = (
        ('Archivo', {
            'fields': ('articulo', 'archivo', 'descripcion', 'orden')
        }),
        ('Metadatos', {
            'fields': ('subido_por', 'fecha_subida'),
            'classes': ('collapse',)
        }),
    )

