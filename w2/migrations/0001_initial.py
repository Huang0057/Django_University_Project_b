# Generated by Django 4.2.5 on 2023-10-04 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Arm_UID', models.CharField(max_length=20, unique=True)),
                ('Foot_UID', models.CharField(max_length=20, unique=True)),
                ('Limb_UID', models.CharField(max_length=20, unique=True)),
                ('Hand_UID', models.CharField(max_length=20, unique=True)),
                ('TotalCoin', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LimbMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastStage', models.CharField(max_length=20)),
                ('TotalPlayTime', models.FloatField(default=0)),
                ('TotalPlayCount', models.IntegerField(default=0)),
                ('PassCount', models.IntegerField(default=0)),
                ('TotalGetCoin', models.IntegerField(default=0)),
                ('LastRecordId', models.CharField(max_length=20)),
                ('Limb_UID', models.CharField(max_length=20, unique=True)),
                ('USER_UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w2.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HandMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastStage', models.CharField(max_length=20)),
                ('TotalPlayTime', models.FloatField(default=0)),
                ('TotalPlayCount', models.IntegerField(default=0)),
                ('PassCount', models.IntegerField(default=0)),
                ('TotalGetCoin', models.IntegerField(default=0)),
                ('LastRecordId', models.CharField(max_length=20)),
                ('Hand_UID', models.CharField(max_length=20, unique=True)),
                ('USER_UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w2.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GameRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlayDate', models.DateField()),
                ('PlayPart', models.CharField(max_length=20)),
                ('UID', models.IntegerField()),
                ('PlayStage', models.CharField(max_length=20)),
                ('StartTime', models.TimeField()),
                ('EndTime', models.TimeField()),
                ('DurationTime', models.DurationField()),
                ('AddCoin', models.IntegerField(default=0)),
                ('ExerciseCount', models.IntegerField(default=0)),
                ('EstablishTime', models.DateTimeField(auto_now_add=True)),
                ('USER_UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w2.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='FootMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastStage', models.CharField(max_length=20)),
                ('TotalPlayTime', models.FloatField(default=0)),
                ('TotalPlayCount', models.IntegerField(default=0)),
                ('PassCount', models.IntegerField(default=0)),
                ('TotalGetCoin', models.IntegerField(default=0)),
                ('LastRecordId', models.CharField(max_length=20)),
                ('Foot_UID', models.CharField(max_length=20, unique=True)),
                ('USER_UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w2.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArmMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastStage', models.CharField(max_length=20)),
                ('TotalPlayTime', models.FloatField(default=0)),
                ('TotalPlayCount', models.IntegerField(default=0)),
                ('PassCount', models.IntegerField(default=0)),
                ('TotalGetCoin', models.IntegerField(default=0)),
                ('LastRecordId', models.CharField(max_length=20)),
                ('Arm_UID', models.CharField(max_length=20, unique=True)),
                ('USER_UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w2.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
