# Generated by Django 4.1.5 on 2023-01-03 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0003_textelement_quizpageelement_page_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizpage',
            name='name',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
