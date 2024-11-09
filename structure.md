```
nebula-partner-backend/
├── alembic/
│   ├── versions/
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── documentacion/
│   ├── ER_Diagram_Simplified_Partner_App.png
│   ├── ER_User-Company.md
│   ├── flujo.md
│   ├── historias_usuario.md
│   └── tareas_pendientes.md
├── src/
│   ├── account/
│   │   ├── models.py
│   │   └── repository.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth0_helper.py
│   │   ├── jwt_handler.py
│   │   ├── permissions.py
│   │   └── routes.py
│   ├── company/
│   │   ├── models.py
│   │   └── repository.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── cors.py
│   ├── supplier/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── routes.py
│   │   └── service.py
│   ├── user/
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   └── pagination.py
├── tests/
│   └── __init__.py
├── versions/
│   ├── 20071d0d310b_first_migration.py
│   └── c0bbeefe9b90_all_models.py
├── .env
├── .env.template
├── .gitignore
├── Makefile
├── README.md
├── alembic.ini
├── generate_structure.py
├── logging.ini
├── poetry.lock
├── pyproject.toml
└── structure.md
```
