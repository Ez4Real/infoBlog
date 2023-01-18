from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

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
    ('3', _('Doctor or PhD')),
    ('4', _('Other'))
    )
    first_name = forms.CharField(label=_('First name'),
                                 max_length=100,
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    last_name = forms.CharField(label=_('Last name'),
                                max_length=100,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}))
    education_level = forms.ChoiceField(label = _('Your level of education'),
                                        choices=EDUCATION_LEVELS,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    expertise_area = forms.CharField(label=_('Briefly describe your area of expertise'),
                                     max_length=600,
                                     widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    expectations = forms.CharField(label=_('What do you expect from cooperation with us?'),
                                   max_length=600,
                                   widget=forms.Textarea(attrs={'type': 'text', 'class': 'form-control', 'style': 'max-height: 90px'}))
    resume = forms.FileField(label=_('Resume'),
                             widget=forms.FileInput(attrs={'class': 'form-control', 'style': 'max-width: 50%'}))
    

class VolunteerForm(forms.Form):
    first_name = forms.CharField(label=_('First name'),
                                 max_length=100,
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    last_name = forms.CharField(label=_('Last name'),
                                max_length=100,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    
    dob = forms.DateField(label=_('Date of Birth'),
                          widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    city = forms.CharField(label=_('City'),
                           max_length=100,
                           widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}))
    phone = PhoneNumberField(label=_('Phone'),
                             widget=PhoneNumberPrefixWidget(initial='UA', attrs={'class': 'form-control'}))
    employment = forms.CharField(label=('What do you do in life?'),
                                 max_length=600,
                                 widget=forms.Textarea(attrs={'type': 'text','class': 'form-control', 'style': 'max-height: 160px; width: 100%;'}))
    