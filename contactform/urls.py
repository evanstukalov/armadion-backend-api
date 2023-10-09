from django.contrib import admin
from django.urls import path, include
from contactform.views import contact_form

app_name = 'contactform'

urlpatterns = [
    path('', contact_form, name='contact-form')
]