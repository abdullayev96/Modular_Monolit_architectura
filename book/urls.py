from django.urls import path
from .views import *

urlpatterns = [
    path('book', BookListAPI.as_view())

]