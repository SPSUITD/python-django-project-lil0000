from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('accounts/login/', LoginView.as_view(), name='login'),
  path('registration/', views.registration_view, name='registration'),
  path('logout/', LogoutView.as_view(), name='logout'),

  path('send/', views.create_message, name='send_message'),
  path('dialog/<int:pk>', views.get_dialog, name='dialog'),
]
