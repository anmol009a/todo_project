from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Todo
from django.utils.timezone import now


# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'timestamp', 'due_date')
    list_filter = ('status', 'timestamp', 'due_date')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'status', 'timestamp')}),
        ('Additional Info', {'fields': ('due_date', 'tags')}),
    )
    readonly_fields = ('timestamp',)

    def save_model(self, request, obj, form, change):
        # Set a fallback timestamp if the object is being created
        obj.timestamp = obj.timestamp or now()
        super().save_model(request, obj, form, change)

    def clean_due_date(self, form):
        due_date = form.cleaned_data.get('due_date')
        timestamp = (
            form.instance.timestamp or now()
        )  # Fallback to current time if timestamp is None

        if due_date and due_date < timestamp.date():
            raise ValidationError(
                "Due date cannot be earlier than the creation timestamp. {{timestamp}}"
            )
        return due_date
