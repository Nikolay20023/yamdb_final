from django.urls import path
from . views import RegistrationClass, AuthenticatedClass

urlpatterns = [
    path('v1/auth/signup/', RegistrationClass.as_view()),
    path('v1/auth/token/', AuthenticatedClass.as_view()),
]
