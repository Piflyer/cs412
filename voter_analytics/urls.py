# Author: Tim Nguyen (tim7@bu.edu), 10/30/2026
# Description: set paths for our voter app

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name="voters"),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs', views.GraphListView.as_view(), name="graphs"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)