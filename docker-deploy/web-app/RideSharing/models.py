from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class my_user(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class vehicle(models.Model):
    CATEGORY = (
        ('Compact', 'Compact'),
        ('Luxury', 'Luxury'),
        ('SUV', 'SUV'),
        ('Sport', 'Sport'),
    )
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=False,
                               on_delete=models.SET_NULL)  # settings.AUTH_USER_MODEL
    plate_num = models.CharField(max_length=150)
    capacity = models.IntegerField()
    type = models.CharField(max_length=150, choices=CATEGORY, default='Compact')
    special_request = models.CharField(blank=True, null=True, max_length=150)

    def get_absolute_url(self):
        return reverse('driver_detail')

    def __str__(self):
        return str(self.capacity) + ' ' + str(self.driver)


# UUID!

class Ride(models.Model):
    """
    1. Required fields.
    Use automatically added field id as ride_id.
    For RideStatus
    """
    OPEN = 0
    OPEN_WITH_SHARER = 1
    CONFIRMED = 2
    COMPLETE = 3
    RIDES_STATUS = [
        (OPEN, 'Wait for Driver to confirm'),
        (OPEN_WITH_SHARER, 'Sharer Joined'),
        (CONFIRMED, 'Confirmed by Driver'),
        (COMPLETE, 'Complete'),
    ]
    status = models.IntegerField(default=OPEN, choices=RIDES_STATUS)
    owner = models.ForeignKey(my_user, default=None, related_name="owner", on_delete=models.DO_NOTHING)
    owner_count = models.IntegerField(default=0, verbose_name="Number of Passengers in your party")
    is_shared = models.BooleanField(default=True, verbose_name="Share with others")
    # Include owner, driver, sharers.
    psg = models.ManyToManyField(my_user, default=1, related_name="psg")
    psg_count = models.IntegerField(default=0, verbose_name="Number of all passengers")
    dest = models.CharField(default=None, verbose_name="Destination", max_length=150)
    arrival_daytime = models.DateTimeField(default=timezone.now, verbose_name="Arrival Time")
    """
    2. Optional Fields.
    driver, type, special_request, sharer_id, sharer_num, 
    """
    driver = models.ForeignKey(my_user,
                               blank=True,
                               related_name="driver", null=True,
                               on_delete=models.SET_NULL,
                               verbose_name="Driver")
    sharer_info = JSONField(blank=True, null=True)
    """
    3. Optional
    """
    CATEGORY = (
        ('Compact', 'Compact'),
        ('Luxury', 'Luxury'),
        ('SUV', 'SUV'),
        ('Sport', 'Sport'),
    )
    vehicle_type = models.CharField(max_length=150, choices=CATEGORY, default='Compact',
                                    verbose_name="Expected Vehicle Type")
    special_request = models.CharField(blank=True, null=True, max_length=150, verbose_name="Any Special Request")

    def __str__(self):
        return self.owner.email + ' ' + self.dest + ' ' + self.arrival_daytime.strftime("%m/%d/%Y, %H:%M:%S")

    def get_absolute_url(self):
        return reverse('ride_detail', kwargs={'pk': self.pk})
