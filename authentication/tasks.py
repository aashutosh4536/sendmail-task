from celery import shared_task  
import sib_api_v3_sdk
import json

@shared_task(bind=True)
def send_mail_trigger(self,recipient_email, otp_generated):
    print(recipient_email,otp_generated,"^^^^^^^^^^^^^^^^^^^^^^&&&&&&&&&&&&&")
    subject = f'Email Verification code {otp_generated}'
    html_content = f'your verfication is {otp_generated}'      
    sender = {"name":"Team Thoughtwin","email":"aashutosh4536@gmail.com"}
    to = [{"email":f"{recipient_email}"}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    send_email=sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)
    return send_email