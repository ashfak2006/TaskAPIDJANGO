from django.contrib import admin
from .models import tasks,message
# Register your models here.
admin.site.register(tasks)
admin.site.register(message)