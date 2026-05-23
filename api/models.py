from django.db import models


class Event(models.Model):
    hostname = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.severity}"