# Generated by Django 4.2.5 on 2023-09-26 06:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(default=uuid.UUID('816ec6cf-71d6-48ee-b374-4afa6d40d77c'), editable=False, primary_key=True, serialize=False),
        ),
    ]