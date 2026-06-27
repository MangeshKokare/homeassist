from .chatbot import get_bot_reply
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib import messages
from django.db.models import Avg
from .models import (
    Service,
    Booking,
    Message,
    Notification,
    Review,
    FavoriteProvider,
)
from .forms import ServiceForm, BookingForm
from datetime import datetime
import random

# =========================
# RESIDENT HOME
# =========================
@login_required
def resident_home(request):
    if request.user.profile.role != 'resident':
        messages.error(request, 'Access denied. Residents only.')
        return redirect('provider_dashboard')

    search_query = request.GET.get('search')
    services = Service.objects.all().order_by('-id')

    if search_query:
        services = services.filter(service_name__icontains=search_query)

    return render(request, 'residents/resident_home.html', {
        'services': services,
        'search_query': search_query,
    })



@login_required
def explore_services(request):

    search_query = request.GET.get('search', '')
    active_category = request.GET.get('category', '')
    active_sub = request.GET.get('sub', '')

    services = Service.objects.select_related(
        'provider',
        'provider__profile'
    ).all()

    if search_query:
        services = services.filter(
            Q(service_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(provider__first_name__icontains=search_query) |
            Q(provider__last_name__icontains=search_query)
        )

    if active_category:
        services = services.filter(
            category__iexact=active_category
        )

    # Optional: filter by subcategory (after you add a subcategory field)
    if active_sub:
        services = services.filter(
            subcategory__iexact=active_sub
        )

    categories = [
        "Cleaning",
        "Electrician",
        "Plumber",
        "Painter",
        "Carpenter",
        "Waterproofing",
    ]

    context = {
        'services': services,
        'search_query': search_query,
        'active_category': active_category,
        'active_sub': active_sub,
        'categories': categories,
    }
    favorite_providers = []

    if request.user.is_authenticated:

        favorite_providers = list(
            FavoriteProvider.objects.filter(
                resident=request.user
            ).values_list(
                'provider_id',
                flat=True
            )
        )
    return render(
        request,
        'residents/explore_services.html',
        {
            'services': services,
            'categories': categories,
            'active_category': active_category,
            'active_sub': active_sub,
            'search_query': search_query,
            'favorite_providers': favorite_providers,
        }
    )

@login_required
def resident_bookings(request):

    if request.user.profile.role != 'resident':
        messages.error(request, 'Access denied. Residents only.')
        return redirect('provider_dashboard')

    all_bookings = Booking.objects.filter(
        resident=request.user
    ).select_related(
        'provider',
        'service'
    ).order_by('-id')

    active_status = request.GET.get('status', 'all')

    if active_status == 'all':
        bookings = all_bookings

    elif active_status in [
        'pending',
        'accepted',
        'in_progress',
        'completed',
        'cancelled'
    ]:
        bookings = all_bookings.filter(
            status=active_status
        )

    else:
        bookings = all_bookings
        active_status = 'all'

    context = {
        'bookings': bookings,
        'active_status': active_status,

        'pending_count': all_bookings.filter(
            status='pending'
        ).count(),

        'accepted_count': all_bookings.filter(
            status='accepted'
        ).count(),

        'completed_count': all_bookings.filter(
            status='completed'
        ).count(),

        'cancelled_count': all_bookings.filter(
            status='cancelled'
        ).count(),

        'total_count': all_bookings.count(),
        'in_progress_count':
        all_bookings.filter(
            status='in_progress'
        ).count(),
    }

    return render(
        request,
        'residents/manage_bookings.html',
        context
    )


@login_required
def resident_messages(request):

    if request.user.profile.role != 'resident':
        messages.error(request, 'Access denied. Residents only.')
        return redirect('provider_dashboard')

    from .models import Message as Msg

    sent_to = Msg.objects.filter(
        sender=request.user
    ).values_list(
        'receiver',
        flat=True
    ).distinct()

    received_from = Msg.objects.filter(
        receiver=request.user
    ).values_list(
        'sender',
        flat=True
    ).distinct()

    contact_ids = set(
        list(sent_to) + list(received_from)
    )

    conversations = []

    for uid in contact_ids:

        other_user = User.objects.get(id=uid)

        last_message = Msg.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).order_by('-timestamp').first()

        conversations.append({
            'other_user': other_user,
            'last_message': last_message,
        })

    conversations.sort(
        key=lambda x: x['last_message'].timestamp,
        reverse=True
    )

    return render(
        request,
        'residents/messages.html',
        {
            'conversations': conversations,
        }
    )

@login_required
def resident_profile(request):

    if request.user.profile.role != 'resident':
        messages.error(request, 'Access denied. Residents only.')
        return redirect('provider_dashboard')

    user = request.user

    all_bookings = Booking.objects.filter(
        resident=user
    )

    active_bookings = all_bookings.filter(
        status__in=['pending', 'accepted']
    ).count()

    completed_bookings = all_bookings.filter(
        status='completed'
    ).count()

    total_messages = Message.objects.filter(
        Q(sender=user) |
        Q(receiver=user)
    ).count()

    context = {
        'user_obj': user,
        'profile': user.profile,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'total_messages': total_messages,
    }

    return render(
        request,
        'residents/profile.html',
        context
    )


# =========================
# RESIDENT EDIT PROFILE
# =========================
@login_required
def resident_edit_profile(request):

    if request.user.profile.role != 'resident':
        messages.error(request, 'Access denied.')
        return redirect('provider_dashboard')

    user = request.user
    profile = user.profile

    if request.method == 'POST':

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        user.save()

        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()

        messages.success(request, 'Profile updated successfully.')

        return redirect('resident_profile')

    return render(
        request,
        'residents/edit_profile.html',
        {
            'user_obj': user,
            'profile': profile,
        }
    )


# =========================
# PROVIDER DASHBOARD
# =========================
@login_required
def provider_dashboard(request):
    if request.user.profile.role != 'provider':
        messages.error(request, 'Access denied. Providers only.')
        return redirect('resident_home')

    all_bookings = Booking.objects.filter(provider=request.user)

    return render(request, 'services/provider_dashboard.html', {
        'services': Service.objects.filter(provider=request.user),
        'recent_bookings': all_bookings.order_by('-created_at')[:5],
        'pending_count': all_bookings.filter(status='pending').count(),
        'accepted_count': all_bookings.filter(status='accepted').count(),
        'completed_count': all_bookings.filter(status='completed').count(),
    })


# =========================
# ADD SERVICE
# =========================
@login_required
def add_service(request):
    if request.user.profile.role != 'provider':
        messages.error(request, 'Only providers can add services.')
        return redirect('resident_home')

    form = ServiceForm()

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, 'Service added successfully.')
            return redirect('provider_dashboard')

    return render(request, 'services/add_service.html', {'form': form})


# =========================
# EDIT SERVICE
# =========================
@login_required
def edit_service(request, id):
    service = get_object_or_404(Service, id=id, provider=request.user)

    if request.user.profile.role != 'provider':
        messages.error(request, 'Only providers can edit services.')
        return redirect('resident_home')

    form = ServiceForm(instance=service)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('provider_dashboard')

    return render(request, 'services/edit_service.html', {
        'form': form,
        'service': service,
    })


# =========================
# DELETE SERVICE
# =========================
@login_required
def delete_service(request, id):
    service = get_object_or_404(Service, id=id, provider=request.user)

    if request.user.profile.role != 'provider':
        messages.error(request, 'Only providers can delete services.')
        return redirect('resident_home')

    service.delete()
    messages.success(request, 'Service deleted successfully.')
    return redirect('provider_dashboard')


# =========================
# PROVIDER BOOKINGS
# =========================
@login_required
def provider_bookings(request):
    if request.user.profile.role != 'provider':
        messages.error(request, 'Access denied. Providers only.')
        return redirect('resident_home')

    all_bookings = Booking.objects.filter(provider=request.user)
    active_status = request.GET.get('status', 'all')

    if active_status == 'all':
        bookings = all_bookings.order_by('-created_at')
    elif active_status in [
        'pending',
        'accepted',
        'in_progress',
        'completed',
        'cancelled'
    ]:
        bookings = all_bookings.filter(
            status=active_status
        ).order_by('-created_at')
    else:
        bookings = all_bookings.order_by('-created_at')
        active_status = 'all'

    return render(
        request,
        'services/provider_bookings.html',
        {
            'bookings': bookings,
            'active_status': active_status,

            'pending_count': all_bookings.filter(
                status='pending'
            ).count(),

            'accepted_count': all_bookings.filter(
                status='accepted'
            ).count(),
            'in_progress_count': all_bookings.filter(
                status='in_progress'
            ).count(),
            'completed_count': all_bookings.filter(
                status='completed'
            ).count(),

            'cancelled_count': all_bookings.filter(
                status='cancelled'
            ).count(),

            'total_count': all_bookings.count(),
        }
    )


def generate_otp():

    return str(
        random.randint(1000, 9999)
    )
# =========================
# UPDATE BOOKING STATUS
# =========================
@login_required
def update_booking_status(
    request,
    booking_id,
    new_status
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider=request.user
    )

    if new_status == "accepted":

        booking.status = "accepted"

        booking.start_otp = generate_otp()

        booking.save()

        Notification.objects.create(
            user=booking.resident,
            title='Booking Accepted',
            message='Your service provider has accepted the booking.'
        )

        Notification.objects.create(
            user=booking.resident,
            title='Service OTP Generated',
            message=f'Share OTP {booking.start_otp} when the provider arrives.'
        )
        Notification.objects.create(
            user=request.user,
            title='Booking Accepted',
            message=f'You accepted booking #{booking.id}.'
        )
        messages.success(
            request,
            "Booking accepted."
        )

    elif new_status == "cancelled":

        booking.status = "cancelled"

        booking.save()
        Notification.objects.create(
            user=booking.resident,
            title='Booking Rejected',
            message='The provider rejected your booking request.'
        )
        Notification.objects.create(
            user=request.user,
            title='Booking Rejected',
            message=f'You rejected booking #{booking.id}.'
        )
        messages.success(
            request,
            "Booking cancelled."
        )

    return redirect(
        "provider_bookings"
    )
from django.utils import timezone
@login_required
def verify_start_otp(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider=request.user
    )

    entered_otp = request.POST.get(
        "otp"
    )

    if entered_otp == booking.start_otp:

        booking.status = "in_progress"

        booking.started_at = timezone.now()

        booking.complete_otp = generate_otp()

        booking.save()
        Notification.objects.create(
            user=booking.resident,
            title='Service Started',
            message='The provider has started the service.'
        )

        Notification.objects.create(
            user=booking.resident,
            title='Completion OTP Generated',
            message=f'Completion OTP: {booking.complete_otp}'
        )
        Notification.objects.create(
            user=request.user,
            title='Service Started',
            message=f'Service for booking #{booking.id} is now in progress.'
        )
        messages.success(
            request,
            "Service started."
        )

    else:

        messages.error(
            request,
            "Invalid OTP."
        )

    return redirect(
        "provider_bookings"
    )

@login_required
def verify_complete_otp(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider=request.user
    )

    otp = request.POST.get(
        "otp"
    )

    if otp == booking.complete_otp:

        booking.status = "completed"

        booking.completed_at = timezone.now()

        booking.save()
        
        Notification.objects.create(
            user=booking.resident,
            title='Service Completed',
            message='Your booking has been completed successfully.'
        )
        Notification.objects.create(
            user=request.user,
            title='Service Completed',
            message=f'Booking #{booking.id} has been completed.'
        )
        messages.success(
            request,
            "Booking completed."
        )

    else:

        messages.error(
            request,
            "Invalid OTP."
        )

    return redirect(
        "provider_bookings"
    )
# =========================
# PROVIDER MESSAGES LIST
# =========================
@login_required
def provider_messages(request):
    if request.user.profile.role != 'provider':
        messages.error(request, 'Access denied. Providers only.')
        return redirect('resident_home')

    # Get all unique users the provider has exchanged messages with
    from .models import Message as Msg

    sent_to = Msg.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_from = Msg.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    contact_ids = set(list(sent_to) + list(received_from))

    conversations = []
    for uid in contact_ids:
        other_user = User.objects.get(id=uid)
        last_msg = Msg.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).order_by('-timestamp').first()

        conversations.append({
            'other_user': other_user,
            'last_message': last_msg,
            'unread_count': 0,  # Extend model for read tracking if needed
        })

    # Sort by most recent message
    conversations.sort(key=lambda x: x['last_message'].timestamp, reverse=True)

    return render(request, 'services/provider_messages.html', {
        'conversations': conversations,
    })

@login_required
def provider_notifications(request):

    notifications = request.user.notifications.all().order_by(
        '-created_at'
    )

    notifications.filter(
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        'services/provider_notifications.html',
        {
            'notifications': notifications
        }
    )
# =========================
# PROVIDER PROFILE
# =========================
@login_required
def provider_profile(request):
    if request.user.profile.role != 'provider':
        messages.error(request, 'Access denied. Providers only.')
        return redirect('resident_home')

    all_bookings = Booking.objects.filter(provider=request.user)
    reviews = Review.objects.filter(
        provider=request.user
    )

    avg_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    review_count = reviews.count()
    return render(
        request,
        'services/provider_profile.html',
        {
            'profile': request.user.profile,

            'services_count':
                Service.objects.filter(
                    provider=request.user
                ).count(),

            'total_bookings':
                all_bookings.count(),

            'completed_bookings':
                all_bookings.filter(
                    status='completed'
                ).count(),

            'pending_bookings':
                all_bookings.filter(
                    status='pending'
                ).count(),

            'avg_rating':
                avg_rating,

            'review_count':
                review_count,
        }
    )


# =========================
# EDIT PROFILE
# =========================
@login_required
def edit_profile(request):
    if request.user.profile.role != 'provider':
        messages.error(request, 'Access denied. Providers only.')
        return redirect('resident_home')

    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if email:
            user.email = email
        user.save()

        profile = user.profile
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if phone:
            profile.phone = phone

        if address:
            profile.address = address

        business_name = request.POST.get(
            'business_name',
            ''
        ).strip()

        if business_name:
            profile.business_name = business_name

        if request.POST.get('experience_years'):
            profile.experience_years = request.POST.get(
                'experience_years'
            )

        about_me = request.POST.get(
            'about_me',
            ''
        ).strip()

        if about_me:
            profile.about_me = about_me

        gender = request.POST.get(
            'gender',
            ''
        ).strip()

        if gender:
            profile.gender = gender

        date_of_birth = request.POST.get(
            'date_of_birth'
        )

        if date_of_birth:
            profile.date_of_birth = date_of_birth

        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if city:
            profile.city = city

        if state:
            profile.state = state

        if pincode:
            profile.pincode = pincode

        if request.POST.get('service_radius'):
            profile.service_radius = request.POST.get(
                'service_radius'
            )

        working_days = request.POST.get(
            'working_days',
            ''
        ).strip()

        if working_days:
            profile.working_days = working_days

        profile.emergency_available = (
            request.POST.get(
                'emergency_available'
            ) == 'on'
        )

        if request.POST.get('starting_price'):
            profile.starting_price = request.POST.get(
                'starting_price'
            )

        website = request.POST.get('website', '').strip()
        instagram = request.POST.get('instagram_url', '').strip()
        facebook = request.POST.get('facebook_url', '').strip()
        linkedin = request.POST.get('linkedin_url', '').strip()

        if website:
            profile.website = website

        if instagram:
            profile.instagram_url = instagram

        if facebook:
            profile.facebook_url = facebook

        if linkedin:
            profile.linkedin_url = linkedin
            
        working_start_time = request.POST.get(
            'working_start_time'
        )

        working_end_time = request.POST.get(
            'working_end_time'
        )

        if working_start_time:
            profile.working_start_time = working_start_time

        if working_end_time:
            profile.working_end_time = working_end_time
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        aadhaar = request.POST.get(
            'aadhaar_number',
            ''
        ).strip()

        pan = request.POST.get(
            'pan_number',
            ''
        ).strip()

        if aadhaar:
            profile.aadhaar_number = aadhaar

        if pan:
            profile.pan_number = pan

        if 'aadhaar_image' in request.FILES:
            profile.aadhaar_image = request.FILES[
                'aadhaar_image'
            ]

        if 'pan_image' in request.FILES:
            profile.pan_image = request.FILES[
                'pan_image'
            ]
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('provider_profile')

    return render(
        request,
        'services/edit_profile.html',
        {
            'profile': request.user.profile
        }
    )


# =========================
# PROVIDER DETAILS (for residents)
# =========================
from django.db.models import Avg

@login_required
def provider_details(request, id):

    service = get_object_or_404(
        Service,
        id=id
    )

    reviews = Review.objects.filter(
        provider=service.provider
    ).order_by('-created_at')

    avg_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    is_favorite = FavoriteProvider.objects.filter(
        resident=request.user,
        provider=service.provider
    ).exists()

    return render(
        request,
        'residents/provider_details.html',
        {
            'service': service,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'is_favorite': is_favorite,
        }
    )
# =========================
# BOOK SERVICE
# =========================
@login_required
def book_service(request, id):

    if request.user.profile.role != 'resident':
        messages.error(request, 'Only residents can book services.')
        return redirect('provider_dashboard')

    service = get_object_or_404(
        Service.objects.select_related(
            'provider',
            'provider__profile'
        ),
        id=id
    )

    payment_methods = [
        'Cash',
        'Card',
    ]

    if request.method == 'POST':

        booking_date = request.POST.get(
            'booking_date'
        )

        booking_time = request.POST.get(
            'booking_time'
        )

        selected_time = datetime.strptime(
            booking_time,
            '%H:%M'
        ).time()

        provider_profile = service.provider.profile

        if (
            provider_profile.working_start_time and
            provider_profile.working_end_time
        ):

            if not (
                provider_profile.working_start_time
                <= selected_time <=
                provider_profile.working_end_time
            ):

                messages.error(
                    request,
                    'Selected time is outside provider working hours.'
                )

                return redirect(
                    'book_service',
                    id=service.id
                )

        booking = Booking.objects.create(
            resident=request.user,
            provider=service.provider,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            status='pending'
        )

        Notification.objects.create(
            user=service.provider,
            title='New Booking Request',
            message=f'You received a new booking for {service.service_name}.'
        )
        Notification.objects.create(
            user=request.user,
            title='Booking Created',
            message=f'Your booking for {service.service_name} has been submitted successfully.'
        )

        messages.success(
            request,
            'Service booked successfully.'
        )

        return redirect('resident_bookings')

    return render(
        request,
        'residents/book_service.html',
        {
            'service': service,
            'payment_methods': payment_methods,
        }
    )


@login_required
def resident_notifications(request):

    notifications = request.user.notifications.all().order_by(
        '-created_at'
    )

    notifications.filter(
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        'residents/notifications.html',
        {
            'notifications': notifications
        }
    )


@login_required
def submit_review(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        resident=request.user,
        status='completed'
    )

    if Review.objects.filter(
        booking=booking
    ).exists():

        messages.error(
            request,
            'Review already submitted.'
        )

        return redirect(
            'resident_bookings'
        )

    if request.method == "POST":

        Review.objects.create(
            booking=booking,
            resident=request.user,
            provider=booking.provider,
            rating=request.POST.get('rating'),
            review=request.POST.get('review')
        )

        messages.success(
            request,
            "Review submitted."
        )

        return redirect(
            'resident_bookings'
        )

    return render(
        request,
        'residents/add_review.html',
        {
            'booking': booking
        }
    )

from django.utils import timezone

@login_required
def cancel_booking(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if request.method == "POST":

        booking.status = 'cancelled'

        booking.cancelled_by = request.user

        booking.cancellation_reason = request.POST.get(
            'reason'
        )

        booking.cancelled_at = timezone.now()

        booking.save()

        messages.success(
            request,
            "Booking cancelled."
        )

        return redirect(
            'resident_bookings'
        )
    
@login_required
def toggle_favorite(request, provider_id):

    provider = get_object_or_404(
        User,
        id=provider_id
    )

    favorite, created = FavoriteProvider.objects.get_or_create(
        resident=request.user,
        provider=provider
    )

    if created:

        messages.success(
            request,
            "Provider added to favorites."
        )

    else:

        favorite.delete()

        messages.success(
            request,
            "Provider removed from favorites."
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'resident_home'
        )
    )

@login_required
def rebook_service(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        resident=request.user
    )

    return redirect(
        'book_service',
        booking.service.id
    )

@login_required
def favorite_providers(request):

    favorites = FavoriteProvider.objects.filter(
        resident=request.user
    ).select_related(
        'provider'
    ).prefetch_related(
        'provider__service_set'
    )

    for favorite in favorites:

        favorite.first_service = Service.objects.filter(
            provider=favorite.provider
        ).first()

    return render(
        request,
        'residents/favorite_providers.html',
        {
            'favorites': favorites
        }
    )


