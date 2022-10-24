# Generated by Django 4.1 on 2022-10-24 18:26

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
                ('type', models.CharField(help_text='Enter news type', max_length=25, unique=True, verbose_name='News type')),
                ('slug', models.SlugField(help_text='Slug', unique=True)),
            ],
            options={
                'verbose_name_plural': 'News Types',
            },
        ),
        migrations.CreateModel(
            name='PolicyArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter policy area name', max_length=25, unique=True, verbose_name='News type')),
            ],
            options={
                'verbose_name_plural': 'Policy areas',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Enter e-mail', max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('mailing_language', models.CharField(choices=[('en', 'English'), ('uk', 'Ukrainian')], default='en', max_length=2)),
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
                ('en_title', models.CharField(help_text='Enter news title', max_length=45, verbose_name='English title')),
                ('uk_title', models.CharField(help_text='Enter news title', max_length=45, verbose_name='Ukrainian title')),
                ('banner', models.ImageField(upload_to='uploads/banners', verbose_name='News banner')),
                ('en_subtitle', models.TextField(help_text='Enter subtitle', max_length=296, verbose_name='English subtitle')),
                ('uk_subtitle', models.TextField(help_text='Enter subtitle', max_length=296, verbose_name='Ukrainian subtitle')),
                ('en_content', ckeditor_uploader.fields.RichTextUploadingField(help_text='Enter news content', verbose_name='English content')),
                ('uk_content', ckeditor_uploader.fields.RichTextUploadingField(help_text='Enter news content', verbose_name='Ukrainian content')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('slug', models.SlugField(help_text='Slug', unique=True)),
                ('policy_area', models.ForeignKey(default='News', help_text='Choose policy area', on_delete=django.db.models.deletion.PROTECT, to='blog.policyarea', verbose_name='Type')),
                ('type', models.ForeignKey(default='News', help_text='Choose news type', on_delete=django.db.models.deletion.PROTECT, to='blog.newstype', verbose_name='Type')),
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ['en_title', 'uk_title', 'type', 'date_of_creation'],
            },
        ),
    ]
