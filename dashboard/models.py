from django.db import models


class EndpointDevice(models.Model):
    hostname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    online = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname


class ThreatEvent(models.Model):

    EVENT_TYPES = [
        ('USB', 'USB'),
        ('FILE', 'FILE'),
        ('LOG', 'LOG'),
    ]

    SEVERITY_CHOICES = [
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH'),
    ]

    device = models.ForeignKey(
        EndpointDevice,
        on_delete=models.CASCADE,
        related_name='events'
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.hostname} - {self.event_type}"