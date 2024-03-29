# Generated by Django 4.1.2 on 2022-10-04 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('session_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversionExclusionsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=2000, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pixel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pixel_id', models.CharField(max_length=7000, unique=True)),
                ('pixel_type', models.CharField(choices=[('facebook', 'facebook'), ('tiktok', 'tiktok')], max_length=1000)),
                ('conv_api_token', models.CharField(blank=True, max_length=7000, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='session_management.category')),
            ],
        ),
    ]
