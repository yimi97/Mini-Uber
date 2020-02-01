from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, DriverRegisterForm, DriverSearchForm, ShareSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import my_user, vehicle, Ride
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


def UserRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            # messages.info(request, f"Welcome, {username}")
            return redirect("ride_list")
    else:
        form = UserRegisterForm()
    return render(request, 'RideSharing/user_register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'RideSharing/dashboard.html', {})


@login_required
def DriverRegiseterView(request):
    if not vehicle.objects.filter(driver=request.user).exists():
        if request.method == 'POST':
            form = DriverRegisterForm(request.POST)  # request.user.id,
            if form.is_valid():
                fs = form.save()
                fs.driver = request.user
                fs.save()
                return redirect('driver_detail')
        else:
            form = DriverRegisterForm()
        return render(request, 'RideSharing/driver_register.html', {'form': form})
    else:
        return redirect('driver_detail')


# Inside views


class DriverDetailView(DetailView, LoginRequiredMixin):
    form_class = DriverRegisterForm
    template_name = 'RideSharing/driver_detail.html'

    def get_object(self):
        return get_object_or_404(vehicle, driver=self.request.user)


class DriverEditView(UpdateView, LoginRequiredMixin):
    form_class = DriverRegisterForm
    template_name = 'RideSharing/driver_edit.html'

    def get_object(self):
        return get_object_or_404(vehicle, driver=self.request.user)


def cal_cap(ride):
    for r in ride:
        num = r.owner_count
        for key, value in r.sharer_info:
            num += value
        r['num_psg'] = num
    return r


@login_required
def DriverSearchView(request):
    if not vehicle.objects.filter(driver=request.user).exists():
        return redirect('driver_register')
    form = DriverSearchForm()
    driver = get_object_or_404(vehicle, driver=request.user)
    ride = []
    model = Ride

    if request.method == 'POST':
        if 'confirm' in request.POST:
            if 'choose' in request.POST:
                ride_chosen = Ride.objects.filter(id=request.POST['choose'])
                # add driver, update status
                ride_chosen.update(driver=request.user, status=2)
                # add psg
                for r in ride_chosen:
                    r.psg.add(request.user)
                    # send email to r.sharer r.owner
                    r.save()
                    send_confirm_email(r)
                return redirect('ride_list')
            else:
                return redirect('driver_search')

        ride = Ride.objects.filter(Q(vehicle_type=driver.type),
                                   Q(psg_count__lte=driver.capacity),
                                   (Q(special_request=None) | Q(special_request=driver.special_request)),
                                   Q(status__range=(0, 1))
                                   ).exclude(psg=request.user)
        if not ride.exists():
            messages.info(request, 'Sorry, no matches. Please try again.')

    context = {'form': form, 'ride': ride}
    return render(request, 'RideSharing/driver_search.html', context)


sharer_num = 0


def ShareSearchView(request):
    form = ShareSearchForm()
    ride = []
    model = Ride

    if request.method == 'POST':
        form = ShareSearchForm(request.POST or None)
        if 'search' in request.POST:
            if form.is_valid():
                obj = form.cleaned_data
                ride = Ride.objects.filter(dest=obj.get('dest'),
                                           arrival_daytime__range=(obj.get('start_datetime'),
                                                                   obj.get('end_datetime')),
                                           status__range=(0, 1)).exclude(psg=request.user)
                global sharer_num
                sharer_num = obj.get('num')
                if not ride.exists():
                    messages.info(request, 'Sorry, no matches T^T')
        if 'confirm' in request.POST:
            if 'choose' in request.POST:
                ride_chosen = Ride.objects.filter(id=request.POST['choose'])
                for r in ride_chosen:
                    # add psg
                    form.is_valid()
                    if r.sharer_info is None:
                        r.sharer_info = {}
                    r.sharer_info[request.user.get_username()] = sharer_num
                    r.psg.add(request.user)
                    r.save()
                    if r.psg_count is None:
                        r.psg_count = 0
                    r.psg_count = r.psg_count + sharer_num
                return redirect('ride_list')
            else:
                return redirect('sharer_search')

    context = {'form': form, 'ride': ride}
    return render(request, 'RideSharing/sharer_search.html', context)


def send_confirm_email(r):
    subject = 'Your order to ' + str(r.dest) + ' is confirm.'
    message = 'Thank you you choosing Yi & Yueying \'s RideSharing App.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [r.owner.email]
    if r.sharer_info is not None:
        for key, value in r.sharer_info:
            recipient_list.append(key)
    send_mail(subject, message, email_from, recipient_list)


'''
class RideDisplay(ListView, SingleObjectMixin):
    model = Ride
    fields = ['dest', 'owner_count', 'arrival_daytime', 'is_shared', 'vehicle_type', 'special_request']
    template_name = 'RideSharing/driver_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['form'] = SearchForm()

        context['rides'] = Ride.objects.filter(psg=self.request.user).order_by('-arrival_daytime')
        return context
#form = SearchForm(request.GET, request.FILES)

class Search(SingleObjectMixin, FormView):
    template_name = 'RideSharing/driver_result.html'
    form_class = SearchForm
    model = Ride

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('driver_result')
     
'''

'''
class Driver(ListView):
    form = SearchForm()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = SearchForm(request.GET)
        if form.is_valid():
            obj = form.cleaned_data
            ride = Ride.objects.get_queryset(status=1 or 2,
                                       dest=obj.get('dest'),
                                       arrival_daytime=obj.get('arrival_daytime'))  # capacity
            if not ride.exists():
                messages.info(request, 'Sorry, no matches. Please try again.')
                form = DriverSearchForm()

        #if request.GET.get('Search'):
        self.object_list = self.get
        return super().get(request)


    def post(self, request):

'''
