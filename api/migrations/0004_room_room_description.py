# Generated by Django 5.1.4 on 2025-01-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_roomimage_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
