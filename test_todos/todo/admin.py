from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(ModelAdmin):
    list_display =['title', 'id']
# Register your models here.
