# Coyahue Service Desk 📚

Proyecto académico desarrollado durante 2025 para la **Evaluación 4 de Proyecto Integrado**. Este sistema representa una mesa de ayuda TI orientada a la gestión de tickets, usuarios y soporte técnico, con enfoque en una experiencia web funcional para usuario, técnico y administrador.

## 👥 Autores

- Matías Gajardo
- Jean Pierre Avastia
- Andrés Chandía

Trabajo realizado en conjunto como parte del proceso formativo en desarrollo de software.

## 🧩 Descripción del proyecto

La aplicación fue desarrollada por etapas durante el segundo semestre del segundo año de la carrera, en el marco de la asignatura Proyecto Integrado. Se trabajó en 4 unidades, con planificación progresiva, construcción funcional y presentación final.

El proyecto se implementó para una empresa real llamada Coyahue de la zona de **Temuco, Chile**, y fue presentado formalmente como solución tecnológica para la gestión de soporte interno.

La plataforma permite administrar los procesos principales de una mesa de ayuda TI:

- Registro y gestión de usuarios con roles.
- Creación y seguimiento de tickets de soporte.
- Gestión de estados, prioridades y categorías.
- Asignación de tickets a técnicos.
- Historial de comentarios y trazabilidad de atención.
- Paneles diferenciados para usuario, técnico y administrador.
- Base de conocimiento (FAQ) para autoayuda de usuarios.

Además de la parte de gestión, el proyecto incorpora una interfaz web responsive con vistas funcionales como:

- Inicio de sesión.
- Recuperación de contraseña.
- Dashboard por perfil.
- Listado y detalle de tickets.
- Administración de usuarios, categorías, subcategorías, estados y prioridades.

## ✨ Características principales

- Flujo de tickets enfocado en soporte TI empresarial.
- Control de permisos por tipo de usuario.
- Gestión administrativa completa de entidades del sistema.
- Módulo de notificaciones para eventos relevantes.
- Reportes con vistas de seguimiento.
- Integración de API con Django REST Framework y JWT.

## 🛠️ Stack tecnológico

- Python 3.13
- Django 5.2.8
- Django REST Framework
- Simple JWT
- HTML, CSS, JavaScript
- Plantillas Django
- SQLite (base de datos por defecto del repositorio)
- PostgreSQL (base de datos usada en el proyecto original)
- AWS (despliegue realizado durante la etapa académica)

## 🗂️ Módulos del sistema

- `accounts`: autenticación, registro, perfiles y control de roles.
- `tickets`: lógica principal de tickets, estados y seguimiento.
- `notifications`: notificaciones dentro de la plataforma.
- `knowledge_base`: gestión de preguntas frecuentes y archivos de apoyo.
- `config`: configuración principal del proyecto Django.

## 🚀 Puesta en marcha local

1. Clonar el repositorio.
2. Entrar a la carpeta del proyecto.
3. Crear y activar entorno virtual.
4. Instalar dependencias.
5. Aplicar migraciones.
6. Iniciar servidor.

Comandos sugeridos en Windows PowerShell:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir en navegador:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`
- `http://127.0.0.1:8000/login/`

## ☁️ Despliegue

El proyecto **sí fue desplegado en AWS** durante su etapa académica y presentado como parte de la entrega a una empresa real.  
Para facilitar su ejecución en repositorio y revisión de portafolio, esta versión se deja funcional con **SQLite** en entorno local.

## 🎯 Contexto académico

Este repositorio conserva una entrega importante del curso para revisar decisiones de diseño, estructura y avances logrados durante la asignatura.

Proceso de trabajo considerado:

- En las primeras unidades, el trabajo fue mayoritariamente teórico.
- Antes de codificar, se desarrollaron mockups y planificación paso a paso.
- En la Evaluación 3 se presentó una versión base del sistema.
- En la Evaluación 4 se consolidó la versión final, con mejoras de interfaz, validaciones y flujo funcional completo.

## 📌 Resumen

Una base sólida en Django para gestión de soporte TI, desarrollada en equipo, aplicada en contexto real y presentada en empresa, con enfoque práctico y buen nivel de cierre académico para servir como referencia en proyectos futuros.
