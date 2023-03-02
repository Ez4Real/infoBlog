from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_user(request, email, password):
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return True
    else:
        messages.error(request, 'Invalid email or password.')
        return False