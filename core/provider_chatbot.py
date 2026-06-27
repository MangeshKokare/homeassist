def get_main_menu(provider_name):

    return f"""
🤖 HomeAssist Provider Assistant

Hello Provider 👋 {provider_name}

Welcome to HomeAssist.

I'm here to help you manage your HomeAssist account.

Please choose an option.

1️⃣ Accept or Reject Bookings

2️⃣ Start a Service

3️⃣ Complete a Service

4️⃣ Booking Status

5️⃣ OTP Help

6️⃣ Edit My Profile

7️⃣ Verification Documents

8️⃣ Contact Support

0️⃣ Exit Chat
"""


def get_provider_bot_reply(message, provider_name):

    message = message.strip().lower()

    if message in ["hi", "hello", "hey", "start", "menu", "/start"]:
        return get_main_menu(provider_name)

    elif message == "1":
        return """
📅 Accept or Reject Bookings

• Open Provider Dashboard.

• Open Pending Bookings.

• Review the booking details.

• Tap Accept or Reject.

Reply with 99 to return.
"""

    elif message == "2":
        return """
▶️ Start a Service

• Reach the customer's location.

• Ask the resident for the Start OTP.

• Enter the OTP.

• The booking status changes to In Progress.

Reply with 99 to return.
"""

    elif message == "3":
        return """
✅ Complete a Service

• Finish the work.

• Ask the resident for the Completion OTP.

• Enter the OTP.

• The booking will be marked as Completed.

Reply with 99 to return.
"""

    elif message == "4":
        return """
📍 Booking Status

Possible booking statuses:

• Pending

• Accepted

• In Progress

• Completed

• Cancelled

Reply with 99 to return.
"""

    elif message == "5":
        return """
🔐 OTP Help

• OTP is provided by the resident.

• Verify the OTP before starting.

• Verify another OTP after completing.

Reply with 99 to return.
"""

    elif message == "6":
        return """
👤 Edit Profile

• Open Profile.

• Tap Edit Profile.

• Update your information.

• Save the changes.

Reply with 99 to return.
"""

    elif message == "7":
        return """
🪪 Verification Documents

• Upload Aadhaar.

• Upload PAN Card.

• Wait for Admin Verification.

• Check verification status in your profile.

Reply with 99 to return.
"""

    elif message == "8":
        return """
💰 Earnings & Payments

• View completed bookings.

• Check your earnings.

• Download payment history.

Reply with 99 to return.
"""

    elif message == "9":
        return """
☎ Contact Support

📧 support@homeassist.com

📞 +91-8485809524

Monday to Saturday

9:00 AM to 6:00 PM

Reply with 99 to return.
"""

    elif message == "99":
        return get_main_menu(provider_name)

    elif message in ["0", "exit", "quit"]:
        return """
👋 Thank you.

Have a great day.

Type

hello

to open the menu again.
"""

    else:
        return f"""
    🤖 HomeAssist Provider Assistant

    Hello Provider 👋 {provider_name}

    Welcome to HomeAssist.

    I'm here to help you manage your HomeAssist account.

    Please choose one of the following options.

    1️⃣ Accept or Reject Bookings

    2️⃣ Start a Service

    3️⃣ Complete a Service

    4️⃣ Booking Status

    5️⃣ OTP Help

    6️⃣ Edit My Profile

    7️⃣ Verification Documents

    8️⃣ Contact Support

    0️⃣ Exit Chat
    """