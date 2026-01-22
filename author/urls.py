from django.urls import path
from .views import AuthorAPI

urlpatterns = [
    path('', AuthorAPI.as_view())

]