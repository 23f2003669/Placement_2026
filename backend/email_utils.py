import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, html_body):
    """
    Send an HTML email via Gmail SMTP.
    Reads credentials from environment (.env loaded by config).
    Returns True on success, False on failure.
    """
    server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    port = int(os.environ.get('MAIL_PORT', 587))
    username = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    sender = os.environ.get('MAIL_DEFAULT_SENDER', username)

    if not username or not password:
        print('[email] MAIL_USERNAME or MAIL_PASSWORD not set - skipping send')
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(server, port) as smtp:
            smtp.starttls()
            smtp.login(username, password)
            smtp.sendmail(sender, [to_email], msg.as_string())
        print(f'[email] sent to {to_email}: {subject}')
        return True
    except Exception as e:
        print(f'[email] failed to send to {to_email}: {e}')
        return False
