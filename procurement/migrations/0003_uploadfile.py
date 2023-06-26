# Generated by Django 4.2 on 2023-06-26 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0002_masterprocurement_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploads', models.ImageField(blank=True, null=True, upload_to='procurement/')),
                ('filetype', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'UploadFile',
                'db_table': 'UploadFile',
            },
        ),
    ]
