from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from .views import SignupView

app_name = 'mainapp'
urlpatterns = [
    path('', TemplateView.as_view(template_name='mainapp/base.html'), name='base'),
    path('clients/create/', SignupView.as_view(), name='sign-up'),
]
