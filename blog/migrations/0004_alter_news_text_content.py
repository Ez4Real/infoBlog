# Generated by Django 4.0.6 on 2022-07-30 16:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_news_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='text_content',
            field=ckeditor.fields.RichTextField(help_text='Введіть зміст новини', verbose_name='Зміст'),
        ),
    ]
