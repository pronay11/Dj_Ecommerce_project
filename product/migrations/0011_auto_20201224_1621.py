# Generated by Django 3.1.3 on 2020-12-24 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.EmailField(blank=True, max_length=270),
        ),
    ]
