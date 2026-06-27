from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import Profile
import time

from django.conf import settings

from django.core.mail import send_mail

from django.contrib.auth import login

from django.contrib.auth.models import User

from .utils import generate_otp

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

        email = request.POST.get('email').strip().lower()

        # Username will be the email
        username = email

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


        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Email already exists.'
            )

            return redirect('register')

        user = User.objects.create_user(
            username=email,
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

def login_view(request):

    if request.user.is_authenticated:

        try:

            profile = request.user.profile

            if profile.role == "provider":
                return redirect("provider_dashboard")

            return redirect("resident_home")

        except:

            logout(request)

    if request.method == "POST":

        email = request.POST.get("email").strip().lower()

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            messages.error(request,"Email is not registered.")

            return redirect("login")

        otp = generate_otp()

        request.session["otp"] = otp

        request.session["otp_email"] = email

        request.session["otp_time"] = time.time()

        send_mail(

            "HomeAssist Login OTP",

            f"""
Hello,

Your OTP for HomeAssist Login is:

{otp}

This OTP will expire in 5 minutes.

Do not share this OTP.

HomeAssist Team
""",

            settings.EMAIL_HOST_USER,

            [email],

            fail_silently=False

        )

        messages.success(request,"OTP has been sent.")

        return redirect("verify_login_otp")

    return render(request,"accounts/login.html")


def verify_login_otp(request):

    if request.method=="POST":

        entered_otp=request.POST.get("otp")

        original_otp=request.session.get("otp")

        email=request.session.get("otp_email")

        otp_time=request.session.get("otp_time")

        if not otp_time:

            messages.error(request,"OTP expired.")

            return redirect("login")

        if time.time()-otp_time>300:

            messages.error(request,"OTP expired.")

            return redirect("login")

        if entered_otp!=original_otp:

            messages.error(request,"Invalid OTP")

            return redirect("verify_login_otp")

        user=User.objects.get(email=email)

        login(request,user)

        request.session.pop("otp",None)
        request.session.pop("otp_email",None)
        request.session.pop("otp_time",None)

        try:
            profile = user.profile

            if profile.role == "provider":
                return redirect("provider_dashboard")

            elif profile.role == "resident":
                return redirect("resident_home")

            else:
                messages.error(request, "Invalid role.")
                logout(request)
                return redirect("login")

        except Profile.DoesNotExist:
            logout(request)
            messages.error(request, "Profile not found.")
            return redirect("login")

    return render(request,"accounts/verify_login_otp.html")


# =========================
# LOGOUT VIEW
# =========================
def logout_view(request):

    logout(request)

    messages.error(
        request,
        'Logged out successfully.'
    )

    return redirect('login')