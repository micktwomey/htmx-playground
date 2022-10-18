from django.contrib import admin

from .models import Widget


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    pass
