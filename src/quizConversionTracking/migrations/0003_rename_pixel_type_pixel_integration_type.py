# Generated by Django 4.1.8 on 2023-04-16 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizConversionTracking', '0002_alter_pixel_conv_api_token_alter_pixel_pixel_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pixel',
            old_name='pixel_type',
            new_name='integration_type',
        ),
    ]