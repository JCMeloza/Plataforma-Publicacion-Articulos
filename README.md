# 📰 Plataforma de Publicación de Artículos - Revista Digital

[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-5.2.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![CSS3](https://img.shields.io/badge/CSS3-Vanilla-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/es/docs/Web/CSS)
[![Responsive](https://img.shields.io/badge/Responsive-Mobile--First-00adb5?style=for-the-badge)](https://developer.mozilla.org/es/docs/Web/CSS/CSS_media_queries)

Una plataforma web dinámica para la publicación y gestión de artículos en una revista digital. El sistema cuenta con autenticación de usuarios, perfiles de cuenta personalizables, interacciones (likes y comentarios) y un flujo editorial completo estructurado bajo diferentes roles de acceso.

🌐 **Demo online**: [https://publicacionarticulos.onrender.com/](https://publicacionarticulos.onrender.com/)

El diseño del sitio es 100% responsivo y está optimizado bajo la filosofía **Mobile-First**, garantizando una visualización limpia tanto en dispositivos móviles (mediante un menú hamburguesa CSS sin Javascript y tablas convertidas a tarjetas dinámicas) como en computadoras de escritorio.

---

## 🚀 Características y Flujo de Trabajo por Roles

La plataforma implementa un sistema robusto de permisos según el tipo de usuario:

### 👤 1. Lector (Reader)
- **Visualización**: Acceso al feed principal de artículos publicados.
- **Interacción**: Sistema de "Me gusta" (Likes) dinámicos y caja de comentarios en cada artículo.
- **Gestión de Perfil**: Posibilidad de modificar su avatar, nombre de usuario y biografía desde su panel personal.

### ✍️ 2. Redactor (Reviewer)
- **Espacio de Trabajo**: Acceso a su escritorio personal (`Mi Escritorio`).
- **Creación**: Redacción de nuevos artículos (título, contenido, categoría, etiquetas e imagen de portada).
- **Ciclo de Vida**: Los artículos se guardan inicialmente como **Borradores** o **Rechazados**. El redactor puede editarlos y enviarlos formalmente a revisión cuando estén listos.

### 🕵️‍♂️ 3. Editor (Editor)
- **Revisión Editorial**: Visualiza todos los artículos enviados por los redactores que están **Pendientes** de aprobación.
- **Flujo de Calidad**: El editor puede revisar el detalle de la publicación y decidir **Aprobar** (lo que publica el artículo automáticamente en la web) o **Rechazar** (devolviéndolo al escritorio del redactor con el estado correspondiente para su corrección).

### ⚙️ 4. Administrador (Superuser)
- **Control Global**: Acceso al panel de administración general de Django y a un dashboard personalizado en el sitio.
- **Gestión de Usuarios**: Modificación directa del rol de cualquier usuario registrado en la base de datos (pasar de Lector a Redactor o Editor).
- **Taxonomías**: Creación y gestión de categorías y etiquetas para la clasificación de los artículos.

---

## 🛠️ Stack Tecnológico

- **Backend**: [Django 5.2](https://docs.djangoproject.com/en/5.2/) (Patrón MVT)
- **Base de Datos**: PostgreSQL (Supabase) en producción / SQLite3 en desarrollo local
- **Hosting**: [Render](https://render.com/) (servicio web gratuito)
- **Base de Datos remota**: [Supabase](https://supabase.com/) (plan gratuito)
- **Manejo de Archivos**: Pillow (procesamiento de imágenes de perfil y portadas de artículos)
- **Estilos**: Vanilla CSS3 responsivo estructurado y sin frameworks CSS (Tailwind/Bootstrap), asegurando máxima eficiencia y rendimiento.

---

## ⚙️ Instalación y Configuración Local

Seguí estos pasos para desplegar el proyecto en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/JCMeloza/Plataforma-Publicacion-Articulos.git
cd Plataforma-Publicacion-Articulos
```

### 2. Crear y activar el entorno virtual
En Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
En Windows:
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar las migraciones de la base de datos
```bash
python manage.py migrate
```

### 5. Crear el superusuario
```bash
python manage.py createsuperuser
```

### 6. Datos de prueba
Para probar la plataforma con diferentes roles, podes crear los siguientes usuarios:
- **Superusuario (Admin)**: `admin` / `admin`
- **Lector**: `lector_usuario1` / `prueba`
- **Redactor**: `redactor_usuario1` / `prueba`
- **Editor**: `editor_usuario1` / `prueba`

### 7. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

Una vez que el servidor esté corriendo, podés ingresar a:
- La aplicación web: `http://127.0.0.1:8000/`
- El panel de administración de Django: `http://127.0.0.1:8000/admin/`

---

## 🌐 Despliegue en Producción (Render + Supabase)

Guía completa para desplegar la plataforma gratis en internet.

### Paso 1: Crear la base de datos en Supabase

1. Andá a [https://supabase.com/](https://supabase.com/) y creá una cuenta gratuita.
2. Hacé clic en **"New Project"** y completá:
   - **Organization**: Creá una nueva o usá una existente.
   - **Project name**: `publicacion-articulos` (o el que prefieras).
   - **Database Password**: Generá una contraseña fuerte y **guardala** (la vas a necesitar después).
   - **Region**: Elegí la más cercana a tu audiencia (ej: `EU West 1` para Europa).
3. Esperá a que el proyecto se cree (~2 minutos).

### Paso 2: Crear las tablas en Supabase

Una vez creado el proyecto:

1. Andá a la pestaña **"SQL Editor"** del dashboard.
2. Creá un "New query" y pegá el siguiente SQL para crear todas las tablas necesarias:

```sql
-- Tipos de roles
DO $$ BEGIN
  CREATE TYPE user_role AS ENUM ('lector', 'redactor', 'editor', 'admin');
EXCEPTION WHEN duplicate_object THEN null;
END $$;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users_user (
  id BIGSERIAL PRIMARY KEY,
  password VARCHAR(128) NOT NULL,
  last_login TIMESTAMPTZ,
  is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
  username VARCHAR(150) UNIQUE NOT NULL,
  first_name VARCHAR(150) NOT NULL DEFAULT '',
  last_name VARCHAR(150) NOT NULL DEFAULT '',
  email VARCHAR(254) NOT NULL DEFAULT '',
  is_staff BOOLEAN NOT NULL DEFAULT FALSE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  role user_role NOT NULL DEFAULT 'lector',
  bio TEXT NOT NULL DEFAULT '',
  avatar VARCHAR(100)
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS articles_category (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  description TEXT NOT NULL DEFAULT ''
);

-- Tabla de etiquetas
CREATE TABLE IF NOT EXISTS articles_tag (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  slug VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de artículos
CREATE TABLE IF NOT EXISTS articles_article (
  id BIGSERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  slug VARCHAR(200) UNIQUE NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  status VARCHAR(20) NOT NULL DEFAULT 'borrador',
  cover_image VARCHAR(100),
  author_id BIGINT NOT NULL REFERENCES users_user(id),
  category_id BIGINT REFERENCES articles_category(id)
);

-- Tabla de relación artículo-etiqueta
CREATE TABLE IF NOT EXISTS articles_article_tags (
  id BIGSERIAL PRIMARY KEY,
  article_id BIGINT NOT NULL REFERENCES articles_article(id) ON DELETE CASCADE,
  tag_id BIGINT NOT NULL REFERENCES articles_tag(id) ON DELETE CASCADE,
  UNIQUE(article_id, tag_id)
);

-- Tabla de comentarios
CREATE TABLE IF NOT EXISTS articles_comment (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  article_id BIGINT NOT NULL REFERENCES articles_article(id) ON DELETE CASCADE,
  author_id BIGINT NOT NULL REFERENCES users_user(id)
);

-- Tabla de likes
CREATE TABLE IF NOT EXISTS articles_like (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  article_id BIGINT NOT NULL REFERENCES articles_article(id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users_user(id),
  UNIQUE(article_id, user_id)
);

-- Tabla de mensajes de contacto
CREATE TABLE IF NOT EXISTS articles_contactmessage (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(254) NOT NULL,
  subject VARCHAR(200) NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  is_read BOOLEAN NOT NULL DEFAULT FALSE
);

-- Tabla de revisiones editoriales
CREATE TABLE IF NOT EXISTS editorial_review (
  id BIGSERIAL PRIMARY KEY,
  status VARCHAR(20) NOT NULL DEFAULT 'pendiente',
  notes TEXT NOT NULL DEFAULT '',
  reviewed_at TIMESTAMPTZ,
  article_id BIGINT NOT NULL REFERENCES articles_article(id),
  reviewer_id BIGINT NOT NULL REFERENCES users_user(id)
);

-- Tablas de Django (required)
CREATE TABLE IF NOT EXISTS django_migrations (
  id BIGSERIAL PRIMARY KEY,
  app VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  applied TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS django_content_type (
  id BIGSERIAL PRIMARY KEY,
  app_label VARCHAR(100) NOT NULL,
  model VARCHAR(100) NOT NULL,
  UNIQUE(app_label, model)
);

CREATE TABLE IF NOT EXISTS auth_permission (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  content_type_id BIGINT NOT NULL REFERENCES django_content_type(id),
  codename VARCHAR(100) NOT NULL,
  UNIQUE(content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS auth_group (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_group_permissions (
  id BIGSERIAL PRIMARY KEY,
  group_id BIGINT NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
  permission_id BIGINT NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
  UNIQUE(group_id, permission_id)
);

CREATE TABLE IF NOT EXISTS users_user_groups (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
  group_id BIGINT NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
  UNIQUE(user_id, group_id)
);

CREATE TABLE IF NOT EXISTS users_user_user_permissions (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users_user(id) ON DELETE CASCADE,
  permission_id BIGINT NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
  UNIQUE(user_id, permission_id)
);

CREATE TABLE IF NOT EXISTS django_admin_log (
  id BIGSERIAL PRIMARY KEY,
  action_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  object_id TEXT,
  object_repr VARCHAR(200) NOT NULL,
  action_flag SMALLINT NOT NULL,
  change_message TEXT NOT NULL,
  content_type_id BIGINT REFERENCES django_content_type(id),
  user_id BIGINT NOT NULL REFERENCES users_user(id)
);

CREATE TABLE IF NOT EXISTS django_session (
  session_key VARCHAR(40) PRIMARY KEY,
  session_data TEXT NOT NULL,
  expire_date TIMESTAMPTZ NOT NULL
);
```

3. Ejecutá el query. Las tablas se crearán automáticamente.

### Paso 3: Insertar datos de prueba (opcional)

Si querés tener artículos y usuarios de ejemplo en producción, ejecutá estos queries en el SQL Editor de Supabase después de crear las tablas:

```sql
-- Usuarios (contraseña: prueba para todos, excepto admin)
-- Generá los hashes con: python -c "from django.contrib.auth.hashers import make_password; print(make_password('prueba'))"
-- O usá el admin panel para crear usuarios después del deploy

-- Categorías
INSERT INTO articles_category (name, slug, description) VALUES
('Tecnología', 'tecnologia', 'Artículos sobre innovación y tecnología'),
('Ciencia', 'ciencia', 'Descubrimientos y avances científicos'),
('Cultura', 'cultura', 'Arte, cine, música y tendencias culturales'),
('Deportes', 'deportes', 'Noticias y análisis deportivos'),
('Economía', 'economia', 'Finanzas, mercados y economía global');

-- Etiquetas
INSERT INTO articles_tag (name, slug) VALUES
('IA', 'ia'),
('Sostenibilidad', 'sostenibilidad'),
('Fútbol', 'futbol'),
('Cine', 'cine'),
('Inversión', 'inversion');

-- Usuarios (usando hashes de Django)
INSERT INTO users_user (username, password, email, first_name, last_name, role, is_staff, is_superuser) VALUES
('admin', '$argon2id$v=19$m=65536,t=3,p=4$TUFBSEhBSEhBSEhBSEhBSEg$RANDRANDRANDRANDRANDRAND', 'admin@test.com', 'Admin', 'User', 'admin', true, true),
('redactor_usuario1', '$argon2id$v=19$m=65536,t=3,p=4$TUFBSEhBSEhBSEhBSEhBSEg$RANDRANDRANDRANDRANDRAND', 'redactor@test.com', 'Redactor', 'Usuario1', 'redactor', false, false),
('editor_usuario1', '$argon2id$v=19$m=65536,t=3,p=4$TUFBSEhBSEhBSEhBSEhBSEg$RANDRANDRANDRANDRANDRAND', 'editor@test.com', 'Editor', 'Usuario1', 'editor', false, false),
('lector_usuario1', '$argon2id$v=19$m=65536,t=3,p=4$TUFBSEhBSEhBSEhBSEhBSEg$RANDRANDRANDRANDRANDRAND', 'lector@test.com', 'Lector', 'Usuario1', 'lector', false, false);
```

> **Nota**: Los hashes de contraseña son ejemplos. Para datos reales, creá los usuarios desde el panel de admin de Django después del deploy, o generá los hashes con:
> ```bash
> python -c "from django.contrib.auth.hashers import make_password; print(make_password('tu_password'))"
> ```

### Paso 4: Crear la cuenta de Render

1. Andá a [https://render.com/](https://render.com/) y creá una cuenta gratuita.
2. Conectá tu cuenta de GitHub para acceder a tus repositorios.

### Paso 5: Crear el servicio web en Render

1. En el dashboard de Render, hacé clic en **"New +"** → **"Web Service"**.
2. Seleccioná tu repositorio de GitHub: `JCMeloza/Plataforma-Publicacion-Articulos`.
3. Configurá el servicio:
   - **Name**: `publicacion-articulos`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```bash
     gunicorn config.wsgi
     ```
   - **Plan**: `Free`

### Paso 6: Configurar variables de entorno en Render

En la página de tu servicio en Render, andá a la pestaña **"Environment"** y agregá estas variables:

| Variable | Valor |
|----------|-------|
| `DATABASE_URL` | `postgresql://postgres.TU_PROJECT_REF:TU_PASSWORD@aws-1-TU_REGION.pooler.supabase.com:6543/postgres?sslmode=require` |
| `SECRET_KEY` | Una clave secreta larga (generala con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DEBUG` | `False` |

#### Cómo obtener el `DATABASE_URL` de Supabase

1. En el dashboard de Supabase, andá a **Settings** → **Database**.
2. Buscá la pestaña **"Connection pooling"** o **"Transaction"**.
3. Copiá la URI que aparece. Tiene este formato:
   ```
   postgresql://postgres.gnxlcshqlciagpxxndgm:TU_PASSWORD@aws-1-eu-west-1.pooler.supabase.com:6543/postgres
   ```
4. Agregale `?sslmode=require` al final si no lo tiene.

> **Importante**: Usá la conexión de **Connection Pooling** (puerto 6543), NO la conexión directa (puerto 5432). La conexión directa falla desde Render por restricciones de red IPv6.

### Paso 7: Desplegar

1. Hacé clic en **"Create Web Service"** en Render.
2. El deploy comenzará automáticamente. Esperá ~3-5 minutos.
3. Tu app estará disponible en: `https://TU-SERVICIO.onrender.com/`

### Paso 8: Crear superusuario en producción

Una vez desplegado, necesitás crear un superuser para acceder al admin. Desde la terminal local:

```bash
# Conectate a tu base de datos de Supabase
export DATABASE_URL="postgresql://postgres.TU_REF:TU_PASSWORD@aws-1-TU_REGION.pooler.supabase.com:6543/postgres?sslmode=require"

# Crear superuser
python manage.py createsuperuser
```

O creá los usuarios directamente desde el panel de admin de Django (`https://TU-SERVICIO.onrender.com/admin/`) una vez que tengas un superuser.

---

## 🔧 Troubleshooting

### Error 500 en la homepage
- Verificá que `DATABASE_URL` esté configurado correctamente en Render.
- Asegurate de usar el pooler (puerto 6543), no la conexión directa.
- Revisá los logs de Render en la pestaña "Logs".

### Error "No se puede conectar a la base de datos"
- Verificá que la contraseña en `DATABASE_URL` sea correcta.
- Asegurate de que `DEBUG=False` esté configurado (si está en `True`, los errores se muestran en pantalla).
- Probá con `?sslmode=require` al final de la URL.

### Error "Static files not found"
- Asegurate de que el build command incluya `python manage.py collectstatic --noinput`.
- Verificá que `STATIC_ROOT` esté configurado en `settings.py`.

### La app tarda mucho en cargar
- Render free tier apaga los servicios después de inactividad. El primer request puede tardar 30-60 segundos (cold start).
- Los requests subsiguientes serán normales.

---

## 📂 Estructura del Proyecto

```text
Plataforma-Publicacion-Articulos/
├── articles/            # Aplicación principal de artículos, perfiles y valoraciones
│   ├── templates/       # Plantillas HTML de los dashboards y detalle de artículo
│   ├── models.py        # Modelos (Article, Comment, Category, Tag)
│   └── views.py         # Controladores y lógica de negocio
├── config/              # Directorio de configuración de Django (settings, urls)
├── editorial/           # Modelos de control del flujo editorial
├── static/              # Archivos estáticos (JavaScript, Imágenes)
│   └── css/             # Hojas de estilo modularizadas y responsivas (base, home, dashboard, etc.)
├── templates/           # Plantillas generales (Base HTML, Login, navbar, footer)
│   ├── includes/        # Fragmentos de plantillas reutilizables (_navbar, _footer)
│   └── registration/    # Plantillas de inicio de sesión y registro
├── manage.py            # Script de gestión de Django
├── requirements.txt     # Archivo de dependencias del proyecto
├── Procfile             # Configuración de Render para Gunicorn
└── README.md            # Documentación del proyecto
```

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, ver el archivo de licencia correspondiente.

---
Desarrollado con pasión por [JCMeloza](https://github.com/JCMeloza).
