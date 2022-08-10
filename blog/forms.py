from .models import UserEmail
from django.forms import ModelForm, EmailInput
  
class UserEmailForm(ModelForm):
    email = EmailInput()
    
    class Meta:  
        model = UserEmail 
        fields = "__all__"