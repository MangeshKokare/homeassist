from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('resident', 'Resident'),
    ('provider', 'Service Provider'),
)


BOOKING_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
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
        
    VERIFICATION_STATUS = (
        ('pending','Pending'),
        ('verified','Verified'),
        ('rejected','Rejected'),
    )

    aadhaar_number = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )

    aadhaar_image = models.ImageField(
        upload_to='verification/aadhaar/',
        blank=True,
        null=True
    )

    pan_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    pan_image = models.ImageField(
        upload_to='verification/pan/',
        blank=True,
        null=True
    )

    # Professional Information
    business_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    about_me = models.TextField(
        blank=True,
        null=True
    )

    # Personal Information
    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    # Service Area
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    service_radius = models.PositiveIntegerField(
        default=10,
        help_text="Radius in KM"
    )

    # Availability
    working_days = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    emergency_available = models.BooleanField(
        default=False
    )

    # Pricing
    starting_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Social Links
    website = models.URLField(
        blank=True,
        null=True
    )

    instagram_url = models.URLField(
        blank=True,
        null=True
    )

    facebook_url = models.URLField(
        blank=True,
        null=True
    )

    linkedin_url = models.URLField(
        blank=True,
        null=True
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='pending'
    )
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)

    service_name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=100
    )

    # NEW FIELD
    subcategory = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    description = models.TextField()

    price = models.IntegerField()

    image = models.ImageField(
        upload_to='services/'
    )

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

    start_otp = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    complete_otp = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    started_at = models.DateTimeField(
        blank=True,
        null=True
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    cancelled_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cancelled_bookings'
    )

    cancellation_reason = models.TextField(
        blank=True,
        null=True
    )

    cancelled_at = models.DateTimeField(
        blank=True,
        null=True
    )
    def __str__(self):
        return self.service.service_name


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    
class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
class Review(models.Model):

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )

    resident = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )

    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )

    rating = models.IntegerField()

    review = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.provider.username} - {self.rating}"
    

class BookingTimeline(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

class FavoriteProvider(models.Model):

    resident = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_providers'
    )

    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'resident',
            'provider'
        )