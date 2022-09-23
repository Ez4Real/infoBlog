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

from .tokens import email_unsubscribe_token

class NewsType(models.Model):
    type = models.CharField(help_text='Введіть тип новини',
                            max_length=25,
                            verbose_name='Тип новини')

    class Meta:
        verbose_name_plural = 'Типи новин'

    def __str__(self):
        return f'{self.type}'


class News(models.Model):

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

    title = models.CharField(max_length=45,
                             help_text='Введіть заголовок новини',
                             verbose_name='Заголовок')

    banner = models.ImageField(upload_to='uploads/banners', 
                               verbose_name='Банер новини')
    
    subtitle = models.TextField(max_length=296,
                                help_text='Введіть текст підзаголовку',
                                verbose_name='Підзаголовок')

    content = RichTextUploadingField(help_text='Введіть зміст новини',
                                  verbose_name='Зміст')

    type = models.ForeignKey(NewsType,
                             on_delete=models.PROTECT,
                             help_text='Оберіть тип новини',
                             verbose_name='Тип',
                             default='News')

    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name='Дата створення')

    class Meta:
        ordering = ['title', 'type', 'date_of_creation']
        verbose_name_plural = 'Новини'

    def __str__(self):
        return f'{self.title}'

    def send(self, request):
        context = {}
        context['domain'] = get_current_site(request).domain
        context['protocol'] = 'https' if request.is_secure() else 'http'
        context['date'] = self.date_of_creation
        context['subtitle'] = self.subtitle
        context['type'] = self.type
        context['pk'] = self.pk
        
        subscribers = Subscriber.objects.filter(is_active=True)
        mail_subject = self.title
        
        for sub in subscribers:
            context['uid'] = urlsafe_base64_encode(force_bytes(sub.pk))
            context['token'] = email_unsubscribe_token.make_token(sub)
            if self.banner.url:
                img_url = self.banner.url
                print(img_url)
                context['img_url'] = img_url
                img = Image.open(requests.get(img_url, stream=True).raw)
                print(img)
                byte_buffer = BytesIO()
                img.save(byte_buffer, 'png')
                print('SAVE', img)
                print(img.format)
                img = MIMEImage(byte_buffer.getvalue())
                img.add_header('Content-ID', f'<{img_url}>')

            message = get_template('blog/newsletter/news.html').render(context)
            email = EmailMessage(mail_subject, message, to=[sub.email])
            email.content_subtype = 'html'
            if img_url: email.attach(img)
            email.send()


class Subscriber(models.Model):
    email = models.EmailField(unique=True,
                              max_length=254,
                              help_text='Введіть email')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Електронні пошти підписників'

    def __str__(self):
        return self.email + " (" + ("not " if not self.is_active else "") + "confirmed)"


class Video(models.Model):
    video = RichTextUploadingField(help_text='Введіть зміст відео',
                                   verbose_name='Зміст')
    date_of_creation = models.DateTimeField(auto_now_add=True,
                                            verbose_name='Дата створення')

    class Meta:
        verbose_name_plural = 'Відеоконтент'

    def __str__(self):
        return self.video
