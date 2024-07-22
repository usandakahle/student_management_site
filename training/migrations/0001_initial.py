# Generated by Django 5.0.6 on 2024-07-15 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('files', models.FileField(upload_to='files/task_files')),
                ('status', models.CharField(default='Assigned', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('unit_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=50)),
                ('unit_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User_record',
            fields=[
                ('user_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('reg_date', models.DateField(auto_now_add=True)),
                ('user_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_file', models.FileField(upload_to='files/submission_files')),
                ('comments', models.TextField(max_length=1000)),
                ('sub_date', models.DateField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='training.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='unit',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='training.unit'),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='training.user_record'),
        ),
        migrations.CreateModel(
            name='User_unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='training.unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='training.user_record')),
            ],
        ),
    ]
