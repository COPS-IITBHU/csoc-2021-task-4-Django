# Generated by Django 2.2.1 on 2021-07-21 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210721_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookrate',
            old_name='book',
            new_name='book_rated',
        ),
    ]