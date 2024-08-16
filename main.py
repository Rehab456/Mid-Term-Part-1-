import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Sheety API details
SHEETY_API_URL = 'https://api.sheety.co/89639a95e436705219f75e996c4dcd70/weddingGuestList/sheet1'

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Your email address from environment variables
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  

def get_guests_list():
    response = requests.get(SHEETY_API_URL)
    response.raise_for_status()
    data = response.json()
    print(data)  
    return data.get('sheet1', [])  

def send_email(to_email, names):
    # Create the email content
    subject = "You're Invited to Our Wedding!"
    body = f"Dear {names},\n\nWe are excited to invite you to our wedding! Please let us know if you can attend.\n\nBest,\nYour Name"

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the email server
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"Email sent to {names} ({to_email})")
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your email and password.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    guests = get_guests_list()
    for guests in guests:
        print(guests)  
        names = guests.get('names', 'guests names')  
        emails = guests.get('emails', 'guests emails')  
        send_email(emails, names)

if __name__ == "__main__":
    main()
