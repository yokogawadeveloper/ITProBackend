# Generated by Django 4.2 on 2023-06-20 11:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File', models.FileField(blank=True, null=True, upload_to='procurement/%Y/%m/%d/%H_%M_%S')),
                ('FileType', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'MasterUpload',
                'db_table': 'MasterUpload',
            },
        ),
        migrations.CreateModel(
            name='MasterProcurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RequestNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('RequestType', models.CharField(blank=True, max_length=100, null=True)),
                ('Name', models.CharField(blank=True, max_length=100, null=True)),
                ('Department', models.CharField(blank=True, max_length=100, null=True)),
                ('IsExpenditure', models.CharField(blank=True, default='No', max_length=100, null=True)),
                ('TotalBudget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('UtilizedBudget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Remarks', models.TextField(blank=True, null=True)),
                ('PurchaseDate', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('Age', models.IntegerField(blank=True, default=0, null=True)),
                ('Status', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('DeviceType', models.CharField(blank=True, choices=[('New', 'New'), ('Rental', 'Rental')], default='New', max_length=100, null=True)),
                ('Created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('Updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('Attachment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='procurement.masterupload')),
                ('Created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('Updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'MasterProcurement',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='InlineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('item', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('unitprice', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('totalprice', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('attachment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='procurement.masterupload')),
                ('costcenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.mastercostcenter')),
                ('procurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inlineitem', to='procurement.masterprocurement')),
            ],
            options={
                'db_table': 'InlineItem',
                'ordering': ['id'],
            },
        ),
    ]
