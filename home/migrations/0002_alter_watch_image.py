# Generated by Django 5.1.7 on 2025-04-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='image',
            field=models.ImageField(upload_to='watch_images/'),
        ),
    ]
