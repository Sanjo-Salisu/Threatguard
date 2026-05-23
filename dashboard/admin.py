from django.contrib import admin
from .models import EndpointDevice, ThreatEvent

admin.site.register(EndpointDevice)
admin.site.register(ThreatEvent)