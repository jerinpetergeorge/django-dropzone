# Generated by Django 4.1.1 on 2022-12-27 07:29

from django.db import migrations, models
import dropzone.models


class Migration(migrations.Migration):

    dependencies = [
        ('dropzone', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=dropzone.models.Session.session_upload_path),
        ),
    ]
