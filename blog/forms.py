from .models import Subscriber
from django import forms

class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(label='Ваш email',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:  
        model = Subscriber 
        fields = ['email']