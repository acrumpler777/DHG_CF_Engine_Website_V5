# Generated by Django 3.1.1 on 2020-09-12 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_flow_engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='calculated_file',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
