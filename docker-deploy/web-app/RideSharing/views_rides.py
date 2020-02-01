from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RideForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Ride, vehicle


class RideRequestView(CreateView, LoginRequiredMixin):
    model = Ride
    form_class = RideForm

    def form_valid(self, form):
        form.instance.status = Ride.OPEN
        form.instance.owner = self.request.user
        form.instance.psg_count = form.instance.owner_count
        fs = form.save()
        fs.psg.add(self.request.user)
        fs.save()
        return redirect(form.instance.get_absolute_url())


class RideDetailView(DetailView):
    model = Ride

    def get_context_data(self, **kwargs):
        context = super(RideDetailView, self).get_context_data(**kwargs)
        context['vehicle'] = vehicle.objects.filter(driver=self.object.driver)
        return context


class RideListView(ListView):
    model = Ride

    # <app>/<model>_<viewtype>.html
    def get_context_data(self, **kwargs):
        context = super(RideListView, self).get_context_data(**kwargs)
        context['rides'] = Ride.objects.filter(psg=self.request.user).order_by('-arrival_daytime')
        return context


class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['dest', 'owner_count', 'arrival_daytime', 'is_shared', 'vehicle_type', 'special_request']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.owner:
            return True
        return False
