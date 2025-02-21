# Generated by Django 5.1.4 on 2024-12-27 20:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity_name', models.CharField(max_length=50)),
                ('amenity_category', models.CharField(choices=[('Room Amenities', 'Room Amenities'), ('Bathroom Amenities', 'Bathroom Amenities'), ('Dining Amenities', 'Dining Amenities'), ('Leisure and Entertainment Amenities', 'Leisure and Entertainment Amenities'), ('Business Amenities', 'Business Amenities'), ('General Hotel Amenities', 'General Hotel Amenities'), ('Outdoor and Recreational Amenities', 'Outdoor and Recreational Amenities')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=50)),
                ('feature_category', models.CharField(choices=[('Safety and Security', 'Safety and Security'), ('Accessibility Features', 'Accessibility Features'), ('Technology Features', 'Technology Features'), ('Sustainability Features', 'Sustainability Features'), ('Design and Aesthetic Features', 'Design and Aesthetic Features')], max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('room_type', models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite')], max_length=40)),
                ('room_status', models.CharField(choices=[('Available', 'Available'), ('Booked', 'Booked')], max_length=40)),
                ('room_price', models.FloatField(default=0)),
                ('room_amenities', models.ManyToManyField(related_name='amenities', to='api.amenity')),
                ('room_features', models.ManyToManyField(related_name='features', to='api.feature')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_date', models.DateField()),
                ('checkout_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='api.room')),
            ],
        ),
    ]
