from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import my_user, vehicle, Ride
from django.views.generic.edit import FormView
from django.utils import timezone
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
        fields = ['driver', 'plate_num', 'capacity', 'type', 'special_request']
        exclude = ['driver', ]
        '''
        class AuthorCreate(LoginRequiredMixin, CreateView):
        model = Author
        fields = ['name']
        def form_valid(self, form):
        form.instance.created_by(driver here) = self.request.user
        return super().form_valid(form)
        '''


class DriverSearchForm(forms.Form):
    dest = forms.CharField(max_length=150, label="Destination")


class ShareSearchForm(forms.Form):
    dest = forms.CharField(max_length=150, label="Destination")
    num = forms.IntegerField(initial=1, label="Number of passengers")
    start_datetime = forms.DateTimeField(widget=DateTimePickerInput(), initial=timezone.now,
                                         label="Expected Earliest Arrival Time")
    end_datetime = forms.DateTimeField(widget=DateTimePickerInput(), initial=timezone.now,
                                       label="And the Latest time you accept")

    def clean_end_datetime(self):
        start_datetime = self.cleaned_data.get('start_datetime')
        end_datetime = self.cleaned_data.get('end_datetime')

        if start_datetime > end_datetime:
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
