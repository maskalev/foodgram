# Generated by Django 3.2.4 on 2021-06-19 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='title',
            new_name='name',
        ),
    ]
