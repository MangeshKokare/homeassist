from django.urls import path

from .accounts_views import (
    login_view,
    register_view,
    logout_view
)

from .service_views import (
    resident_home,
    explore_services,
    resident_bookings,
    resident_messages,
    resident_profile,
    resident_edit_profile,
    provider_dashboard,
    add_service,
    provider_details,
    book_service,
    edit_service,
    delete_service,
    provider_bookings,
    update_booking_status,
    provider_messages,
    provider_profile,
    edit_profile,
    verify_start_otp,
    verify_complete_otp,
    resident_notifications,
    provider_notifications,
    submit_review,
    cancel_booking,
    toggle_favorite,
    rebook_service,
    favorite_providers,
)

from .message_views import chat_view


urlpatterns = [

    path('', login_view, name='login'),

    path('register/', register_view, name='register'),

    path('logout/', logout_view, name='logout'),

    path('resident/home/', resident_home, name='resident_home'),

    path('resident/explore/', explore_services, name='explore_services'),

    path('resident/bookings/', resident_bookings, name='resident_bookings'),

    path('resident/messages/', resident_messages, name='resident_messages'),

    path('resident/profile/', resident_profile, name='resident_profile'),

    path('resident/profile/edit/', resident_edit_profile, name='resident_edit_profile'),

    path('provider/details/<int:id>/', provider_details, name='provider_details'),

    path('book/<int:id>/', book_service, name='book_service'),

    path('provider/dashboard/', provider_dashboard, name='provider_dashboard'),

    path('provider/service/add/', add_service, name='add_service'),

    path('provider/service/<int:id>/edit/', edit_service, name='edit_service'),

    path('provider/service/<int:id>/delete/', delete_service, name='delete_service'),

    path('provider/bookings/', provider_bookings, name='provider_bookings'),

    path('provider/bookings/<int:booking_id>/status/<str:new_status>/', update_booking_status, name='update_booking_status'),

    path('provider/messages/', provider_messages, name='provider_messages'),

    path('provider/profile/', provider_profile, name='provider_profile'),

    path('provider/profile/edit/', edit_profile, name='edit_profile'),

    path('chat/<int:user_id>/', chat_view, name='chat'),

    path('provider/bookings/<int:booking_id>/verify-start-otp/',verify_start_otp,name='verify_start_otp'),
    
    path('provider/bookings/<int:booking_id>/verify-complete-otp/',verify_complete_otp,name='verify_complete_otp'),

    path('resident/notifications/',resident_notifications,name='resident_notifications'),

    path('provider/notifications/',provider_notifications,name='provider_notifications'),

    path('booking/<int:booking_id>/review/',submit_review,name='submit_review'),

    path('booking/<int:booking_id>/cancel/',cancel_booking,name='cancel_booking'),

    path('provider/<int:provider_id>/favorite/',toggle_favorite,name='toggle_favorite'),

    path('booking/<int:booking_id>/rebook/',rebook_service,name='rebook_service'),

    path('resident/favorites/',favorite_providers,name='favorite_providers'),
]