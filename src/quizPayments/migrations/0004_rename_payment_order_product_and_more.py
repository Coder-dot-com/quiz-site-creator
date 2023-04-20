# Generated by Django 4.1.8 on 2023-04-20 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizPayments', '0003_alter_product_name_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='email',
            new_name='shipping_email',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_total',
            new_name='total',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_number',
        ),
        migrations.AddField(
            model_name='order',
            name='currency_code',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('On hold', 'On hold')], default='New', max_length=10),
        ),
    ]