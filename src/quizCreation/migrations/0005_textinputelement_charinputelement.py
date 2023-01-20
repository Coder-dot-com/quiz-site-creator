# Generated by Django 4.1.5 on 2023-01-20 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0004_quizpage_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextInputElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='CharInputElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
    ]
