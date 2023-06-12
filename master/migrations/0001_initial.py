# Generated by Django 4.2 on 2023-06-12 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MasterCategory',
            fields=[
                ('CategoryId', models.AutoField(primary_key=True, serialize=False)),
                ('ItemCategory', models.CharField(max_length=100, unique=True)),
                ('BoolInUse', models.BooleanField(blank=True, default=True, null=True)),
                ('IsActive', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'MasterCategory',
                'db_table': 'MasterCategory',
            },
        ),
        migrations.CreateModel(
            name='MasterCostCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CostCenter', models.CharField(max_length=100, unique=True)),
                ('BUSA', models.CharField(blank=True, max_length=100, null=True)),
                ('IsExisting', models.BooleanField(blank=True, default=0, null=True)),
                ('IsActive', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'MasterCostCenter',
                'db_table': 'MasterCostCenter',
            },
        ),
        migrations.CreateModel(
            name='MasterDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DepartmentName', models.CharField(max_length=100, unique=True)),
                ('DepartmentHead', models.CharField(blank=True, max_length=100, null=True)),
                ('DepartmentAdministrator', models.CharField(blank=True, max_length=100, null=True)),
                ('DepartmentSubAdministrator', models.CharField(blank=True, max_length=100, null=True)),
                ('BUCode', models.CharField(blank=True, max_length=100, null=True)),
                ('BoolInUse', models.BooleanField(blank=True, default=True, null=True)),
                ('IsActive', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'MasterDepartment',
                'db_table': 'MasterDepartment',
            },
        ),
        migrations.CreateModel(
            name='OrgDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, unique=True)),
                ('Head', models.CharField(blank=True, max_length=100, null=True)),
                ('BUWallet', models.CharField(blank=True, max_length=100, null=True)),
                ('RRProcessName', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'OrgDepartment',
                'db_table': 'OrgDepartment',
            },
        ),
        migrations.CreateModel(
            name='OrgDepartmentHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Head', models.CharField(blank=True, max_length=100, null=True)),
                ('Designation', models.CharField(blank=True, max_length=100, null=True)),
                ('OrgOffice', models.IntegerField(blank=True, null=True)),
                ('OrgDepartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrgDepartmentHead', to='master.orgdepartment')),
            ],
            options={
                'verbose_name_plural': 'OrgDepartmentHead',
                'db_table': 'OrgDepartmentHead',
            },
        ),
        migrations.CreateModel(
            name='MasterItem',
            fields=[
                ('ItemId', models.AutoField(primary_key=True, serialize=False)),
                ('ItemName', models.CharField(blank=True, max_length=100, null=True)),
                ('UnitPrice', models.FloatField(blank=True, null=True)),
                ('BoolInUse', models.BooleanField(blank=True, default=True, null=True)),
                ('IsActive', models.BooleanField(blank=True, default=True, null=True)),
                ('ItemCategoryId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.mastercategory')),
            ],
            options={
                'verbose_name_plural': 'MasterItem',
                'db_table': 'MasterItem',
            },
        ),
    ]
