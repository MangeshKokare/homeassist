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

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Validation
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

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create Profile
        Profile.objects.create(
            user=user,
            role=role
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