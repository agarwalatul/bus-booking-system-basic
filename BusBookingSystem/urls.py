"""BusBookingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from booking_system import views as booking_system_views
from bus import views as bus_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trips/', booking_system_views.TripList.as_view()),
    path('trips/<int:pk>/', booking_system_views.TripDetail.as_view()),
    path('users/', user_views.UserList.as_view()),
    path('users/<int:pk>/', user_views.UserDetail.as_view()),
    path('bus/', bus_views.BusList.as_view()),
    path('bus/<int:pk>/', bus_views.BusDetail.as_view()),
    path('tickets/', booking_system_views.TicketList.as_view()),
]
