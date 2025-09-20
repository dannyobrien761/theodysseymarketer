# utils/send_email.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, to_email, html_content, from_email=None):
    """
    Reusable helper to send an email via SendGrid.

    Args:
        subject (str): Subject line of the email
        to_email (str or list): Recipient email(s)
        html_content (str): HTML content of the email
        from_email (str, optional): Defaults to DEFAULT_FROM_EMAIL in env
    """
    from_email = from_email or os.environ.get("DEFAULT_FROM_EMAIL")

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
       # sg.set_sendgrid_data_residency("eu")
        response = sg.send(message)
        print(response.body)
        print(response.headers)
        return response.status_code  # 202 means success
    except Exception as e:
        # Log or raise for debugging
        print("SendGrid Error:", e)
        return None
