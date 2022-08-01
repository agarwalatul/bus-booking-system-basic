from rest_framework import serializers

from booking_system.models import Trip, TripSeatStatus, Ticket


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class TripSeatStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripSeatStatus
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'