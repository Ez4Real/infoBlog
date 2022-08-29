from bs4 import BeautifulSoup
from ckeditor_uploader.fields import RichTextUploadingField
from email.mime.image import MIMEImage

from django.db import models
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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

    text = RichTextUploadingField(help_text='Введіть зміст новини',
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
        subscribers = Subscriber.objects.filter(is_active=True)
        mail_subject = self.title
        soup = BeautifulSoup(self.text, "html.parser")
        img_tags = soup.findAll('img')
        for sub in subscribers:
            if img_tags:
                img_path = img_tags[0]['src']
                with open(img_path[1:], 'rb') as f:
                    img_data = f.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', f'<{img_path}>')
                img_tags[0]['src'] = f'cid:{img_path}'
                for tag in img_tags[1:]:
                    tag.decompose()

            message = get_template('blog/newsletter/news.html').render({
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(sub.pk)),
                'token': email_unsubscribe_token.make_token(sub),
                'protocol': 'https' if request.is_secure() else 'http',
                'date': self.date_of_creation,
                'content': str(soup),
            })
            email = EmailMessage(mail_subject, message, to=[sub.email])
            if img_tags: email.attach(img)
            email.content_subtype = 'html'
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
