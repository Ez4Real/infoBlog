import datetime

from django.db import models
from django.urls import reverse


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
    
    text_content = models.TextField(help_text='Введіть зміст новини',
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


class UserEmail(models.Model):
    email = models.EmailField(max_length = 254,
                              help_text='Введіть email',
                              unique=True)
    
    class Meta:
        verbose_name_plural = 'Електронні пошти розсилки'
        
    def __str__(self):
        return f'{self.email}'