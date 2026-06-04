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

    CATEGORY_CHOICES = [
        ('Cleaning', '🧹 Cleaning'),
        ('Electrician', '⚡ Electrician'),
        ('Plumber', '🚰 Plumbing'),
        ('Appliance', '🛠 Appliance Repair'),
        ('Carpenter', '🪚 Carpenter'),
        ('Pest Control', '🐜 Pest Control'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full bg-surface-container-low border border-outline-variant rounded-xl px-md py-sm text-body-md text-on-surface focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent'
        })
    )

    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['provider']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time']
        # DO NOT include 'resident', 'provider', 'service' — set in the view



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']