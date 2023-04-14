import time
from authentication.models import Register
from authentication.utils import send_email, generate_otp, validate_otp, is_otp_expired
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def register(request):
    """To Register the User"""

    if request.method == "POST":
        useremail = request.POST['userEmail']
        otp_value = generate_otp()
        data = Register.objects.create(
            user_email = useremail, 
            )
        send_email(data, otp_value)
        request.session['useremail'] = useremail
        request.session['otp'] = otp_value
        request.session['otp_created_time'] = int(time.time())
        return redirect("verfication")
    return render( request, "register.html")


def verify_otp(request):
    """This API is used to verify the otp sent through email"""

    if request.method == 'POST':
        entered_otp = request.POST.getlist('otp')
        entered_otp =  "".join(entered_otp)
        otp_in_session = request.session.get('otp')
        otp_created_time = request.session.get('otp_created_time')
        if validate_otp(int(entered_otp), int(otp_in_session)) and not is_otp_expired(otp_created_time):
            context = {"message":"Otp Verified"}
            return render(request, "verify.html",context)
        else:
            context = {"message":"Otp Invalid"}
            return render(request, "verify.html",context)
    else:
        useremail_in_session = request.session.get('useremail')
        context={"useremail" : useremail_in_session}
        return render(request,"verify.html", context)
    
def resend_otp(request):
    """This API will resend the OTP to user if failed or expired """

    if request.method == 'GET':
        useremail_in_session = request.session.get('useremail')
        otp_value = generate_otp()
        data = Register.objects.create(
            user_email = useremail_in_session, 
            )
        send_email(data, otp_value)
        request.session['useremail'] = useremail_in_session
        request.session['otp'] = otp_value
        request.session['otp_created_time'] = int(time.time())
        return redirect("verfication")
