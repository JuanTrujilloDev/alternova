"""
Films routing configuration file
"""

from django.urls import path
import users.views as views

urlpatterns = [
   path("login/", views.APILoginView.as_view(template_name = "users/login.html"), name="login"),
   path("logout/", views.APILogoutView.as_view(), name="logout"),
]
