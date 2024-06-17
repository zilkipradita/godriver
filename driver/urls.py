from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
     path("", views.index, name="index"),
     path("create_user", views.create_user, name="create_user"),
     path("login", views.login, name="login"),
     path("create_trips", views.create_trips, name="create_trips"),
     path("show_trips", views.show_trips, name="show_trips"),
     path("delete_trips/<int:id>/<int:user>/", views.delete_trips, name="delete_trips"),
     path("takes_order", views.takes_order, name="takes_order"),
     path("trips_status/<int:id>/", views.trips_status, name="trips_status"),
     path("order_done/<int:id>/<int:driver>/", views.order_done, name="order_done"),
     path("order_canceled/<int:id>/<int:driver>/", views.order_canceled, name="order_canceled"),
]
