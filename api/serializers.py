from rest_framework import serializers
from dashboard.models import ThreatEvent, EndpointDevice


class EndpointDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndpointDevice
        fields = '__all__'


class ThreatEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatEvent
        fields = '__all__'