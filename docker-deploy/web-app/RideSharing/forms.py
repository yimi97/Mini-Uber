from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import my_user, vehicle, Ride
from django.views.generic.edit import FormView
from django.utils import timezone
import datetime
from flatpickr import DateTimePickerInput


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = my_user
        fields = [
            'email',
            'username',
        ]


class DriverRegisterForm(forms.ModelForm):
    class Meta:
        model = vehicle
        fields = ['driver', 'realname', 'plate_num', 'capacity', 'type', 'special_request']
        exclude = ['driver', ]


class ShareSearchForm(forms.Form):
    dest = forms.CharField(max_length=150, label="Destination")
    num = forms.IntegerField(initial=1, label="Number of passengers (including yourself)")
    start_datetime = forms.DateTimeField(widget=DateTimePickerInput(), initial=timezone.now,
                                         label="Expected Earliest Arrival Time")
    end_datetime = forms.DateTimeField(widget=DateTimePickerInput(), initial=timezone.now,
                                       label="And the Latest time you accept")

    def clean_start_datetime(self):
        start_datetime = self.cleaned_data.get('start_datetime')
        print(start_datetime)
        if start_datetime < timezone.now():
            raise forms.ValidationError("Sorry, the start time passed already.")

        return start_datetime

    def clean_end_datetime(self):
        start_datetime = self.cleaned_data.get('start_datetime')
        end_datetime = self.cleaned_data.get('end_datetime')

        if not start_datetime or start_datetime > end_datetime:
            raise forms.ValidationError("Please check the range is valid.")

        return end_datetime


class RideForm(forms.ModelForm):
    owner_count = forms.IntegerField(initial=1)

    class Meta:
        model = Ride
        fields = ['dest', 'owner_count', 'arrival_daytime', 'is_shared', 'vehicle_type', 'special_request']
        widgets = {
            'arrival_daytime': DateTimePickerInput(),
        }

class RideSearchForm(forms.Form):
    ROLE_CHOICE = (
        (0, 'All'),
        (1, 'Owner'),
        (2, 'Driver'),
        (3, 'Sharer')
    )
    STATUS_CHOICE = (
        (0, 'Non-Complete'),
        (1, 'Complete')
    )
    role = forms.ChoiceField(choices=ROLE_CHOICE, label="Role", initial=ROLE_CHOICE[0])
    status = forms.ChoiceField(choices=STATUS_CHOICE, label="Ride Status", initial=STATUS_CHOICE[0])
