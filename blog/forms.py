from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Subscriber, LibraryMember
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


TextInputWidget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
SelectWidget = forms.Select(attrs={'class': 'form-control'})
FileInputWidget = forms.FileInput(attrs={'class': 'form-control', 'style': 'max-width: 50%'})
PhoneNumberWidget = PhoneNumberPrefixWidget(initial='UA', attrs={'class': 'form-control'})


class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(label='',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             required=True)
    
    class Meta:  
        model = Subscriber
        fields = ['email']
        
    def save(self, commit=True):
        sub = super().save(commit=False)
        sub.email = self.cleaned_data['email']
        if commit:
            sub.save()

        return sub

    
class BaseMemberForm(forms.Form):
    first_name = forms.CharField(label=_('First name'),
                                 max_length=100,
                                 widget=TextInputWidget)
    last_name = forms.CharField(label=_('Last name'),
                                max_length=100,
                                widget=TextInputWidget)
    email = forms.EmailField(label='E-mail',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}))
    


class ContactForm(BaseMemberForm):
    EDUCATION_LEVELS = (
    ('1', _('Secondary')),
    ('2', _('High')),
    ('3', _('Doctor or PhD')),
    ('4', _('Other'))
    )
    education_level = forms.ChoiceField(label = _('Level of education'),
                                        choices=EDUCATION_LEVELS,
                                        widget=SelectWidget)
    expertise_area = forms.CharField(label=_('Briefly describe your area of expertise'),
                                     max_length=600,
                                     widget=TextInputWidget)
    expectations = forms.CharField(label=_('What do you expect from cooperation with us?'),
                                   max_length=600,
                                   widget=forms.Textarea(attrs={'type': 'text', 'class': 'form-control', 'style': 'max-height: 90px'}))
    resume = forms.FileField(label=_('Resume'),
                             widget=FileInputWidget)
    

class VolunteerForm(BaseMemberForm):
    dob = forms.DateField(label=_('Date of Birth'),
                          widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    city = forms.CharField(label=_('City'),
                           max_length=100,
                           widget=TextInputWidget)
    phone = PhoneNumberField(label=_('Phone'),
                             widget=PhoneNumberWidget)
    employment = forms.CharField(label=(_('What do you do in life?')),
                                 max_length=600,
                                 widget=forms.Textarea(attrs={'type': 'text', 'class': 'form-control', 'style': 'max-height: 160px; width: 100%;'}))
    

class LibraryMemberForm(BaseMemberForm):
    EDUCATION_LEVELS = (
    (1, _('Master')),
    (2, _('Doctor or PhD')),
    (3, _('Postgraduate')),
    (4, _('Doctorate'))
    )
    
    phone = PhoneNumberField(label=_('Phone'),
                             widget=PhoneNumberWidget)
    password = forms.CharField(label=_('Password'),
                               max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    institution = forms.CharField(label=_('Higher Education or Research Institution'),
                                  max_length=200,
                                  widget=TextInputWidget)
    department = forms.CharField(label=_('Research Unit/Department/Chair'),
                                 max_length=200,
                                 widget=TextInputWidget)
    specialization = forms.CharField(label=_('Scientific Specialization'),
                                     max_length=200,
                                     widget=TextInputWidget)
    education_level = forms.ChoiceField(label = _('Level of education'),
                                        choices=EDUCATION_LEVELS,
                                        widget=SelectWidget)
    supervisor = forms.CharField(label=_('Academic Supervisor/Cosultant'),
                                 max_length=200,
                                 widget=TextInputWidget)
    resource_plans = forms.CharField(label=_('How do you plan to use the sources of ERGOSUM European Library?'),
                                     max_length=600,
                                     widget=forms.Textarea(attrs={'type': 'text', 'class': 'form-control', 'style': 'max-height: 90px'}))
    google_scholar = forms.CharField(label=_('ORCHID/Google Scholar'),
                                     required=False,
                                     max_length=200,
                                     widget=TextInputWidget)
    resume = forms.FileField(label=_('Academic CV'),
                             required=False,
                             widget=FileInputWidget)