from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
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

class ContactForm(forms.Form):
    EDUCATION_LEVELS = (
    ('1', _('Secondary')),
    ('2', _('High')),
    ('3', _('Doctor or candidate of sciences')),
    ('4', _('Other'))
    )
    first_name = forms.CharField(label=_('First name'), max_length=100)
    last_name = forms.CharField(label=_('Last name'), max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    education_level = forms.ChoiceField(label = _('Your level of education'), choices=EDUCATION_LEVELS)
    expertise_area = forms.CharField(label=_('Briefly describe your area of expertise'),
                                     max_length=600,
                                     widget=forms.Textarea)
    expectations = forms.CharField(label=_('What do you expect from cooperation with us?'),
                                   max_length=600,
                                   widget=forms.Textarea)
    resume = forms.FileField(label=_('Resume'))