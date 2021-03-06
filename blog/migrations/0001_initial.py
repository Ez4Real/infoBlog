# Generated by Django 4.0.6 on 2022-08-01 15:58

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='Введіть тип новини', max_length=25, verbose_name='Тип новини')),
            ],
            options={
                'verbose_name_plural': 'Типи новин',
            },
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Введіть email', max_length=254, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Електронні пошти розсилки',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введіть заголовок новини', max_length=45, verbose_name='Заголовок')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(help_text='Введіть зміст новини', verbose_name='Зміст')),
                ('date_of_creation', models.DateField(default=datetime.date.today, help_text='Введіть дату створення новини', verbose_name='Дата створення')),
                ('type', models.ForeignKey(default='News', help_text='Оберіть тип новини', on_delete=django.db.models.deletion.PROTECT, to='blog.newstype', verbose_name='Тип')),
            ],
            options={
                'verbose_name_plural': 'Новини',
                'ordering': ['title', 'type'],
            },
        ),
    ]
