import requests
from django.conf import settings


def send_otp_email(email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
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
        <h2>HomeAssist Login</h2>
        <h1>{otp}</h1>
        """
    }

    print("=" * 60)
    key = settings.BREVO_API_KEY

    print("KEY EXISTS:", key is not None)
    print("KEY LENGTH:", len(key or ""))

    if key:
        print("FIRST 10:", key[:10])
        print("LAST 10:", key[-10:])

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
    print("=" * 60)

    # Stop here if Brevo returned an error
    if response.status_code != 201:
        raise Exception(f"Brevo Error: {response.text}")