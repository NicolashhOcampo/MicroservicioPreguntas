## Inicializar Proyecto
```bash
#Crear entorno virtual
python -m venv .venv

#Activar entorno virtual
source .venv/Scripts/activate

#Levantar servidor
fastapi dev app/main.py

#Consumir rabbit
python -m app.rabbit.article_deleted_consumer

```