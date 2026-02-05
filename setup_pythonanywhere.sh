#!/bin/bash
# Script de configuración inicial para PythonAnywhere
# Ejecutar desde la consola Bash de PythonAnywhere

echo "========================================="
echo "Setup de Proyecto Barber en PythonAnywhere"
echo "========================================="
echo ""

# Variables (PERSONALIZAR SEGÚN TU USUARIO)
PROJECT_DIR="$HOME/barber"
VENV_DIR="$HOME/.virtualenvs/barber-venv"

# Verificar que estemos en el directorio del proyecto
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: No se encuentra el directorio del proyecto en $PROJECT_DIR"
    echo "Asegúrate de haber clonado o subido el proyecto primero"
    exit 1
fi

cd "$PROJECT_DIR"

# Crear virtual environment si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment ya existe"
fi

# Activar virtual environment
echo "Activando virtual environment..."
source "$VENV_DIR/bin/activate"

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: No se encuentra el archivo .env"
    echo "Por favor, crea un archivo .env basado en .env.example"
    echo "y configura las variables de entorno antes de continuar"
    echo ""
    read -p "¿Deseas continuar de todas formas? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Crear directorio para archivos estáticos si no existe
echo "Creando directorios..."
mkdir -p staticfiles
mkdir -p media

# Aplicar migraciones
echo "Aplicando migraciones de base de datos..."
python manage.py migrate

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "✅ Setup completado!"
echo "========================================="
echo ""
echo "Próximos pasos:"
echo "1. Configurar el archivo WSGI en la web app de PythonAnywhere"
echo "2. Configurar la ruta de archivos estáticos: /static/ -> $PROJECT_DIR/staticfiles"
echo "3. Configurar la ruta de archivos media: /media/ -> $PROJECT_DIR/media"
echo "4. Crear un superusuario: python manage.py createsuperuser"
echo "5. Recargar la aplicación web"
echo ""
