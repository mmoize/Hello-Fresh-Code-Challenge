from django.urls import path
from .views import RegistrationAPIView, LoginApIView

app_name = 'authentication'

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name="signup"),
    path('login/', LoginApIView.as_view(), name="login"),
]
