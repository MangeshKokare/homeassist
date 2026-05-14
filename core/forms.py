from django import forms
from django.contrib.auth.models import User
from .models import Profile, Service, Booking, Message

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'category', 'description', 'price', 'image']
        # DO NOT include 'provider' — it's set automatically in the view

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time']
        # DO NOT include 'resident', 'provider', 'service' — set in the view



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']