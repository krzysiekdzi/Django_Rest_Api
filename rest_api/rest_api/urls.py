from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.shortcuts import redirect

from rest_api.main.views import (
    cars_request_router,
    delete_car_endpoint,
    insert_car_rate_endpoint,
    fetch_popular_cars_endpoint)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^cars/?$', cars_request_router),
    url(r'^cars/(?P<car_id>[\w]+)/?$', delete_car_endpoint),
    url(r'^rate/?$', insert_car_rate_endpoint),
    url(r'^popular/?$', fetch_popular_cars_endpoint),
]
