# Generated by Django 5.1.3 on 2024-11-30 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_managers_remove_user_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
