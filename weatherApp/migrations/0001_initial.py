# Generated by Django 2.2.7 on 2021-03-31 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farmerApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='my_cities_tbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cities', models.CharField(max_length=40)),
                ('timestamp', models.CharField(max_length=20)),
                ('farmer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmerApp.farmer_registration_tbl')),
            ],
        ),
    ]
