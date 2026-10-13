# Práctica 6 - Django y JWT Authentication

Proyecto backend desarrollado con **Django REST Framework** y **PostgreSQL**, utilizando contenedores de **Docker** para la base de datos y documentado con **Swagger**.

---

## 🚀 Tecnologías y Herramientas Utilizadas
- **Python 3.8+ / Django 4.2**
- **Django REST Framework (DRF)**
- **PostgreSQL 15** (a través de Docker Compose)
- **drf-yasg** (para la generación de la interfaz de Swagger)
- **Linux Mint / Git / GitHub**

---

## 📂 Estructura del Proyecto

El proyecto está organizado en las siguientes aplicaciones principales:

* **`gestion_productos/`**: Modelos, serializadores y ViewSets para la administración completa del catálogo de productos.
* **`gestion_usuarios/`**: Gestión de perfiles, control de acceso y lógica de usuarios del sistema.
* **`autentificacion/`**: Configuración y endpoints dedicados a la emisión y validación de credenciales y tokens JWT.

---

## 🛠️ Instrucciones de Configuración y Ejecución

Sigue estos pasos en tu terminal para poner a marchar el proyecto en tu equipo local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TS-UAM26O-JMVH/p06_django.git](https://github.com/TS-UAM26O-JMVH/p06_django.git)
cd p06_django/proyectos_django/django4/proyecto_django/back_end_django
```

### 2. Activar el entorno virtual
```bash
source venv/bin/activate
```

### 2.1 Cómo desactivar el entorno virtual
Para salir del entorno virtual y regresar a la terminal normal del sistema, simplemente ejecuta:
```bash
deactivate
```
### 3 Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Levantar la base de datos con Docker compose
asegurate de tener DOcker activo y ejecuta el sigiente comando en la raiz donde se encuentra tu Docker-compose.yml
```bash
sudo docker compose up -d
```
### 4.1 como detener la base de datos de Docker
Cuando termines de trabajar y desees apagar el contenedor de PostgreSQL de forma limpia, ejecuta el siguiente comando en la misma ruta donde se encuentra tu docker-compose.yml:
```bash
sudo docker compose down
```

### 5. Aplicar las migraciones de la Base de datos y crear SuperUsuario
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
```

### 6. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```
### 6.1 Para detener el servidor de desarrollo de django
para detener el servidor en cualquier momento presiona en la terminal:
```
Ctrl +  C
```
---

## 🔐 Autenticación y Uso de Endpoints (JWT)

Este proyecto utiliza una política de seguridad global basada en IsAuthenticated. Por lo tanto, las peticiones a los recursos protegidos requieren un token de acceso válido.

1. Obtener el Token: Realiza una petición POST enviando tus credenciales (usuario y contraseña) a la ruta:

[http://127.0.0.1:8000/api/token/](http://127.0.0.1:8000/api/token/)

El servidor te devolverá un JSON con los tokens access y refresh.

2. Autorización en Swagger:

    >Dirígete a la interfaz de Swagger en http://127.0.0.1:8000/swagger/ (o la ruta configurada).

    >Haz clic en el botón Authorize.

    >Ingresa tu token de acceso anteponiendo la palabra Bearer  seguida de un espacio:
      ```
      Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      ```
    >¡Listo! Ahora podrás probar los endpoints protegidos de productos y usuarios.
---

## 👨‍💻 Autor

Desarrollado por Juan Valentin.


