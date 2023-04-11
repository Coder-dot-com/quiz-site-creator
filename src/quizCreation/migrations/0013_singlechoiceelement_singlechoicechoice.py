# Generated by Django 4.1.8 on 2023-04-11 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0012_userquiz_analytics_scripts'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleChoiceElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='SingleChoiceChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=300)),
                ('single_choice_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.singlechoiceelement')),
            ],
        ),
    ]