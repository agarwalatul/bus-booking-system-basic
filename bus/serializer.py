from rest_framework import serializers

from bus.models import Bus, Seat


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


