from django.urls import path
from waitingdeploy.views import *

urlpatterns = [
    path('', comingsoon, name="comingsoon"),
]
