# Author: Tim Nguyen (tim7@bu.edu), 9/17/2026
# Description: set redirect paths to render proper pages for restraunts

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main, name="home"),
    path('main', views.main, name="main"),
    path('order', views.order, name="orders"),
    path('confirmation', views.confirmation, name="confirmation"),
    path('submit', views.submit, name="submit")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)