import re

from django.contrib import messages
from django.http import HttpRequest
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from ..forms import SubscriberForm
from ..models import Subscriber
from ..tokens import email_activation_token
from .email_services import send_user_subscribe_activation

def get_subscriber_form(request: HttpRequest) -> SubscriberForm:
    """ Returns Subcriber form """
    if request.POST:
        sub = Subscriber(email=request.POST['email'])
        if Subscriber.objects.filter(email=sub.email).exists():
            messages.warning(request, 'This address is already subscribed!')
        elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", sub.email):
            messages.error(request, 'This address is not valid!')
        else:
            sub.save()
            send_user_subscribe_activation(request, sub, sub.email)

    return SubscriberForm()

def get_subscriber_by_uid(uidb64: str) -> Subscriber:
    """ Returns Subcriber by uidb64 decoding """
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
    except: 
        sub = None
    else: 
        return Subscriber.objects.get(pk=uid)
    
def check_subscriber_and_token(sub: Subscriber, token: str) -> bool:
    """ Checks if subscriber is not None and his token """
    return True if sub is not None and email_activation_token.check_token(sub, token) else False

