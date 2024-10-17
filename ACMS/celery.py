#from celery import shared_task
from django.utils import timezone
from main.models import Tasks

#@shared_task
def check_and_update_tasks():
    tasks = Tasks.objects.filter(status_task='Запланировано')
    current_date = timezone.now()
    for task in tasks:
        if task.date_task and task.date_task <= current_date:
            task.status_task = 'Выполнено'
            task.save()