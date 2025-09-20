import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Ensure you have your API key set in environment variables
# Locally, you can temporarily set it like this:
# os.environ["SENDGRID_API_KEY"] = "YOUR_SENDGRID_API_KEY"
load_dotenv()
FROM_EMAIL = "danny@impulsivemarketing.ie"  # must be a verified sender in SendGrid
TO_EMAIL = "dannyobrien761@gmail.com"                # where you want to receive test email

message = Mail(
    from_email=FROM_EMAIL,
    to_emails=TO_EMAIL,
    subject="SendGrid EU API Test",
    html_content="<strong>If you receive this email, SendGrid is working with EU residency!</strong>"
)

try:
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    # Ensure EU data residency if using a regional subuser
     #  sg.set_sendgrid_data_residency("eu")  
    response = sg.send(message)
    print("Status Code:", response.status_code)
    print("Body:", response.body)
    print("Headers:", response.headers)
    if response.status_code == 202:
        print("✅ Email sent successfully! Check your inbox.")
except Exception as e:
    print("❌ SendGrid Error:", e)
