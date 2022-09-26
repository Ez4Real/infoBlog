<<<<<<< HEAD
# Generated by Django 4.1 on 2022-09-26 16:47
=======
# Generated by Django 4.1 on 2022-09-19 10:54
>>>>>>> 26bcdfd51c40bd14c360a7aa850e83eb01b1a09b

import ckeditor_uploader.fields
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
                ('type', models.CharField(help_text='Enter news type', max_length=25, verbose_name='News type')),
            ],
            options={
                'verbose_name_plural': 'News Types',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Enter e-mail', max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Subscribers e-mails',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', ckeditor_uploader.fields.RichTextUploadingField(help_text='Upload video', verbose_name='Content')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
            ],
            options={
                'verbose_name_plural': 'Video content',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('en_title', models.CharField(help_text='Enter news title', max_length=45, verbose_name='English title')),
                ('uk_title', models.CharField(help_text='Enter news title', max_length=45, verbose_name='Ukrainian title')),
                ('banner', models.ImageField(upload_to='uploads/banners', verbose_name='News banner')),
                ('en_subtitle', models.TextField(help_text='Enter subtitle', max_length=296, verbose_name='English subtitle')),
                ('uk_subtitle', models.TextField(help_text='Enter subtitle', max_length=296, verbose_name='Ukrainian subtitle')),
                ('en_content', ckeditor_uploader.fields.RichTextUploadingField(help_text='Enter news content', verbose_name='English content')),
                ('uk_content', ckeditor_uploader.fields.RichTextUploadingField(help_text='Enter news content', verbose_name='Ukrainian content')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('type', models.ForeignKey(default='News', help_text='Choose news type', on_delete=django.db.models.deletion.PROTECT, to='blog.newstype', verbose_name='Type')),
=======
                ('title', models.CharField(help_text='Введіть заголовок новини', max_length=45, verbose_name='Заголовок')),
                ('banner', models.ImageField(upload_to='uploads/banners', verbose_name='Банер новини')),
                ('subtitle', models.TextField(help_text='Введіть текст підзаголовку', max_length=1000, verbose_name='Підзаголовок')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(help_text='Введіть зміст новини', verbose_name='Зміст')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('type', models.ForeignKey(default='News', help_text='Оберіть тип новини', on_delete=django.db.models.deletion.PROTECT, to='blog.newstype', verbose_name='Тип')),
>>>>>>> 26bcdfd51c40bd14c360a7aa850e83eb01b1a09b
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ['en_title', 'type', 'date_of_creation'],
            },
        ),
    ]
