# Generated by Django 4.1 on 2023-04-13 19:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_subresource_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryauthor',
            name='slug',
            field=models.SlugField(default=1, help_text='Slug', unique=True, validators=[django.core.validators.MaxLengthValidator(50)]),
            preserve_default=False,
        ),
    ]