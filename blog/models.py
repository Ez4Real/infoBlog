import requests
from PIL import Image
from io import BytesIO
from email.mime.image import MIMEImage

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from .tokens import email_unsubscribe_token


class NewsType(models.Model):
    NEWS_TYPES = [
        ('Opinion', 'Opinion'),
        ('Events', 'Events'),
        ('News', 'News'),
        ('Op-eds', 'Op-eds'),
        ('Analytics', 'Analytics'),
    ]
    
    class Meta:
        verbose_name_plural = _('News Types')
        
    def __str__(self):
        return self.type
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.type.lower())
        super(NewsType, self).save(*args, **kwargs)
    
    type = models.CharField(help_text='Enter news type',
                            max_length=25,
                            unique=True,
                            verbose_name=_('News type'),
                            choices=NEWS_TYPES)
    
    slug = models.SlugField(help_text='Slug',
                            unique=True,)
    

class PolicyArea(models.Model):
    class Meta:
        verbose_name_plural = _('Policy areas')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.lower())
        super(PolicyArea, self).save(*args, **kwargs)
    
    name = models.CharField(help_text='Enter policy area name',
                            max_length=25,
                            unique=True,
                            verbose_name=_('Policy area name'))
    
    slug = models.SlugField(unique=True)


class Person(models.Model):
    class Meta:
        ordering = ['-date_of_creation']
    
    def __str__(self):
        return f'{self.en_full_name} - {self.uk_full_name}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.en_full_name.lower())
        super(Person, self).save(*args, **kwargs)
    
    def get_all_objects(self):
        return self._meta.model.objects.all()
    
    image = models.ImageField(upload_to='uploads/blog-scholars', 
                              verbose_name=_('Photo of the represent')
                              )
    en_full_name = models.CharField(max_length=45,
                                    help_text='Enter full name on english',
                                    verbose_name=_('Full name on english')
                                    )
    uk_full_name = models.CharField(max_length=45,
                                    help_text='Enter full name on ukrainian',
                                    verbose_name=_('Full name on ukrainian')
                                    )
    en_position = models.TextField(max_length=255,
                                   help_text='Enter position',
                                   verbose_name=_('English position')
                                   )
    uk_position = models.TextField(max_length=255,
                                   help_text='Enter position',
                                   verbose_name=_('Ukrainian position')
                                   )
    slug = models.SlugField(unique=True)
    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name=_('Date of creation'))
        

class BlogScholar(Person):
    class Meta:
        verbose_name_plural = _('Blog Scholars')
        
    def get_scholar_posts(self):
        return reverse('scholar-posts', args=[self.slug])
    
    link = models.URLField(help_text='Enter link',
                           max_length = 200,
                           verbose_name=_('University link'))


class TeamMember(Person):
    class Meta:
        verbose_name_plural = _('Team Members')
        
    def get_absolute_url(self):
        return reverse('team-member-detail', args=[self.slug])
    
    en_content = RichTextUploadingField(help_text='Enter news content',
                                        verbose_name=_('English content')
                                        )
    uk_content = RichTextUploadingField(help_text='Enter news content',
                                        verbose_name=_('Ukrainian content')
                                        )


class LibraryMemberManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email address is required')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user


class LibraryMember(AbstractBaseUser):
    class Meta:
        verbose_name_plural = _('Library members')
        ordering = ['-date_of_creation', 'last_name']

    EDUCATION_LEVELS = (
    ('1', _('Master')),
    ('2', _('Doctor or PhD')),
    ('3', _('Postgraduate')),
    ('4', _('Doctorate'))
    )
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    first_name = models.CharField(verbose_name=_('First name'),
                                  max_length=100)
    last_name = models.CharField(verbose_name=_('Last name'),
                                 max_length=100)
    email = models.EmailField(unique=True,
                              verbose_name='E-mail',
                              max_length=100)
    phone_number = models.CharField(unique=True,
                                    verbose_name=_('Phone number'),
                                    max_length=20)
    institution = models.CharField(verbose_name=_('Higher Education or Research Institution'),
                                   max_length=200)
    department = models.CharField(verbose_name=_('Research Unit/Department/Chair'),
                                  max_length=200)
    specialization = models.CharField(verbose_name=_('Scientific Specialization'),
                                      max_length=200)
    specialization_code = models.PositiveIntegerField(validators=[MinValueValidator(100)])
    education_level = models.CharField(verbose_name = _('Level of education'),
                                       choices=EDUCATION_LEVELS,
                                       max_length=1)
    supervisor = models.CharField(verbose_name=_('Academic Supervisor/Consultant'),
                                  max_length=200,
                                  null=True,
                                  blank=True)
    google_scholar = models.CharField(verbose_name='ORCHID/Google Scholar',
                                      max_length=200,
                                      blank=True,
                                      null=True)
    resume = models.FileField(verbose_name=_('Academic CV'),
                              upload_to='uploads/Library Members Resumes',
                              blank=True,
                              null=True)
    resource_plans = models.TextField(verbose_name=_('Resource Plans'),
                                      max_length=600)
    date_of_creation = models.DateTimeField(verbose_name=_('Date of creation'),
                                            auto_now_add=True)

    objects = LibraryMemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'institution',
                       'department', 'specialization', 'education_level', 'resource_plans']


class Article(models.Model):
    class Meta:
        ordering = ['-date_of_creation', 'en_title']
        
    def __str__(self):
        return f'{self.en_title} - {self.date_of_creation}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.en_title.lower())[:50]
        super(Article, self).save(*args, **kwargs)
        
    slug = models.SlugField(help_text='Slug',
                            unique=True,
                            validators=[MaxLengthValidator(50)])
    
    en_title = models.CharField(max_length=100,
                                help_text='Enter news title',
                                verbose_name=_('English title')
                                )
    uk_title = models.CharField(max_length=100,
                                help_text='Enter news title',
                                verbose_name=_('Ukrainian title')
                                )
    en_content = RichTextUploadingField(help_text='Enter news content',
                                        verbose_name=_('English content')
                                        )
    uk_content = RichTextUploadingField(help_text='Enter news content',
                                        verbose_name=_('Ukrainian content')
                                        )
    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name=_('Date of creation'))
    
    
class Blog(Article):
    class Meta:
        verbose_name_plural = _('Blog Articles')
        
    def get_absolute_url(self):
        return reverse('blog-post-detail', args=[self.author.slug, self.slug])
    
    author = models.ForeignKey(BlogScholar,
                               on_delete=models.PROTECT,
                               help_text='Choose blog scholar',
                               verbose_name=_('Author')
                               )


class News(Article):
    class Meta:
        verbose_name_plural = _('News')
        
    def get_absolute_url(self):
        return reverse('post-detail', args=[self.type.slug, self.slug]) 

    banner = models.ImageField(upload_to='uploads/banners', 
                               verbose_name=_('News banner')
                               )
    
    en_subtitle = models.TextField(max_length=100,
                                   help_text='Enter subtitle',
                                   verbose_name=_('English subtitle')
                                   )
    uk_subtitle = models.TextField(max_length=100,
                                   help_text='Enter subtitle',
                                   verbose_name=_('Ukrainian subtitle')
                                   )
    
    type = models.ForeignKey(NewsType,
                             on_delete=models.PROTECT,
                             help_text='Choose news type',
                             verbose_name=_('Type'),
                             default='News')
    policy_area = models.ForeignKey(PolicyArea,
                                    on_delete=models.PROTECT,
                                    help_text='Choose policy area',
                                    verbose_name=_('Policy area'),
                                    default='Foreign policy')
    author = models.ForeignKey(TeamMember,
                               on_delete=models.PROTECT,
                               help_text='Select an author if needed',
                               verbose_name=_('Author'),
                               blank=True,
                               null=True)
    
    def send(self, request):
        context = {}
        context['domain'] = get_current_site(request).domain
        context['protocol'] = 'https' if request.is_secure() else 'http'
        context['date'] = self.date_of_creation
        context['type'] = self.type.slug
        context['slug'] = self.slug
        
        subscribers = Subscriber.objects.filter(is_active=True)
        for sub in subscribers:
            context['uid'] = urlsafe_base64_encode(force_bytes(sub.pk))
            context['token'] = email_unsubscribe_token.make_token(sub)
            if self.banner.url:
                img_url = self.banner.url
                context['img_url'] = img_url
                img = Image.open(requests.get(f'{img_url[:52]}c_scale,r_15,w_600/{img_url[52:]}', stream=True).raw)
                byte_buffer = BytesIO()
                img.save(byte_buffer, 'png')
                img = MIMEImage(byte_buffer.getvalue())
                img.add_header('Content-ID', f'<{img_url}>')
            match sub.mailing_language:
                case 'en':
                    mail_subject = self.en_title
                    context['subtitle'] = self.en_subtitle
                case 'uk':
                    mail_subject = self.uk_title
                    context['subtitle'] = self.uk_subtitle
                
            message = get_template('blog/newsletter/news.html').render(context)
            email = EmailMessage(mail_subject, message, to=[sub.email])
            email.content_subtype = 'html'
            if img_url: email.attach(img)
            email.send()

class Subscriber(models.Model):
    class Meta:
        verbose_name_plural = _('Subscribers')
        ordering = ['-date_of_creation', 'email']

    def __str__(self):
        return self.email + " (" + ("not " if not self.is_active else "") + "confirmed)"
    
    email = models.EmailField(unique=True,
                              max_length=255
                              )
    is_active = models.BooleanField(default=False,
                                    verbose_name=_('Is Active'))
    mailing_language = models.CharField(max_length=2,
                                        choices=[('en', _('English')),
                                                 ('uk', _('Ukrainian'))])
    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name=_('Date of creation'))


class Video(models.Model):
    MEDIA_CHOICES = (
        ('pc', 'Podcasts'),
        ('vd', 'Videos')
    )
    
    class Meta:
        verbose_name_plural = _('Video content')
        ordering = ['-date_of_creation', 'type']
    
    def __str__(self):
        return self.en_title
    
    def save(self, *args, **kwargs):
        self.url = self.url.split('/')[-1]
        super(Video, self).save(*args, **kwargs)

    
    en_title = models.CharField(max_length=100,
                                help_text='Enter video title',
                                verbose_name=_('English title'))
    uk_title = models.CharField(max_length=100,
                                help_text='Enter video title',
                                verbose_name=_('Ukrainian title'))
    type = models.CharField(max_length=2,
                            help_text='Choose video type',
                            choices=MEDIA_CHOICES)
    url = models.URLField(help_text='Video URL path',
                          max_length = 200,
                          verbose_name=('URL'))
    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name=_('Date of creation'))
    

class ResourceType(models.Model):
    RESOURCE_TOPICS = [
        ('Journals', 'Journals'),
        ('Magazines', 'Magazines'),
        ('Books', 'Books'),
        ('Newspapers', 'Newspapers'),
        ('Brochures', 'Brochures'),
        ('Other papers', 'Other papers'),
    ]
    
    type = models.CharField(max_length=20, choices=RESOURCE_TOPICS, default='Journals')
    
    banner = models.ImageField(upload_to='uploads/library_banners', 
                               verbose_name=_('Resource banner')
                               )
    
    def __str__(self):
        return f'{self.type}'
    
    def get_absolute_url(self):
        if self.type == 'Books':
            return reverse('book-list')
        else: return reverse('cover-list', args=[self.type])
    

class LibraryAuthor(models.Model):
    slug = models.SlugField(help_text='Slug',
                            unique=True,
                            validators=[MaxLengthValidator(50)])
    en_full_name = models.CharField(max_length=45,
                                    help_text='Enter full name on english',
                                    verbose_name=_('Full name on english'),
                                    unique=True
                                    )
    uk_full_name = models.CharField(max_length=45,
                                    help_text='Enter full name on ukrainian',
                                    verbose_name=_('Full name on ukrainian')
                                    )
    
    def __str__(self):
        return f'{self.en_full_name}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.en_full_name.lower())[:50]
        super(LibraryAuthor, self).save(*args, **kwargs)


class LibraryResource(Article):
    type = models.ForeignKey(ResourceType,
                             on_delete=models.CASCADE,
                             related_name='resources',
                             help_text='Choose resource type',
                             verbose_name=_('Resource type'),
                            )
    banner = models.ImageField(upload_to='uploads/library_banners', 
                               verbose_name=_('Resource banner')
                               )
    author = models.ForeignKey(LibraryAuthor,
                               on_delete=models.CASCADE,
                               related_name='books',
                               help_text=_('Only for Books.'),
                               verbose_name=_('Author'),
                               blank=True,
                               null=True
                               )
    file = models.FileField(upload_to='uploads/resources', 
                            verbose_name=_('Resource file'),
                            blank=True,
                            null=True,
                            help_text=_('Only for Books, Brochures and other.')
                            )
    pages = models.PositiveIntegerField(blank=True,
                                        null=True,
                                        help_text=_('Only for Books.')
                                        )
    date = models.DateField(default=now,
                            verbose_name=_('Date of creation'))
    
    def __str__(self):
        return f'{self.type} - {self.en_title}'
    
    def get_absolute_url(self):
        if self.type.type == 'Books':
            return reverse('book-detail', args=[self.slug])
        else: return reverse('cover-detail', args=[self.type, self.slug])

class Subresource(models.Model):
    file = models.FileField(upload_to='uploads/subresources', 
                            verbose_name=_('Subresource file')
                            )
    date = models.DateField(default=now,
                            verbose_name=_('Date of creation'))
    topic = models.CharField(max_length=45,
                             help_text='Enter topic',
                             verbose_name=_('Topic'),
                             unique=True)
    bounded_resource = models.ForeignKey(LibraryResource,
                                         on_delete=models.CASCADE,
                                         related_name='subresources',
                                         help_text='Choose bounded resource',
                                         verbose_name=_('Bounded resource'),
                                        )