from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib import messages
from .models import Service, Booking, Message
from .forms import ServiceForm, BookingForm
from datetime import datetime

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

    categories = Service.objects.values_list(
        'category',
        flat=True
    ).distinct()

    context = {
        'services': services,
        'search_query': search_query,
        'active_category': active_category,
        'categories': categories,
    }

    return render(
        request,
        'residents/explore_services.html',
        context
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

    active_status = request.GET.get('status', 'pending')

    if active_status == 'all':
        bookings = all_bookings

    elif active_status in [
        'pending',
        'accepted',
        'completed',
        'cancelled'
    ]:
        bookings = all_bookings.filter(
            status=active_status
        )

    else:
        bookings = all_bookings.filter(
            status='pending'
        )
        active_status = 'pending'

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
    active_status = request.GET.get('status', 'pending')

    if active_status == 'all':
        bookings = all_bookings.order_by('-created_at')
    elif active_status in [
        'pending',
        'accepted',
        'completed',
        'cancelled'
    ]:
        bookings = all_bookings.filter(
            status=active_status
        ).order_by('-created_at')
    else:
        bookings = all_bookings.filter(status='pending').order_by('-created_at')
        active_status = 'pending'

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

            'completed_count': all_bookings.filter(
                status='completed'
            ).count(),

            'cancelled_count': all_bookings.filter(
                status='cancelled'
            ).count(),

            'total_count': all_bookings.count(),
        }
    )


# =========================
# UPDATE BOOKING STATUS
# =========================
@login_required
def update_booking_status(request, booking_id, new_status):
    booking = get_object_or_404(Booking, id=booking_id, provider=request.user)

    valid_statuses = [
        'pending',
        'accepted',
        'completed',
        'cancelled'
    ]
    if new_status in valid_statuses:
        booking.status = new_status
        booking.save()
        messages.success(request, f'Booking marked as {new_status}.')
    else:
        messages.error(request, 'Invalid status.')

    return redirect('provider_bookings')


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


# =========================
# PROVIDER PROFILE
# =========================
@login_required
def provider_profile(request):
    if request.user.profile.role != 'provider':
        messages.error(request, 'Access denied. Providers only.')
        return redirect('resident_home')

    all_bookings = Booking.objects.filter(provider=request.user)

    return render(request, 'services/provider_profile.html', {
        'services_count': Service.objects.filter(provider=request.user).count(),
        'total_bookings': all_bookings.count(),
        'completed_bookings': all_bookings.filter(status='completed').count(),
        'pending_bookings': all_bookings.filter(status='pending').count(),
    })


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
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone', '').strip()
        profile.address = request.POST.get('address', '').strip()

        profile.working_start_time = request.POST.get(
            'working_start_time'
        )

        profile.working_end_time = request.POST.get(
            'working_end_time'
        )

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('provider_profile')

    return render(request, 'services/edit_profile.html')


# =========================
# PROVIDER DETAILS (for residents)
# =========================
@login_required
def provider_details(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'residents/provider_details.html', {'service': service})

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

        Booking.objects.create(
            resident=request.user,
            provider=service.provider,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            status='pending'
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