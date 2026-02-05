"""
Configuración WSGI para PythonAnywhere
Este archivo debe copiarse al configurador WSGI en la web app de PythonAnywhere
"""
import os
import sys
from pathlib import Path

# Ruta al proyecto (CAMBIAR SEGÚN TU USUARIO)
# Ejemplo: /home/tuusuario/barber
project_home = '/home/USUARIO/barber'

# Añadir el directorio del proyecto al path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activar el virtual environment
# Ejemplo: /home/tuusuario/.virtualenvs/barber-venv
virtualenv_path = '/home/USUARIO/.virtualenvs/barber-venv'
activate_this = Path(virtualenv_path) / 'bin' / 'activate_this.py'

# Cargar variables de entorno desde .env
env_file = Path(project_home) / '.env'
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

# Configurar Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peluqueria.settings')

# Importar la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
