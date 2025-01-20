from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    REQUEST_STATUS = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    type_of_service = models.CharField(max_length=255)
    details = models.TextField()
    attached_file = models.FileField(upload_to='attachments/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=REQUEST_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} by {self.customer.username}"
