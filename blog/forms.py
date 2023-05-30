import datetime

from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator

from .models import Subscriber, LibraryMember
from .services.validators import validate_password

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


TextInputWidget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
SelectWidget = forms.Select(attrs={'class': 'form-control'})
FileInputWidget = forms.FileInput(attrs={'class': 'form-control'})
PhoneNumberWidget = PhoneNumberPrefixWidget(initial='UA', attrs={'class': 'form-control'})
EmailWidget = forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'})
MAX_RESUME_SIZE = 5242880


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
                             widget=EmailWidget)
    

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
    

class LibraryMemberForm(UserCreationForm, BaseMemberForm):
    EDUCATION_LEVELS = (
    (1, _('Master')),
    (2, _('Doctor or PhD')),
    (3, _('Postgraduate')),
    (4, _('Doctorate'))
    )
    class Meta:
        model = LibraryMember
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'password_reveal',
                  'institution', 'department', 'specialization', 'education_level', 'supervisor', 'google_scholar',
                  'resume', 'resource_plans')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].validators.append(validate_password)
        self.fields['password_reveal'].widget.attrs.update({'onclick': 'togglePassword()'})
        
    def save(self, commit=True):
        member = super(LibraryMemberForm, self).save(commit=False)
        member.set_password(self.cleaned_data['password1'])
        member.specialization_code = self.cleaned_data['specialization_code']
        
        if commit:
            member.save()
        return member
    
    def clean(self):
        cleaned_data = super().clean()
        education_level = cleaned_data.get('education_level')
        supervisor = cleaned_data.get('supervisor')
        if education_level in ['3', '4'] and not supervisor:
            self.add_error('supervisor', _("This field is required for education levels 'Postgraduate' and 'Doctorate'."))
            
        resume = self.cleaned_data.get('resume', False)
        if resume:
            if resume.size > 5 * 1024 * 1024:
                self.add_error('resume', _('Resume file size must be under 5MB.'))
    
    phone_number = PhoneNumberField(label=_('Phone'),
                                    widget=PhoneNumberWidget)
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password_field', 'type': 'password'}))
    password2 = forms.CharField(label=_('Password confirmation'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password_conf_field', 'type': 'password'}))
    password_reveal = forms.BooleanField(label=_('Show password'),
                                         required=False,
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'password-toggle'}))
    institution = forms.CharField(label=_('Higher Education or Research Institution'),
                                  max_length=200,
                                  widget=TextInputWidget)
    department = forms.CharField(label=_('Research Unit/Department/Chair'),
                                 max_length=200,
                                 widget=TextInputWidget)
    specialization = forms.CharField(label=_('Scientific Specialization'),
                                     max_length=200,
                                     widget=forms.TextInput(attrs={
                                         'type': 'text', 
                                         'class': 'form-control',
                                         'placeholder': _('Specialty name')
                                         }),
                                     )
    specialization_code = forms.IntegerField(validators=[MinValueValidator(100), ],
                                             widget=forms.TextInput(attrs={
                                                 'class': 'form-control',
                                                 'placeholder': _('Code')
                                                 })
                                             )
    education_level = forms.ChoiceField(label = _('Level of education'),
                                        choices=EDUCATION_LEVELS,
                                        widget=SelectWidget)
    supervisor = forms.CharField(label=_('Academic Supervisor/Consultant'),
                                 max_length=200,
                                 widget=TextInputWidget,
                                 required=False)
    resource_plans = forms.CharField(label=_('How do you plan to use the sources of ERGOSUM European Library?'),
                                     max_length=600,
                                     widget=forms.Textarea(attrs={'type': 'text', 'class': 'form-control', 'style': 'max-height: 90px'}))
    google_scholar = forms.CharField(label='ORCHID/Google Scholar',
                                     required=False,
                                     max_length=200,
                                     widget=TextInputWidget)


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail',
                             max_length=100,
                             widget=EmailWidget)
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    
class ResourcesFilterForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'max-width: 100%',
            'placeholder': _('Title or Author'),
            'aria-label': 'Search'
        })
    )
    year = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    ) 

    def __init__(self, *args, **kwargs):
        super(ResourcesFilterForm, self).__init__(*args, **kwargs)
        current_year = datetime.date.today().year
        year_choices = [(str(year), str(year)) for year in range(current_year, current_year-80, -1)]
        self.fields['year'].choices = [('', 'All time')] + year_choices