# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 10:49
from __future__ import unicode_literals

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(max_length=1024)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('description', models.TextField(max_length=1024)),
                ('script', models.TextField(max_length=10240)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('characters', models.ManyToManyField(blank=True, to='core.Character')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Game')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Mechanic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Game')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(blank=True)),
                ('file', models.FileField(blank=True, upload_to=core.models.user_directory_path)),
                ('type', models.CharField(choices=[('AUDIO', 'Audio'), ('VIDEO', 'Video'), ('PICTURE', 'Picture')], max_length=30)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Game')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='mechanic',
            name='medias',
            field=models.ManyToManyField(blank=True, to='core.Media'),
        ),
        migrations.AddField(
            model_name='level',
            name='mechanics',
            field=models.ManyToManyField(blank=True, to='core.Mechanic'),
        ),
        migrations.AddField(
            model_name='level',
            name='medias',
            field=models.ManyToManyField(blank=True, to='core.Media'),
        ),
        migrations.AddField(
            model_name='character',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Game'),
        ),
        migrations.AddField(
            model_name='character',
            name='mechanics',
            field=models.ManyToManyField(blank=True, to='core.Mechanic'),
        ),
        migrations.AddField(
            model_name='character',
            name='medias',
            field=models.ManyToManyField(blank=True, to='core.Media'),
        ),
    ]
