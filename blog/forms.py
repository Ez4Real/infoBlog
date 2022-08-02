from django import forms  
from .models import UserEmail
  
class UserEmailForm(forms.ModelForm):  
    class Meta:  
        model = UserEmail 
        fields = "__all__"