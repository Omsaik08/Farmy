# Generated by Django 2.2.7 on 2021-03-31 10:41

import authorityApp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farmerApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='officer_registration_tbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to=authorityApp.models.path_and_rename)),
                ('full_name', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('mobile_no', models.CharField(max_length=10, unique=True)),
                ('address', models.CharField(max_length=100)),
                ('dob', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=10)),
                ('timestamp', models.CharField(max_length=20)),
                ('account_status', models.CharField(default='active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='send_email_with_image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to=authorityApp.models.temporary_image)),
            ],
        ),
        migrations.CreateModel(
            name='answer_tbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=400)),
                ('timestamp', models.CharField(max_length=20)),
                ('likes', models.PositiveSmallIntegerField(default=0)),
                ('dislikes', models.PositiveSmallIntegerField(default=0)),
                ('authority_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorityApp.officer_registration_tbl')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmerApp.questions_tbl')),
            ],
        ),
        migrations.CreateModel(
            name='amendment_bill_tbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_issued_date', models.CharField(max_length=15)),
                ('bill_uploading_date', models.CharField(max_length=20)),
                ('issued_by', models.CharField(max_length=50)),
                ('bill', models.FileField(upload_to=authorityApp.models.bill_rename)),
                ('subject', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('authority_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorityApp.officer_registration_tbl')),
            ],
        ),
    ]