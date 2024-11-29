from django.contrib import admin
from .models import Todo


# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'timestamp', 'due_date')
    list_filter = ('status', 'timestamp', 'due_date')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'status')}),
        ('Additional Info', {'fields': ('due_date', 'tags')}),
    )
    readonly_fields = ('timestamp',)
