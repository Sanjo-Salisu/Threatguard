from rest_framework.decorators import api_view
from rest_framework.response import Response

from dashboard.models import EndpointDevice
from dashboard.models import ThreatEvent

from .serializers import ThreatEventSerializer
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event
from django.http import JsonResponse


@csrf_exempt
def receive_event(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            Event.objects.create(
                hostname=data.get("hostname"),
                ip_address=data.get("ip_address"),
                event_type=data.get("event_type"),
                severity=data.get("severity"),
                description=data.get("description")
            )

            print("EVENT SAVED:", data)

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"status": "error"})

    return JsonResponse({"detail": "Method not allowed"}, status=405)

def get_events(request):

    events = Event.objects.all().order_by('-timestamp')[:50]

    data = []

    for e in events:
        data.append({
            "hostname": e.hostname,
            "event_type": e.event_type,
            "severity": e.severity,
            "description": e.description,
            "timestamp": e.timestamp
        })

    return JsonResponse(data, safe=False)

@api_view(['POST'])
def receive_event(request):

    hostname = request.data.get('hostname')
    ip_address = request.data.get('ip_address')

    event_type = request.data.get('event_type')
    severity = request.data.get('severity')
    description = request.data.get('description')

    if not hostname:
        return Response({
            'error': 'hostname required'
        }, status=400)

    device, created = EndpointDevice.objects.get_or_create(
        hostname=hostname,
        defaults={
            'ip_address': ip_address
        }
    )

    event = ThreatEvent.objects.create(
        device=device,
        event_type=event_type,
        severity=severity,
        description=description
    )

    serializer = ThreatEventSerializer(event)

    return Response({
        'message': 'event received',
        'data': serializer.data
    })
