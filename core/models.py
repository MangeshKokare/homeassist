from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('resident', 'Resident'),
    ('provider', 'Service Provider'),
)


BOOKING_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('completed', 'Completed'),
)

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    working_start_time = models.TimeField(
        null=True,
        blank=True
    )

    working_end_time = models.TimeField(
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.service_name


class Booking(models.Model):
    resident = models.ForeignKey(User, related_name='resident_bookings', on_delete=models.CASCADE)
    provider = models.ForeignKey(User, related_name='provider_bookings', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    booking_date = models.DateField()
    booking_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service.service_name


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username