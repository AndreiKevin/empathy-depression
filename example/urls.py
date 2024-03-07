# example/urls.py
from django.urls import path

from example.views import index, result


urlpatterns = [
    # path('', index),
    path('', index),
    path('result/', result, name='result'),
]
