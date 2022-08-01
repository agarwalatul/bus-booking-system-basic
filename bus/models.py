from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BusTypes(models.TextChoices):
    SLEEPER = 'SLEEPER', _('SLEEPER')
    SEMI_SLEEPER = 'SEMI_SLEEPER', _('SEMI_SLEEPER')
    SEATER = 'SEATER', _('SEATER')


class Bus(BaseModel):
    bus_name = models.CharField(max_length=128, null=False, blank=True)
    bus_type = models.CharField(max_length=32, choices=BusTypes.choices, default=BusTypes.SEATER)
    is_air_conditioned = models.BooleanField(default=False)


class SeatTier(models.TextChoices):
    LOW = 'LOW', _('LOW')
    MIDDLE = 'MIDDLE', _('MIDDLE')
    HIGH = 'HIGH', _('HIGH')


class Seat(BaseModel):
    seat_number = models.IntegerField(null=False, blank=False)
    seat_tier = models.CharField(max_length=16, choices=SeatTier.choices, default=SeatTier.LOW)
    bus = models.ForeignKey(Bus, related_name='seats', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['seat_number', 'bus']
