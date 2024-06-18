from django.contrib import admin
from django.urls import path, re_path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

schema_view = get_schema_view(
    openapi.Info(
        title="goDriver API",
        default_version='v1',
        contact=openapi.Contact(email="mr.zilkipradita@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
     path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
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
