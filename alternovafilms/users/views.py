from typing import Any
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
class APILoginView(LoginView):
    """
    Login view
    """
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get(self, request, *args: Any, **kwargs: Any):
        
        if self.request.user.is_authenticated:
            return redirect(reverse("home"))
        return super().get(request, *args, **kwargs)
    
class APILogoutView(LogoutView):
    """
    Logout view
    """
    next_page = "home"
    
    def get(self, request, *args: Any, **kwargs: Any):
        if self.request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return redirect(reverse("home"))