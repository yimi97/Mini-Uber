from django.urls import path
from . import views, views_rides
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user_register/', views.UserRegister, name="user_register"),
    path('ride_request/', views_rides.RideRequestView.as_view(), name="ride_request"),
    path('ride_list/', views_rides.RideListView.as_view(), name='ride_list'),
    path('ride_detail/<int:pk>/', views_rides.RideDetailView.as_view(), name='ride_detail'),
    path('ride_detail/<int:pk>/update/', views_rides.RideUpdateView.as_view(), name='ride_update'),
    path('login/', auth_views.LoginView.as_view(template_name='RideSharing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('driver_register/', views.DriverRegiseterView, name='driver_register'),
    path('driver_search/', views.DriverSearchView, name='driver_search'),
    path('driver_edit/', views.DriverEditView.as_view(), name='driver_edit'),
    path('driver_detail/', views.DriverDetailView.as_view(), name='driver_detail'),
    path('share_search/', views.ShareSearchView, name='sharer_search'),
]

