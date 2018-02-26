from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('base/', TemplateView.as_view(template_name='base.html'), name='base'),
]
