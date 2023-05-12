# Generated by Django 4.1.8 on 2023-05-12 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0032_userquiz_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
    ]
