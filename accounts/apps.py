# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"     # ruta del módulo
    # NO le pongas otro label distinto ni dupliques esta clase
    # porque puede causar conflictos en Django