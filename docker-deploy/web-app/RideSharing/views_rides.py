from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RideForm, RideSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.db.models import Q
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
    
    form = RideSearchForm()
    template_name = "RideSharing/ride_list.html"
    paginate_by = 5
    

    def get_queryset(self):
    
        role = self.request.GET.get('role', 'give-default-value')
        status = self.request.GET.get('status', 'give-default-value')
        print(self.request.GET)
        print(status[0])
        queryFilter = Q()
        queryFilter.add(Q(psg=self.request.user), Q.AND)
        if status[0] == str(RideSearchForm.STATUS_CHOICE[1][0]):  
            queryFilter.add(Q(status=Ride.COMPLETE), Q.AND)
        else:
            queryFilter.add(~Q(status=Ride.COMPLETE), Q.AND)
        if role[0] == str(RideSearchForm.ROLE_CHOICE[1][0]):
            queryFilter.add(Q(owner=self.request.user), Q.AND)
        if role[0] == str(RideSearchForm.ROLE_CHOICE[2][0]):
            queryFilter.add(Q(driver=self.request.user), Q.AND)
        if role[0] == str(RideSearchForm.ROLE_CHOICE[3][0]):
            queryFilter.add(~Q(owner=self.request.user), Q.AND)
            queryFilter.add(~Q(driver=self.request.user), Q.AND)

        return Ride.objects.filter(queryFilter).order_by('-arrival_daytime')

    # <app>/<model>_<viewtype>.html
    def get_context_data(self, form=form, **kwargs):
        form = RideSearchForm(self.request.GET or None)
        context = super(RideListView, self).get_context_data(**kwargs)
        context['form'] = form;

        return context




class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    form_class = RideForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.owner:
            return True
        return False

def ride_complete(request, ride_id):
    ride_to_complete = Ride.objects.filter(id=ride_id)
    for r in ride_to_complete:
        r.status = Ride.COMPLETE
        r.save()
    return redirect('ride_list')