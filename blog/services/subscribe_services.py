import re

from django.contrib import messages
from django.http import HttpRequest
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.conf import settings

from ..forms import SubscriberForm, ContactForm, \
    VolunteerForm, LibraryMemberForm
from ..models import Subscriber
from ..tokens import email_activation_token
from .email_services import send_user_subscribe_activation, \
    send_join_team_message, send_volunteer_message

def get_subscriber_form(request: HttpRequest) -> SubscriberForm:
    """ Returns Subcriber form """
    if 'subscribe' in request.POST:
        sub = Subscriber.objects.get(email=request.POST['email'])
        if sub.is_active:
            messages.warning(request, 'This address is already subscribed!')
        elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", sub.email):
            messages.error(request, 'This address is not valid!')
        else:
            sub.save()
            send_user_subscribe_activation(request, sub)

    return SubscriberForm()

def get_join_team_form(request: HttpRequest) -> ContactForm:
    """ Returns form for Joining Team """
    if 'join_team' in request.POST:
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            send_join_team_message(request, form, settings.EMAIL_FROM)
            
    return ContactForm()

def get_volunteer_form(request: HttpRequest) -> VolunteerForm:
    """ Returns form for Volunteer """
    if 'volunteer' in request.POST:
        form = VolunteerForm(request.POST)
        if form.is_valid():
            send_volunteer_message(request, form, settings.EMAIL_FROM)
        else: messages.error(request, 'Form is not valid. Check if you typed phone correctly.')
        
    return VolunteerForm()

def get_library_member_form(request: HttpRequest) -> LibraryMemberForm:
    """ Returns form for Library member """
    if 'library_form' in request.POST:
        form = LibraryMemberForm(request.POST)
        if form.is_valid():
            print('\n\nOKAY\n\n')
        else: messages.error(request, 'Form is not valid. Check if you typed phone correctly.')
    
    return LibraryMemberForm()

def get_subscriber_by_uid(uidb64: str) -> Subscriber:
    """ Returns Subcriber by uidb64 decoding """
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
    except: 
        return None
    else: 
        return Subscriber.objects.get(pk=uid)
    
def check_subscriber_and_token(sub: Subscriber, token: str) -> bool:
    """ Checks if subscriber is not None and his token """
    return True if sub is not None and email_activation_token.check_token(sub, token) else False

def activate_user_subscription(request: HttpRequest, uidb64: str, 
                               token: str, lang: str) -> redirect:
    """ Activates user newsletter subscription with chosen language """
    sub = get_subscriber_by_uid(uidb64)

    if check_subscriber_and_token(get_subscriber_by_uid(uidb64), 
                                  token):
        sub.is_active = True
        sub.mailing_language = lang
        sub.save()
        messages.success(request, 'Thank you for subscription.')
    else:
        messages.error(request, 'Activation link is invalid!')
        
    return redirect('homepage')

def deactivate_user_subscription(request: HttpRequest, 
                                 uidb64: str, 
                                 token:str) -> redirect:
    """ Deactivates user newsletter subscription """
    sub = get_subscriber_by_uid(uidb64)

    if check_subscriber_and_token(sub, token):
        sub.delete()
        messages.success(request, 'Unsubscribed successfully')
    else:
        messages.error(request, 'Activation link is invalid!')
        
    return redirect('homepage')

