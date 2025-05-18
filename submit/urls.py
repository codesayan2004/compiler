from django.urls import path
from .views import submit_code

urlpatterns = [
    path('', submit_code),  # Include the URLs from the submit app
]