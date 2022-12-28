from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import SafeString

from ..models import Subscriber
from ..forms import ContactForm
from ..tokens import email_activation_token

def get_subscribe_email_template(request: HttpRequest,
                                 sub: Subscriber) -> SafeString:
    """ Returns email message template for newsletter subscription """
    return get_template('blog/email/activate_subscription.html').render({
        'user': sub.email,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(sub.pk)),
        'token': email_activation_token.make_token(sub),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    
def get_join_team_email_template(form: ContactForm) -> SafeString:
    """ Returns email message template for join team """
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    education_level = form.cleaned_data['education_level']
    return get_template('blog/email/join_team.html').render({
        'full_name': f'{last_name} {first_name}',
        'email': form.cleaned_data['email'],
        'education_level': dict(form.fields['education_level'].choices)[education_level],
        'expertise_area': form.cleaned_data['expertise_area'],
        'expectations': form.cleaned_data['expectations']
    })
    
def get_email_object(subject: str,
                     message: SafeString,
                     to_email: str) -> EmailMessage:
    """ Returns email object by subject and message to send to_email """
    email = EmailMessage(subject, 
                         message, 
                         to=[to_email])
    email.content_subtype = 'html'
    return email

def attach_file_if_available(request: HttpRequest,
                             email: EmailMessage) -> None:
    """ Attach file to EmailMessage if it is available """
    if request.FILES:
        uploaded_file = request.FILES['resume'] 
        email.attach(uploaded_file.name,
                     uploaded_file.read(),
                     uploaded_file.content_type)

def get_join_team_email_object(message: SafeString, to_email: str) -> EmailMessage:
    """ Returns email object to send """
    email = EmailMessage('Інформація про претендента у команду', 
                         message, 
                         to=[to_email])
    email.content_subtype = 'html'
    return email

def send_subscribe_email_message(request: HttpRequest, email: EmailMessage) -> None:
    """ Tryes to send email to user for subscribe """
    # try:
    email.send()
    messages.success(request, 'Please, сonfirm your subscription via email')
    # except:
    #     messages.error(request, 'Problem sending email to this adress, check if you typed it correctly')

def send_join_team_email_message(request: HttpRequest, email: EmailMessage) -> None:
    """ Tryes to send email to user for join team """
    try:
        email.send()
        messages.success(request, 'Thanks. We will contact you shortly')
    except:
        messages.error(request, 'Problem with sharing your contacts. Please, try again later')

def send_join_team_message(request: HttpRequest,
                           form: ContactForm,
                           email_to: str) -> None:
    """ Sends to user email message for joining team """
    message = get_join_team_email_template(form)
    email = get_email_object('Інформація про претендента у команду',
                             message,
                             email_to)
    attach_file_if_available(request, email)
    send_join_team_email_message(request, email)

def send_user_subscribe_activation(request: HttpRequest,
                                   sub: Subscriber) -> None:
    """ Sends to user email message for activate subscription """
    message = get_subscribe_email_template(request, sub)
    email = get_email_object('Activate your email newsletter subscription',
                             message,
                             sub.email)
    send_subscribe_email_message(request, email)