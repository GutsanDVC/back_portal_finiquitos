# Portal Finiquitos Backend

Este es el backend del sistema Portal Finiquitos, construido con Django Rest Framework y PostgreSQL.

## Estructura principal
- `users`: gestión de usuarios y perfiles.
- `employees`: datos maestros de trabajadores.
- `settlements`: lógica y modelos de finiquitos.
- `audit`: logs y trazabilidad.
- `core`: utilidades y configuración global.

## Requisitos
- Python 3.10+
- PostgreSQL 13+

## Instalación rápida
```sh
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Comandos útiles
- `python manage.py migrate`  # Migraciones iniciales
- `python manage.py createsuperuser`  # Crear usuario admin
- `python manage.py runserver`  # Levantar servidor local

## Lint y formato
- `black .`
- `flake8 .`

## Pruebas
- `pytest`

---

Recuerda mantener las buenas prácticas de código y documentación.
