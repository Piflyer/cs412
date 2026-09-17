# Author: Tim Nguyen (tim7@bu.edu), 9/17/2026
# Description: set redirect paths to render proper pages for restraunts

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('/main', views.main, name="main"),
    path('/order', views.order, name="orders"),
    path('/confirmation', views.confirmation, name="confirmation"),
]
