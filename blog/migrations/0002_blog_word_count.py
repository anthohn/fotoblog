# Generated by Django 4.2.7 on 2023-11-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='word_count',
            field=models.IntegerField(null=True),
        ),
    ]