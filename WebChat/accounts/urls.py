from django.urls import path
from . import views


urlpatterns = [
    path('csrf', views.CSRFTokenView.as_view()),
    path('otp', views.OtpView.as_view()),
    path('register', views.RegisterView.as_view()),
]