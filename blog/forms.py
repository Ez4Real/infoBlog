from django.contrib.auth import get_user_model
from django import forms


class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(label='',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             required=True)
    
    class Meta:  
        model = get_user_model() 
        fields = ['email']
        
    def save(self, commit=True):
        sub = super(SubscriberForm, self).save(commit=False)
        sub.email = self.cleaned_data['email']
        if commit:
            sub.save()

        return sub
        