# Generated by Django 4.1.8 on 2023-05-15 10:09

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreeDisagree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dropdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuizPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizPageElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpage')),
            ],
        ),
        migrations.CreateModel(
            name='SatisfiedUnsatisfied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='VideoElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('Upload', 'Upload'), ('Youtube', 'Youtube')], max_length=1000, null=True)),
                ('url', models.CharField(blank=True, max_length=1000, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to='user_quiz_videos/')),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuiz',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='user_quiz_logos/')),
                ('analytics_scripts', models.TextField(blank=True, max_length=10000, null=True)),
                ('redirect_url', models.URLField(blank=True, max_length=10000, null=True)),
                ('quiz_confirmation_content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('stripe_public_key', models.CharField(blank=True, max_length=10000, null=True)),
                ('stripe_secret_key', models.CharField(blank=True, max_length=10000, null=True)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_code/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextInputElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='TextElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='SingleChoiceElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='SingleChoiceChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=300)),
                ('is_correct_choice', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='choice_images/')),
                ('single_choice_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.singlechoiceelement')),
            ],
        ),
        migrations.CreateModel(
            name='SatisfiedUnsatisfiedRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('title', models.TextField(max_length=10000)),
                ('required', models.BooleanField(default=False)),
                ('satisfied_unsatisfied_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.satisfiedunsatisfied')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewStars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.AddField(
            model_name='quizpage',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.userquiz'),
        ),
        migrations.CreateModel(
            name='OneToTenElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='NumberInputElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=300)),
                ('is_correct_choice', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='choice_images/')),
                ('multiple_choice_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.multiplechoiceelement')),
            ],
        ),
        migrations.CreateModel(
            name='ImageDisplayElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='user_quiz_images/')),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='EmailInputElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('use_as_email_for_conversion_tracking', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='DropdownChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=300)),
                ('is_correct_choice', models.BooleanField(default=False)),
                ('dropdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.dropdown')),
            ],
        ),
        migrations.AddField(
            model_name='dropdown',
            name='page_element',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement'),
        ),
        migrations.CreateModel(
            name='CharInputElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('required', models.BooleanField(default=False)),
                ('page_element', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement')),
            ],
        ),
        migrations.CreateModel(
            name='AgreeDisagreeRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('title', models.TextField(max_length=10000)),
                ('required', models.BooleanField(default=False)),
                ('agree_disagree_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.agreedisagree')),
            ],
        ),
        migrations.AddField(
            model_name='agreedisagree',
            name='page_element',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizCreation.quizpageelement'),
        ),
    ]
