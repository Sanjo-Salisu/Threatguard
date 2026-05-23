from django.shortcuts import render
from .models import ThreatEvent, EndpointDevice


def dashboard(request):

    threats = ThreatEvent.objects.order_by('-created_at')[:10]

    total_devices = EndpointDevice.objects.count()

    high_threats = ThreatEvent.objects.filter(
        severity='HIGH'
    ).count()

    context = {
        'threats': threats,
        'total_devices': total_devices,
        'high_threats': high_threats,
    }

    return render(request, 'dashboard/index.html', context)