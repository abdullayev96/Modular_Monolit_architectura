from django.urls import path
from .views import *


urlpatterns = [
          path("register/", RegisterAPI.as_view()),
          path("login/", LoginAPI.as_view()),


]