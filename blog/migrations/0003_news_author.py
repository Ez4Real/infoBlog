# Generated by Django 4.1 on 2023-02-02 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_teammember'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.ForeignKey(default=12, help_text='Select an author if needed', on_delete=django.db.models.deletion.PROTECT, to='blog.teammember', verbose_name='Author'),
            preserve_default=False,
        ),
    ]
