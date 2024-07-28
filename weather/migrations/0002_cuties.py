# Generated by Django 3.2 on 2024-07-23 11:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cuties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(max_length=255)),
                ('city', models.CharField(default='', max_length=6)),
                ('is_active', models.BooleanField(default=False)),
                ('token', models.UUIDField(default=uuid.UUID('dc33e10b-ac02-4f7f-ad51-49bad528650c'))),
            ],
        ),
    ]
