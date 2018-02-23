from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html'), name='root'),
    path('home/', views.home, name='home'),
    path('base/', TemplateView.as_view(template_name='base.html'), name='base'),
    path('grant/', views.add_model, name='grant'),
]
