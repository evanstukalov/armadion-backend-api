from django.contrib import admin
from django.urls import path, include
from contactform.views import contact_form

urlpatterns = [
    path('', contact_form, name='contact_form')
]