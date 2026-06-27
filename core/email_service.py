import requests
from django.conf import settings


def send_otp_email(email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "HomeAssist",
            "email": "mangesh.kokare@bds.christuniversity.in"
        },

        "to": [
            {
                "email": email
            }
        ],

        "subject": "HomeAssist Login OTP",

        "htmlContent": f"""
        <div style="font-family:Arial;padding:30px">

            <h2>HomeAssist Login</h2>

            <p>Your One Time Password is</p>

            <h1 style="color:#2563eb">{otp}</h1>

            <p>This OTP expires in <b>5 minutes</b>.</p>

            <hr>

            <p>Please do not share this OTP.</p>

        </div>
        """
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print(response.status_code)
    print(response.text)

    response.raise_for_status()