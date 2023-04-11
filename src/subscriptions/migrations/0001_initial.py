# Generated by Django 4.1.2 on 2022-10-29 21:23

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import subscriptions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tiers', '0001_initial'),
        ('multicurrency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('renewal_frequency', models.CharField(choices=[('monthly', 'monthly'), ('annually', 'annually')], max_length=300)),
                ('stripe_renewal_frequency', models.CharField(choices=[('month', 'month'), ('year', 'year')], max_length=300, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('price_before_sale', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=300, null=True)),
                ('subscription_name', models.CharField(max_length=300, null=True)),
                ('feature_list', models.TextField(blank=True, default='\n\n                                        <div class="plan-features mt-4">\n                                            <p class="font-size-15"><i class="mdi mdi-checkbox-marked-circle text-success font-size-16 me-2 align-middle"></i><b>Unlimited</b>\n                                                Target Audience</p>\n                                            <p class="font-size-15"><i class="mdi mdi-checkbox-marked-circle text-success font-size-16 me-2 align-middle"></i><b>1</b>\n                                                User Account</p>\n                                            <p class="font-size-15"><i class="mdi mdi-checkbox-marked-circle text-success font-size-16 me-2 align-middle"></i><b>100+</b>\n                                                Video Tuts</p>\n                                            <p class="font-size-15"><i class="mdi mdi-close-circle text-danger font-size-16 me-2 align-middle"></i><b>Public</b>\n                                                Displays\n                                            </p>\n                                        </div>\n    ', max_length=10000, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('create_nonusd_subscriptions', models.BooleanField(default=False)),
                ('has_badge', models.BooleanField(default=False)),
                ('badge_color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=None)),
                ('badge_text_color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=None)),
                ('badge_text', models.CharField(blank=True, max_length=100, null=True)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='multicurrency.currency')),
                ('tier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tiers.tier')),
            ],
        ),
        migrations.CreateModel(
            name='UserPaymentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('free_trial', 'free_trial'), ('active', 'active'), ('free', 'free'), ('beta_tester', 'beta_tester')], max_length=300)),
                ('subscription_expiry', models.DateTimeField(blank=True, null=True)),
                ('add_free_trial_days', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_synced', models.DateTimeField(default=subscriptions.models.default_date_time)),
                ('tier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tiers.tier')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('created', 'created'), ('paid', 'paid'), ('unpaid', 'unpaid'), ('cancelled', 'cancelled'), ('downgraded', 'downgraded'), ('upgraded', 'upgraded')], max_length=300)),
                ('date_subscribed', models.DateTimeField(auto_now_add=True)),
                ('stripe_customer_id', models.CharField(max_length=300)),
                ('payment_intent_id', models.CharField(blank=True, max_length=300, null=True)),
                ('subscription_id', models.CharField(blank=True, max_length=300, null=True)),
                ('interval_start_date', models.DateTimeField(blank=True, null=True)),
                ('next_due', models.DateTimeField()),
                ('payment_method', models.CharField(max_length=300)),
                ('amount_subscribed', models.DecimalField(decimal_places=2, max_digits=7)),
                ('renewal_frequency', models.CharField(max_length=300)),
                ('currency_code', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('latest_response', models.CharField(blank=True, max_length=5000, null=True)),
                ('subscription_confirmation_email_sent', models.BooleanField(default=False)),
                ('subscription_choice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.subscriptionchoices')),
                ('user_payment_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.userpaymentstatus')),
            ],
        ),
    ]
