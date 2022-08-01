import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from bus.models import Bus, Seat
from user.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, db_index=True)
    pincode = models.CharField(max_length=16, unique=True)
    state = models.CharField(max_length=128, null=False, blank=False)
    country = models.CharField(max_length=128, null=False, blank=True)


class Trip(BaseModel):
    origination_city = models.ForeignKey(City, related_name='trips', on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, related_name='trips', on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)


class BookingStatus(models.TextChoices):
    BOOKED = 'BOOKED', _('BOOKED')
    AVAILABLE = 'AVAILABLE', _('AVAILABLE')


class TripSeatStatus(BaseModel):
    trip = models.ForeignKey(Trip, related_name='trip_seat_status', on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=BookingStatus.choices, default=BookingStatus.AVAILABLE)

    class Meta:
        index_together = [['trip', 'status']]


class Ticket(BaseModel):
    ticket_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, db_index=True, on_delete=models.DO_NOTHING)
    trip = models.ForeignKey(Trip, db_index=True, on_delete=models.RESTRICT)
    seat = models.ForeignKey(Seat, on_delete=models.RESTRICT)

    class Meta:
        unique_together = ['user', 'trip', 'seat']
