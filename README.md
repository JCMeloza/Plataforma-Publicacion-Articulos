# 📰 Plataforma de Publicación de Artículos - Revista Digital

[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-5.2.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![CSS3](https://img.shields.io/badge/CSS3-Vanilla-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/es/docs/Web/CSS)
[![Responsive](https://img.shields.io/badge/Responsive-Mobile--First-00adb5?style=for-the-badge)](https://developer.mozilla.org/es/docs/Web/CSS/CSS_media_queries)

Una plataforma web dinámica para la publicación y gestión de artículos en una revista digital. El sistema cuenta con autenticación de usuarios, perfiles de cuenta personalizables, interacciones (likes y comentarios) y un flujo editorial completo estructurado bajo diferentes roles de acceso.

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
- **Base de Datos**: SQLite3 (desarrollo local)
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
└── README.md            # Documentación del proyecto
```

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, ver el archivo de licencia correspondiente.

---
Desarrollado con pasión por [JCMeloza](https://github.com/JCMeloza).
