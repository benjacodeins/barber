# 🚀 Guía de Despliegue en PythonAnywhere - Proyecto Barber

Esta guía te llevará paso a paso para desplegar tu aplicación Django de gestión de reservas de barbería en PythonAnywhere en modo demo.

---

## 📋 Requisitos Previos

- Cuenta en [PythonAnywhere](https://www.pythonanywhere.com/) (cuenta gratuita es suficiente para demo)
- Código del proyecto subido a PythonAnywhere (vía Git o upload directo)
- Python 3.10 o superior disponible en PythonAnywhere

> ℹ️ **Nota sobre Base de Datos**: Este proyecto funciona perfectamente con **SQLite** (incluido en cuentas gratuitas). MySQL solo es necesario si tienes una cuenta de pago y necesitas más funcionalidades de base de datos.

---

## 🔧 Paso 1: Preparar el Proyecto en PythonAnywhere

### 1.1 Acceder a la consola Bash

1. Inicia sesión en PythonAnywhere
2. Ve a la pestaña **"Consoles"**
3. Haz clic en **"Bash"** para abrir una nueva consola

### 1.2 Subir el Proyecto

**Opción A: Usando Git (Recomendado)**
```bash
cd ~
git clone https://github.com/tuusuario/barber.git
cd barber
```

**Opción B: Upload Manual**
1. Usa la pestaña **"Files"** en PythonAnywhere
2. Sube el archivo ZIP del proyecto
3. Descomprímelo en tu directorio home:
```bash
cd ~
unzip barber.zip
cd barber
```

---

## 🗄️ Paso 2: Base de Datos (Opcional - Solo para Cuentas de Pago)

> ⚠️ **IMPORTANTE para Cuentas Gratuitas**: Si tienes una cuenta gratuita de PythonAnywhere, **SALTA este paso completo**. El proyecto usará SQLite automáticamente y funciona perfectamente para demos.

<details>
<summary><b>👉 Click aquí solo si tienes cuenta de PAGO y quieres usar MySQL</b></summary>

### 2.1 Crear la Base de Datos MySQL

1. Ve a la pestaña **"Databases"** en PythonAnywhere
2. En la sección **"MySQL"**, configura tu contraseña si aún no lo has hecho
3. En **"Create a new database"**, ingresa un nombre (ej: `barber_demo`)
4. Haz clic en **"Create"**

> ℹ️ **Nota**: El nombre completo de tu base de datos será `tuusuario$barber_demo`

### 2.2 Anotar las Credenciales

Toma nota de:
- **Nombre de la BD**: `tuusuario$barber_demo`
- **Usuario**: Tu nombre de usuario de PythonAnywhere
- **Contraseña**: La que configuraste
- **Host**: `tuusuario.mysql.pythonanywhere-services.com`

</details>

---

## ⚙️ Paso 3: Configurar Variables de Entorno

### 3.1 Crear el archivo .env

En la consola Bash:

```bash
cd ~/barber
cp .env.example .env
nano .env
```

### 3.2 Editar las Variables

Modifica el archivo `.env` con tus datos reales.

**Para Cuenta GRATUITA (con SQLite):**
```bash
# Generar una SECRET_KEY segura
DJANGO_SECRET_KEY=genera-una-clave-secreta-aqui
DJANGO_DEBUG=False

# Reemplaza "tuusuario" con tu nombre de usuario de PythonAnywhere
ALLOWED_HOSTS=tuusuario.pythonanywhere.com,localhost,127.0.0.1

# No necesitas configurar nada más - usará SQLite automáticamente
```

**Para Cuenta de PAGO (con MySQL - opcional):**
```bash
DJANGO_SECRET_KEY=genera-una-clave-secreta-aqui
DJANGO_DEBUG=False
ALLOWED_HOSTS=tuusuario.pythonanywhere.com,localhost,127.0.0.1

# Configuración de MySQL (descomentar y completar)
DB_NAME=tuusuario$barber_demo
DB_USER=tuusuario
DB_PASSWORD=tu-password-mysql
DB_HOST=tuusuario.mysql.pythonanywhere-services.com
```

**Para generar una SECRET_KEY segura:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Guarda el archivo:
- Presiona `Ctrl + O` para guardar
- Presiona `Enter` para confirmar
- Presiona `Ctrl + X` para salir

---

## 🛠️ Paso 4: Ejecutar el Script de Setup

### 4.1 Dar Permisos de Ejecución

```bash
chmod +x setup_pythonanywhere.sh
```

### 4.2 Ejecutar el Script

```bash
./setup_pythonanywhere.sh
```

Este script automáticamente:
- ✅ Crea el virtual environment
- ✅ Instala todas las dependencias
- ✅ Aplica las migraciones de la base de datos
- ✅ Recolecta archivos estáticos

---

## 🌐 Paso 5: Configurar la Web App

### 5.1 Crear la Web App

1. Ve a la pestaña **"Web"**
2. Haz clic en **"Add a new web app"**
3. Selecciona tu dominio gratuito: `tuusuario.pythonanywhere.com`
4. Selecciona **"Manual configuration"**
5. Selecciona **Python 3.10** (o la versión que uses)

### 5.2 Configurar el Virtual Environment

En la sección **"Virtualenv"**:

1. Ingresa la ruta: `/home/tuusuario/.virtualenvs/barber-venv`
2. Haz clic en el ícono ✓ para confirmar

### 5.3 Configurar el archivo WSGI

1. En la sección **"Code"**, haz clic en el link del archivo **WSGI configuration file**
2. **Borra todo el contenido** del archivo
3. Copia y pega el contenido de `pythonanywhere_wsgi.py` de tu proyecto
4. **IMPORTANTE**: Reemplaza `USUARIO` con tu nombre de usuario en estas líneas:
   ```python
   project_home = '/home/USUARIO/barber'
   virtualenv_path = '/home/USUARIO/.virtualenvs/barber-venv'
   ```
5. Guarda el archivo (botón **Save** en la esquina superior derecha)

### 5.4 Configurar Archivos Estáticos

En la sección **"Static files"**, añade estas rutas:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/tuusuario/barber/staticfiles` |
| `/media/` | `/home/tuusuario/barber/media` |

> 💡 Reemplaza `tuusuario` con tu nombre de usuario

---

## 👤 Paso 6: Crear Superusuario

Para acceder al panel de administración:

```bash
cd ~/barber
source ~/.virtualenvs/barber-venv/bin/activate
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario administrador.

---

## 🚀 Paso 7: ¡Lanzar la Aplicación!

1. Ve a la pestaña **"Web"**
2. Haz clic en el botón verde **"Reload tuusuario.pythonanywhere.com"**
3. Espera unos segundos
4. Visita tu sitio: `https://tuusuario.pythonanywhere.com`

---

## ✅ Verificación

### Verificar que todo funciona:

1. **Página principal**: `https://tuusuario.pythonanywhere.com`
2. **Panel de administración**: `https://tuusuario.pythonanywhere.com/admin`
3. **Archivos estáticos**: Verifica que el CSS se cargue correctamente

---

## 🔍 Solución de Problemas

### Error 502 Bad Gateway

- Verifica el **error log** en la pestaña Web (sección "Log files")
- Asegúrate de que las rutas en el WSGI estén correctas
- Verifica que el virtual environment esté activado

### Los archivos estáticos no se cargan

- Verifica las rutas en la sección "Static files"
- Ejecuta nuevamente: `python manage.py collectstatic`
- Asegúrate de que la ruta apunte a `staticfiles` (no `static`)

### Error en la base de datos

- Verifica las credenciales en el archivo `.env`
- Asegúrate de que el nombre de la BD incluya tu usuario: `tuusuario$nombre`
- Verifica que DEBUG=False en el archivo `.env`

### Ver los logs

```bash
# Log de errores de la aplicación
tail -f ~/.pythonanywhere/error.log

# Log del servidor web
tail -f ~/.pythonanywhere/server.log
```

---

## 🔄 Actualizar la Aplicación

Cuando hagas cambios en tu código:

```bash
cd ~/barber
git pull  # Si usas Git
source ~/.virtualenvs/barber-venv/bin/activate
python manage.py migrate  # Si hay nuevas migraciones
python manage.py collectstatic --noinput  # Si cambiaron archivos estáticos
```

Luego en la pestaña **Web**, haz clic en **"Reload"**

---

## 📚 Recursos Adicionales

- [Documentación de PythonAnywhere](https://help.pythonanywhere.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [PythonAnywhere Forums](https://www.pythonanywhere.com/forums/)

---

## 🎉 ¡Listo!

Tu aplicación de gestión de reservas para barbería ahora está desplegada en PythonAnywhere. Puedes compartir la URL con clientes para demostrar el sistema.

> **💡 Tip para Demo**: Crea algunos datos de ejemplo (servicios, horarios) desde el panel de administración para mostrar la funcionalidad completa.
