# Generated by Django 4.1.8 on 2023-04-12 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0015_multiplechoicechoice_image_singlechoicechoice_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreeDisagree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
    ]