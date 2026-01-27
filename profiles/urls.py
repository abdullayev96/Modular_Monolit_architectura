from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
          # path('balance/', UserBalanceAPI.as_view())
]

router.register('', ProfileAPI, basename='profile'),


urlpatterns += router.urls