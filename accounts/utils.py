from django.core.mail import EmailMessage

def send_verification_email(mail_subject, message, from_email, to_email):
    try:
        email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
        if email.send():
            return True
    except Exception as e:
        print (e)
        return False
