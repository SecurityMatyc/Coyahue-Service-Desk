from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import (
    login_view,
    dashboard_admin,
    dashboard_tecnico,
    dashboard_usuario,

    usuarios_listar,
    usuarios_crear,
    usuarios_editar,
    usuarios_eliminar,

    roles_listar,
    categorias_listar,
    subcategorias_listar,
    prioridades_listar,
    estados_listar,

    tickets_listar,
    tickets_detalle,
    tickets_eliminar,
    tickets_tecnico_listar,
    tickets_usuario_listar,
    ticket_usuario_crear,
    ticket_usuario_detalle,
    ticket_tecnico_detalle,

    reportes_dashboard,

    notificaciones_listar,
    notificacion_marcar_leida,
    reportes_tickets_excel,
    reportes_tickets_pdf,

    editar_perfil,
    recuperar_contrasena,
)

from notifications.views import (
    marcar_todas_leidas,
    eliminar_todas_notificaciones,
)

from tickets.views import TicketViewSet

from knowledge_base.views import (
    faq_listar,
    faq_detalle,
    faq_votar,
    faq_admin_listar,
    faq_admin_crear,
    faq_admin_editar,
    faq_admin_eliminar,
    faq_admin_eliminar_archivo,
)

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")


urlpatterns = [
    # raíz → login
    path("", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("recuperar-contrasena/", recuperar_contrasena, name="recuperar_contrasena"),

    # Django admin clásico
    path("admin/", admin.site.urls),

    # PANEL HTML DE COYAHUE
    path("panel/admin/", dashboard_admin, name="dashboard_admin"),
    path("panel/tecnico/", dashboard_tecnico, name="dashboard_tecnico"),
    path("panel/usuario/", dashboard_usuario, name="dashboard_usuario"),

    # Usuarios (CRUD admin)
    path("panel/usuarios/", usuarios_listar, name="usuarios_listar"),
    path("panel/usuarios/crear/", usuarios_crear, name="usuarios_crear"),
    path("panel/usuarios/<int:usuario_id>/editar/", usuarios_editar, name="usuarios_editar"),
    path("panel/usuarios/<int:usuario_id>/eliminar/", usuarios_eliminar, name="usuarios_eliminar"),

    # Catálogos (solo lectura)
    path("panel/roles/", roles_listar, name="roles_listar"),
    path("panel/categorias/", categorias_listar, name="categorias_listar"),
    path("panel/subcategorias/", subcategorias_listar, name="subcategorias_listar"),
    path("panel/prioridades/", prioridades_listar, name="prioridades_listar"),
    path("panel/estados/", estados_listar, name="estados_listar"),

    # Tickets admin
    path("panel/tickets/", tickets_listar, name="tickets_listar"),
    path("panel/tickets/<int:ticket_id>/", tickets_detalle, name="tickets_detalle"),
    path("panel/tickets/<int:ticket_id>/eliminar/", tickets_eliminar, name="tickets_eliminar"),

    # Tickets técnico
    path("panel/tecnico/tickets/", tickets_tecnico_listar, name="tickets_tecnico_listar"),
    # Tickets técnico
    path("panel/tecnico/tickets/", tickets_tecnico_listar, name="tickets_tecnico_listar"),
    path("panel/tecnico/tickets/<int:ticket_id>/", ticket_tecnico_detalle, name="ticket_tecnico_detalle"),

    # (si necesitas detalle técnico, se puede agregar luego)

    # Tickets del usuario solicitante
    path("panel/usuario/tickets/", tickets_usuario_listar, name="tickets_usuario_listar"),
    path("panel/usuario/tickets/crear/", ticket_usuario_crear, name="ticket_usuario_crear"),
    path("panel/usuario/tickets/<int:ticket_id>/", ticket_usuario_detalle, name="ticket_usuario_detalle"),

    # Notificaciones
    path("panel/notificaciones/", notificaciones_listar, name="notificaciones_listar"),
    path("panel/notificaciones/<int:notif_id>/leer/", notificacion_marcar_leida, name="notificacion_marcar_leida"),
    path("panel/notificaciones/marcar-todas-leidas/", marcar_todas_leidas, name="marcar_todas_leidas"),
    path("panel/notificaciones/eliminar-todas/", eliminar_todas_notificaciones, name="eliminar_todas_notificaciones"),

    # Editar perfil (todos los roles)
    path("panel/perfil/editar/", editar_perfil, name="editar_perfil"),

    # Reportes
    path("panel/reportes/", reportes_dashboard, name="reportes_dashboard"),
    path("panel/reportes/tickets/excel/", reportes_tickets_excel, name="reportes_tickets_excel"),
    path("panel/reportes/tickets/pdf/", reportes_tickets_pdf, name="reportes_tickets_pdf"),

    # Knowledge Base / FAQ - Usuario
    path("panel/faq/", faq_listar, name="faq_listar"),
    path("panel/faq/<int:articulo_id>/", faq_detalle, name="faq_detalle"),
    path("panel/faq/<int:articulo_id>/votar/", faq_votar, name="faq_votar"),

    # Knowledge Base / FAQ - Admin/Técnico
    path("panel/admin/faq/", faq_admin_listar, name="faq_admin_listar"),
    path("panel/admin/faq/crear/", faq_admin_crear, name="faq_admin_crear"),
    path("panel/admin/faq/<int:articulo_id>/editar/", faq_admin_editar, name="faq_admin_editar"),
    path("panel/admin/faq/<int:articulo_id>/eliminar/", faq_admin_eliminar, name="faq_admin_eliminar"),
    path("panel/admin/faq/archivo/<int:archivo_id>/eliminar/", faq_admin_eliminar_archivo, name="faq_admin_eliminar_archivo"),

    # API auth JWT
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API REST
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
