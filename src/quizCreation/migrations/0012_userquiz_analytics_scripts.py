# Generated by Django 4.1.8 on 2023-04-10 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0011_emailinputelement_use_as_email_for_conversion_tracking_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquiz',
            name='analytics_scripts',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]