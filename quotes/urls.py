# Author: Tim Nguyen (tim7@bu.edu), 9/16/2026
# Description: set redirect paths to render proper pages

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

#URL patterns for quotes
urlpatterns = [
    path('', views.quote, name="quote_landing"),
    path('quote', views.quote, name="quote"),
    path('show_all', views.show_all, name="show_all"),
    path('about', views.about, name="about"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)