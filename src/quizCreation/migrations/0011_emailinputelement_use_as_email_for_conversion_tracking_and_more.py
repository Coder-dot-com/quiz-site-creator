# Generated by Django 4.1.8 on 2023-04-10 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0010_rename_name_quizpage_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailinputelement',
            name='use_as_email_for_conversion_tracking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userquiz',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='user_quiz_logos/'),
        ),
    ]
