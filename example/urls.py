# example/urls.py
from django.urls import path

from example.views import index, get_user_input, process_input, result


urlpatterns = [
    # path('', index),
    path('', get_user_input),
    path('api/process_input', process_input, name='process_input'),
    path('result/', result, name='result'),
]
