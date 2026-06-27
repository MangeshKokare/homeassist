MAIN_MENU = """
🤖 HomeAssist Assistant

Hello 👋

Welcome to HomeAssist Support.

I'm here to help you.

Please type the number of the option you need.

1️⃣ How to use HomeAssist

2️⃣ Book a Service

3️⃣ Cancel a Booking

4️⃣ Booking Status

5️⃣ OTP Problems

6️⃣ Payments

7️⃣ Become a Service Provider

8️⃣ Ratings & Reviews

9️⃣ Contact Support

0️⃣ Exit Chat
"""


def get_bot_reply(message):

    message = message.strip().lower()

    if message in ["hi", "hello", "hey", "start", "/start", "menu"]:
        return MAIN_MENU

    elif message == "1":
        return """
        📖 How to use HomeAssist

        • Register or Login.

        • Complete your profile.

        • Browse available services.

        • Select the service you need.

        • Choose your preferred provider.

        • Select the booking date.

        • Select the booking time.

        • Confirm your booking.

        • Chat with your provider if required.

        • Share the Start OTP when the provider arrives.

        • Share the Completion OTP after the work is finished.

        • Rate and review your provider.

        ━━━━━━━━━━━━━━━━━━━━

        Reply with 99 to return to the Main Menu.
        """

    elif message == "2":
        return """
📅 Book a Service

1️⃣ Open the Explore page.

2️⃣ Choose a service category.

3️⃣ Select a provider.

4️⃣ View provider details.

5️⃣ Choose your preferred date.

6️⃣ Choose your preferred time.

7️⃣ Click Confirm Booking.

8️⃣ Wait for the provider to accept your request.

Reply with 99 to return to the Main Menu.
"""

    elif message == "3":
        return """
❌ Cancel a Booking

1️⃣ Open My Bookings.

2️⃣ Select the booking.

3️⃣ Tap Cancel Booking.

4️⃣ Select the cancellation reason.

5️⃣ Confirm cancellation.

Note:
Cancellation may not be available after the provider has started the service.

Reply with 99 to return to the Main Menu.
"""

    elif message == "4":
        return """
📍 Booking Status

Booking status can be:

🟡 Pending

🟢 Accepted

🟠 In Progress

✅ Completed

🔴 Cancelled

Open My Bookings to view the current status.

Reply with 99 to return to the Main Menu.
"""

    elif message == "5":
        return """
🔐 OTP Problems

1️⃣ Wait for at least 30 seconds.

2️⃣ Tap Resend OTP.

3️⃣ Check your mobile network.

4️⃣ Verify your registered phone number.

5️⃣ Restart the application if needed.

6️⃣ Contact support if the issue continues.

Reply with 99 to return to the Main Menu.
"""

    elif message == "6":
        return """
💳 Payments

1️⃣ Payments are completely secure.

2️⃣ Complete payments only through HomeAssist.

3️⃣ Never pay outside the application.

4️⃣ Download your payment receipt anytime.

5️⃣ Contact support for payment issues.

Reply with 99 to return to the Main Menu.
"""

    elif message == "7":
        return """
👷 Become a Service Provider

1️⃣ Open your Profile.

2️⃣ Tap Become a Provider.

3️⃣ Complete your personal details.

4️⃣ Upload Aadhaar.

5️⃣ Upload PAN Card.

6️⃣ Submit verification.

7️⃣ Wait for admin approval.

8️⃣ Start receiving bookings.

Reply with 99 to return to the Main Menu.
"""

    elif message == "8":
        return """
⭐ Ratings & Reviews

1️⃣ Open Completed Bookings.

2️⃣ Select your completed booking.

3️⃣ Tap Rate & Review.

4️⃣ Give a rating from 1 to 5 stars.

5️⃣ Write your review.

6️⃣ Submit your feedback.

Reply with 99 to return to the Main Menu.
"""

    elif message == "9":
        return """
☎ Contact Support

📧 Email

support@homeassist.com

📞 Phone

+91-8485809824

🕘 Working Hours

Monday to Saturday

9:00 AM to 6:00 PM

Reply with 99 to return to the Main Menu.
"""

    elif message in ["0", "exit", "quit"]:
        return """
👋 Thank you for using HomeAssist.

We hope we were able to help you.

Type

hello

or

menu

whenever you need assistance again.
"""

    elif message == "99":
        return MAIN_MENU

    else:
        return """
❌ Invalid option selected.

Please choose one of the following options.

1️⃣ How to use HomeAssist

2️⃣ Book a Service

3️⃣ Cancel a Booking

4️⃣ Booking Status

5️⃣ OTP Problems

6️⃣ Payments

7️⃣ Become a Service Provider

8️⃣ Ratings & Reviews

9️⃣ Contact Support

0️⃣ Exit Chat
"""
