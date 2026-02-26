import os
from celery import Celery

# Define o nome do projeto (deve ser 'setup' porque é o nome da tua pasta)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('setup')

# O namespace 'CELERY' obriga que as configs no settings.py comecem com CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Procura automaticamente ficheiros tasks.py dentro das tuas apps
app.autodiscover_tasks()