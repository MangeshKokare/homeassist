from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Profile, Service, Booking, Message


# =========================
# PROFILE INLINE
# =========================
class ProfileInline(admin.StackedInline):

    model = Profile
    can_delete = False

    fields = (
        'role',
        'phone',
        'address',
        'profile_image'
    )


# =========================
# CUSTOM USER ADMIN
# =========================
class CustomUserAdmin(UserAdmin):

    inlines = (ProfileInline,)


# Remove Default User Admin
admin.site.unregister(User)

# Register Custom User Admin
admin.site.register(User, CustomUserAdmin)


# =========================
# OTHER MODELS
# =========================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        'service_name',
        'provider',
        'category',
        'price'
    )

    search_fields = (
        'service_name',
        'category'
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'resident',
        'provider',
        'service',
        'status',
        'booking_date'
    )

    list_filter = (
        'status',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        'sender',
        'receiver',
        'timestamp'
    )


# Optional Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
        'phone'
    )

    list_filter = (
        'role',
    )