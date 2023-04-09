# Generated by Django 4.1 on 2023-04-08 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_newstype_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryresource',
            name='file',
            field=models.FileField(blank=True, help_text='Only for Brochures or Other papers.', null=True, upload_to='uploads/subresources', verbose_name='Resource file'),
        ),
        migrations.AlterField(
            model_name='subresource',
            name='file',
            field=models.FileField(upload_to='uploads/subresources', verbose_name='Subresource file'),
        ),
    ]
