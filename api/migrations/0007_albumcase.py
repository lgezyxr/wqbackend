# Generated by Django 3.0.10 on 2021-05-31 14:16

import api.models.user
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_delete_albumcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, db_index=True, max_length=512, null=True)),
                ('date', models.DateField(db_index=True, null=True)),
                ('favorited', models.BooleanField(db_index=True, default=False)),
                ('location', django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_index=True, null=True)),
                ('owner', models.ForeignKey(default=None, on_delete=models.SET(api.models.user.get_deleted_user), to=settings.AUTH_USER_MODEL)),
                ('photos', models.ManyToManyField(to='api.Photo')),
                ('shared_to', models.ManyToManyField(related_name='album_case_shared_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('title', 'owner')},
            },
        ),
    ]
