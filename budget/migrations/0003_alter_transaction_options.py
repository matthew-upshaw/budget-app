# Generated by Django 4.0.6 on 2022-07-10 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_alter_transaction_transaction_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date_of_transaction']},
        ),
    ]
