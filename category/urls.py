from django.urls import path
from .views import CategoryAPI

urlpatterns = [
    path('category', CategoryAPI.as_view())

]