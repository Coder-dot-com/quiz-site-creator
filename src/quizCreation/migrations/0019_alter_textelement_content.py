# Generated by Django 4.1.8 on 2023-04-14 14:48

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizCreation', '0018_alter_agreedisagreerow_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textelement',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]