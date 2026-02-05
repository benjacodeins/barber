# 💈 Sistema de Reservas para Barbería

Sistema web desarrollado en Django para gestión de reservas de peluquería/barbería.

## 🚀 Deploy en PythonAnywhere

Para desplegar este proyecto en PythonAnywhere como demo, sigue la guía completa:

**📖 [Ver Guía de Despliegue Completa](DEPLOY_PYTHONANYWHERE.md)**

### Resumen Rápido

1. Clonar/subir el proyecto a PythonAnywhere
2. Configurar base de datos MySQL
3. Crear archivo `.env` con credenciales
4. Ejecutar `./setup_pythonanywhere.sh`
5. Configurar Web App y WSGI
6. ¡Listo!

## 🛠️ Desarrollo Local

### Requisitos

- Python 3.10+
- Django 5.0+
- SQLite (desarrollo) / MySQL (producción)

### Instalación Local

```bash
# Clonar el repositorio
git clone <url-repositorio>
cd barber

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env para desarrollo local
cp .env.example .env
# Editar .env y configurar DJANGO_DEBUG=True

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

Accede a `http://localhost:8000`

## 📁 Estructura del Proyecto

```
barber/
├── peluqueria/          # Configuración principal del proyecto
│   ├── settings.py      # Configuraciones
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # WSGI para producción
├── reservas/           # App de gestión de reservas
├── templates/          # Plantillas HTML
├── static/            # Archivos estáticos (CSS, JS, imágenes)
├── media/             # Archivos subidos por usuarios
├── manage.py          # Utilidad de Django
├── requirements.txt   # Dependencias
├── .env.example       # Ejemplo de variables de entorno
├── pythonanywhere_wsgi.py  # Configuración WSGI para PythonAnywhere
├── setup_pythonanywhere.sh  # Script de setup automático
└── DEPLOY_PYTHONANYWHERE.md # Guía de despliegue
```

## 🔧 Configuración

El proyecto utiliza variables de entorno para la configuración. Crea un archivo `.env` basado en `.env.example`:

- `DJANGO_SECRET_KEY`: Clave secreta de Django
- `DJANGO_DEBUG`: True/False para modo debug
- `ALLOWED_HOSTS`: Hosts permitidos (separados por comas)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`: Configuración de MySQL

## 📝 Características

- ✅ Sistema de reservas online
- ✅ Panel de administración
- ✅ Gestión de servicios
- ✅ Gestión de horarios
- ✅ Responsive design

## 🔐 Seguridad

- Nunca subas el archivo `.env` al repositorio
- Cambia la `SECRET_KEY` en producción
- Mantén `DEBUG=False` en producción
- Actualiza regularmente las dependencias

## 📄 Licencia

[Especificar licencia]

## 👤 Autor

BENJAcode

---

**¿Listo para desplegar?** 👉 [Lee la guía completa](DEPLOY_PYTHONANYWHERE.md)
