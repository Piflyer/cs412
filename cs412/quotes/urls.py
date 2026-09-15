from django.urls import path
from . import views

#URL patterns for quotes
urlpatterns = [
    path('', views.quote, name="quote_landing"),
    path('quote', views.quote, name="quote"),
    path('show_all', views.show_all, name="show_all"),
    path('about', views.about, name="about"),
]
