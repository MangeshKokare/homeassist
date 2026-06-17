from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import Profile


# =========================
# REGISTER VIEW
# =========================
def register_view(request):

    # If user already logged in
    if request.user.is_authenticated:

        try:
            profile = request.user.profile

            if profile.role == 'provider':
                return redirect('provider_dashboard')

            elif profile.role == 'resident':
                return redirect('resident_home')

        except:
            logout(request)

    # Register Form Submit
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        username = request.POST.get('username')
        email = request.POST.get('email')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        role = request.POST.get('role')

        phone = request.POST.get('phone')
        address = request.POST.get('address')

        profile_image = request.FILES.get('profile_image')

        aadhaar_number = request.POST.get('aadhaar_number')
        pan_number = request.POST.get('pan_number')

        aadhaar_image = request.FILES.get('aadhaar_image')
        pan_image = request.FILES.get('pan_image')

        working_start_time = request.POST.get('working_start_time')
        working_end_time = request.POST.get('working_end_time')

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Email already exists.'
            )

            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        Profile.objects.create(
            user=user,
            role=role,
            phone=phone,
            address=address,
            profile_image=profile_image,
            aadhaar_number=aadhaar_number,
            aadhaar_image=aadhaar_image,
            pan_number=pan_number,
            pan_image=pan_image,
            working_start_time=working_start_time or None,
            working_end_time=working_end_time or None
        )

        messages.success(
            request,
            'Account created successfully.'
        )

        return redirect('login')

    return render(
        request,
        'accounts/register.html'
    )


# =========================
# LOGIN VIEW
# =========================
def login_view(request):

    # Already Logged In
    if request.user.is_authenticated:

        try:
            profile = request.user.profile

            # Provider Dashboard
            if profile.role == 'provider':
                return redirect('provider_dashboard')

            # Resident Dashboard
            elif profile.role == 'resident':
                return redirect('resident_home')

        except Profile.DoesNotExist:

            logout(request)

    # Login Submit
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # If user exists
        if user is not None:

            login(request, user)

            try:
                profile = user.profile

                # Provider Login
                if profile.role == 'provider':

                    messages.success(
                        request,
                        'Provider login successful.'
                    )

                    return redirect(
                        'provider_dashboard'
                    )

                # Resident Login
                elif profile.role == 'resident':

                    messages.success(
                        request,
                        'Resident login successful.'
                    )

                    return redirect(
                        'resident_home'
                    )

                # Invalid Role
                else:

                    messages.error(
                        request,
                        'Invalid user role.'
                    )

                    logout(request)

                    return redirect('login')

            except Profile.DoesNotExist:

                messages.error(
                    request,
                    'Profile not found.'
                )

                logout(request)

                return redirect('login')

        # Invalid Credentials
        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return redirect('login')

    return render(
        request,
        'accounts/login.html'
    )


# =========================
# LOGOUT VIEW
# =========================
def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Logged out successfully.'
    )

    return redirect('login')