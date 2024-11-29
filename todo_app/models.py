from django.db import models

# Create your models here.
class Todo(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('WORKING', 'Working'),
        ('PENDING_REVIEW', 'Pending Review'),
        ('COMPLETED', 'Completed'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    due_date = models.DateField(null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)  # Ensure uniqueness in logic
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')

    def save(self, *args, **kwargs):
        self.tags = list(set(self.tags))  # Remove duplicate tags
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
