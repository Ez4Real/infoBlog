import datetime

from django.db import models
from django.urls import reverse
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class NewsType(models.Model):
    
    type = models.CharField(help_text='Введіть тип новини',
                            max_length=25,
                            verbose_name = 'Тип новини')
    
    class Meta:
        verbose_name_plural = 'Типи новин'
    
    def __str__(self):
        return f'{self.type}'      


class News(models.Model):

    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])
    
    title = models.CharField(max_length=45, 
                             help_text='Введіть заголовок новини',
                             verbose_name = 'Заголовок')
    
    text = RichTextUploadingField(help_text='Введіть зміст новини',
                                  verbose_name = 'Зміст')
    
    type = models.ForeignKey(NewsType, 
                             on_delete=models.PROTECT,
                             help_text='Оберіть тип новини',
                             verbose_name = 'Тип',
                             default='News')
    
    date_of_creation = models.DateField(help_text = 'Введіть дату створення новини', 
                                        default=datetime.date.today,
                                        verbose_name = 'Дата створення')
    
    class Meta:
        ordering = ['title', 'type']
        verbose_name_plural = 'Новини'
        
    def __str__(self):
        return f'{self.title}'
    
    def send(self, request):
        subscribers = Subscriber.objects.filter(confirmed=True)
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        for sub in subscribers:
            message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=sub.email,
                    subject=self.title,
                    html_content=self.text + (
                        '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                            request.build_absolute_uri(),
                            sub.email,
                            sub.conf_num))
            sg.send(message)
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True,
                              max_length = 254,
                              help_text='Введіть email')
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Електронні пошти підписників'

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"
    

class Video(models.Model):
    video = RichTextUploadingField(help_text='Введіть зміст відео',
                                   verbose_name = 'Зміст')
    
    class Meta:
        verbose_name_plural = 'Відеоконтент'
        
    def __str__(self):
        return self.video
    