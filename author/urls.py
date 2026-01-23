from django.urls import path
from .views import AuthorAPI

urlpatterns = [
    path('authors', AuthorAPI.as_view())

]