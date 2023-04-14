import random
import time
from authentication.models import Response
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from decouple import config
from django.conf import settings
from .tasks import send_mail_trigger
import json
from celery.result import AsyncResult

root_path = settings.BASE_DIR

API_KEY = config('API_KEY')


def generate_otp():
    """OTP genration """
    otp_generate = random.randint(100000, 999999)
    return otp_generate


def validate_otp(entered_otp, otp_in_session):
    """Validate OTP"""

    if entered_otp == otp_in_session:
        return True
    else:
        return False


def is_otp_expired(otp_created_time):
    """Checks if OTP is expired or not"""

    current_time = int(time.time())
    if current_time - otp_created_time > 60:
        return True
    else:
        return False


def configure_email():
    """Email Configuration"""

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    return api_instance


def send_email(instance, otp_value):
        """Function to send mail via sendinblue platform"""

        recipient_email = instance.user_email
        otp_generated = otp_value
        api_instance = configure_email()
        # send_smtp_email = send_mail_trigger.delay(recipient_email,otp_generated)
        send_smtp_email = send_mail_trigger(recipient_email,otp_generated)

        try:    
            api_response = api_instance.send_transac_email(send_smtp_email)
            if api_response:
                Response.objects.create(response='Message sent Successfully', email = recipient_email)
            else:
                Response.objects.create(response='Failed', email = recipient_email)
        except ApiException as e:
            Response.objects.create(response = e.body, email = recipient_email)