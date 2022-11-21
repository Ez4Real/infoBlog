from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import SafeString

from ..models import Subscriber
from ..tokens import email_activation_token

def get_email_message_template(request: HttpRequest,
                               sub: Subscriber) -> SafeString:
    """ Returns email message template """
    return get_template('blog/email/activate_subscription.html').render({
        'user': sub.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(sub.pk)),
        'token': email_activation_token.make_token(sub),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    
def get_email_object(message: SafeString, to_email: str) -> EmailMessage:
    """ Returns email object to send """
    email = EmailMessage('Activate your email newsletter subscription', 
                         message, 
                         to=[to_email])
    email.content_subtype = 'html'
    return email

def send_email_message(request: HttpRequest, email: EmailMessage) -> None:
    """ Tryes to send email to user for subscribe """
    try:
        email.send()
        messages.success(request, 'Please, сonfirm your subscription via email')
    except:
        messages.error(request, 'Problem sending email to this adress, check if you typed it correctly')

def send_user_subscribe_activation(request: HttpRequest,
                  sub: Subscriber,
                  to_email: str) -> None:
    """ Sends to user email message for activate subscription """
    message = get_email_message_template(request, sub)
    email = get_email_object(message, to_email)
    send_email_message(request, email)