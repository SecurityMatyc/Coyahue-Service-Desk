from django.db import models
from django.conf import settings
from tickets.models import Categoria

Usuario = settings.AUTH_USER_MODEL


class ArticuloFAQ(models.Model):
    """
    Artículo de preguntas frecuentes / base de conocimiento.
    """
    # Contenido
    titulo = models.CharField(max_length=255, help_text="Pregunta o título del artículo")
    problema = models.TextField(help_text="Descripción detallada del problema")
    solucion = models.TextField(help_text="Solución paso a paso")
    
    # Organización
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articulos_faq",
        help_text="Categoría del artículo (mismas que tickets)"
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Palabras clave separadas por comas (ej: password, acceso, vpn)"
    )
    
    # Gestión
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articulos_creados"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True, help_text="Si está visible para usuarios")
    destacado = models.BooleanField(default=False, help_text="Aparece en artículos destacados")
    
    # Métricas
    vistas = models.IntegerField(default=0, help_text="Número de veces que se ha visto")
    util_si = models.IntegerField(default=0, help_text="Votos positivos '¿Fue útil? Sí'")
    util_no = models.IntegerField(default=0, help_text="Votos negativos '¿Fue útil? No'")
    
    class Meta:
        verbose_name = "Artículo FAQ"
        verbose_name_plural = "Artículos FAQ"
        ordering = ["-destacado", "-fecha_actualizacion"]
    
    def __str__(self):
        return self.titulo
    
    @property
    def porcentaje_utilidad(self):
        """Calcula porcentaje de utilidad (votos positivos / total)"""
        total = self.util_si + self.util_no
        if total == 0:
            return None
        return round((self.util_si / total) * 100, 1)
    
    @property
    def total_votos(self):
        """Total de votos recibidos"""
        return self.util_si + self.util_no


class VotoFAQ(models.Model):
    """
    Registro de votos de usuarios en artículos FAQ.
    Evita que un usuario vote más de una vez.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="votos_faq"
    )
    articulo = models.ForeignKey(
        ArticuloFAQ,
        on_delete=models.CASCADE,
        related_name="votos"
    )
    voto = models.CharField(
        max_length=2,
        choices=[('si', 'Útil'), ('no', 'No útil')]
    )
    fecha_voto = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Voto FAQ"
        verbose_name_plural = "Votos FAQ"
        unique_together = ('usuario', 'articulo')  # 1 voto por usuario por artículo
        ordering = ['-fecha_voto']
    
    def __str__(self):
        return f"{self.usuario.email} votó '{self.voto}' en {self.articulo.titulo}"


class ArchivoFAQ(models.Model):
    """
    Archivos adjuntos (imágenes, PDFs) para artículos FAQ.
    Permite adjuntar múltiples archivos con descripciones para guiar paso a paso.
    """
    articulo = models.ForeignKey(
        ArticuloFAQ,
        on_delete=models.CASCADE,
        related_name="archivos"
    )
    archivo = models.FileField(
        upload_to='faq_archivos/%Y/%m/',
        help_text="Imagen o PDF para ilustrar el artículo"
    )
    descripcion = models.CharField(
        max_length=200,
        help_text="Descripción del paso (ej: 'Paso 1: Click en configuración')"
    )
    orden = models.PositiveIntegerField(
        default=0,
        help_text="Orden de visualización"
    )
    subido_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name="archivos_faq_subidos"
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Archivo FAQ"
        verbose_name_plural = "Archivos FAQ"
        ordering = ['orden', 'fecha_subida']
    
    def __str__(self):
        return f"{self.descripcion} - {self.articulo.titulo}"
    
    def extension(self):
        """Devuelve la extensión del archivo"""
        import os
        return os.path.splitext(self.archivo.name)[1].lower()
    
    def es_imagen(self):
        """Verifica si el archivo es una imagen"""
        extensiones_imagen = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.extension() in extensiones_imagen
    
    def es_pdf(self):
        """Verifica si el archivo es un PDF"""
        return self.extension() == '.pdf'

