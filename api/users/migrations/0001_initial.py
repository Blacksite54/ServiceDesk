# Generated by Django 5.1.3 on 2024-11-29 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, null=True, unique=True)),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('patronymic', models.CharField(max_length=200, null=True)),
                ('type_user', models.CharField(choices=[('1', 'User'), ('2', 'Manager')], default='1', max_length=2)),
                ('password', models.CharField(max_length=200, null=True)),
                ('login', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
