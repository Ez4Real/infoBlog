import requests
from PIL import Image
from io import BytesIO
from email.mime.image import MIMEImage

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _

from .tokens import email_unsubscribe_token


class NewsType(models.Model):
    type = models.CharField(help_text='Enter news type',
                            max_length=25,
                            unique=True,
                            verbose_name=_('News type'))
    
    slug = models.SlugField(help_text='Slug',
                            unique=True,)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.type.lower())
        super(NewsType, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = _('News Types')

    def __str__(self):
        return f'{self.type}'


class PolicyArea(models.Model):
    name = models.CharField(help_text='Enter policy area name',
                            max_length=25,
                            unique=True,
                            verbose_name=_('Policy area name'))
    class Meta:
        verbose_name_plural = _('Policy areas')

    def __str__(self):
        return f'{self.name}'

class News(models.Model):

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.type.slug, self.slug])

    en_title = models.CharField(max_length=45,
                                help_text='Enter news title',
                                verbose_name=_('English title')
                                )
    uk_title = models.CharField(max_length=45,
                                help_text='Enter news title',
                                verbose_name=_('Ukrainian title')
                                )

    banner = models.ImageField(upload_to='uploads/banners', 
                               verbose_name=_('News banner')
                               )
    
    en_subtitle = models.TextField(max_length=300,
                                   help_text='Enter subtitle',
                                   verbose_name=_('English subtitle')
                                   )
    uk_subtitle = models.TextField(max_length=300,
                                   help_text='Enter subtitle',
                                   verbose_name=_('Ukrainian subtitle')
                                   )

    en_content = RichTextUploadingField(help_text='Enter news content',
                                        verbose_name=_('English content')
                                        )
    uk_content = RichTextUploadingField(help_text='Enter news content',
                                        verbose_name=_('Ukrainian content')
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
    
    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name=_('Date of creation'))

    slug = models.SlugField(help_text='Slug',
                            unique=True,)

    class Meta:
        ordering = ['en_title', 'uk_title', 'type', 'date_of_creation']
        verbose_name_plural = _('News')

    def __str__(self):
        return f'{self.en_title}, {self.uk_title}, {self.date_of_creation}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.en_title.lower())
        super(News, self).save(*args, **kwargs)

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
    email = models.EmailField(unique=True,
                              max_length=254,
                              help_text='Enter e-mail')
    is_active = models.BooleanField(default=False)
    mailing_language = models.CharField(max_length=2,
                                        help_text='Choose mailing language',
                                        choices=[('en', _('English')),
                                                 ('uk', _('Ukrainian'))])

    class Meta:
        verbose_name_plural = _('Subscribers e-mails')

    def __str__(self):
        return self.email + " (" + ("not " if not self.is_active else "") + "confirmed)"


class Video(models.Model):
    PODCAST = 'pc'
    VIDEO = 'vd'
    MEDIA_CHOICES = (
        (PODCAST, 'Podcasts'),
        (VIDEO, 'Videos')
    )
    en_title = models.CharField(max_length=45,
                                help_text='Enter video title',
                                verbose_name=_('English title'))
    uk_title = models.CharField(max_length=45,
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
    
    def save(self, *args, **kwargs):
        self.url = self.url.split('/')[-1]
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.en_title
    
    class Meta:
        verbose_name_plural = _('Video content')
