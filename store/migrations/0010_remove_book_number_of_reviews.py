# Generated by Django 2.2.1 on 2021-07-22 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_ratingsystem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='number_of_reviews',
        ),
    ]