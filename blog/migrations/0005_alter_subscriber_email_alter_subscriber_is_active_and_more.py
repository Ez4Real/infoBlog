# Generated by Django 4.1 on 2023-02-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_librarymember_alter_article_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='mailing_language',
            field=models.CharField(choices=[('en', 'English'), ('uk', 'Ukrainian')], max_length=2),
        ),
    ]
