# Generated by Django 4.2 on 2023-06-15 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approvalUserName', models.CharField(blank=True, max_length=100, null=True)),
                ('approverEmail', models.EmailField(blank=True, max_length=100, null=True)),
                ('sequence', models.IntegerField(blank=True, default=0, null=True)),
                ('approverType', models.CharField(blank=True, choices=[('BuHead', 'BuHead'), ('DSINHead', 'DSINHead'), ('FinanceHead', 'FinanceHead'), ('MD', 'MD'), ('DSINMPR', 'DSINMPR')], max_length=100, null=True)),
                ('status', models.CharField(blank=True, default='Pending', max_length=100, null=True)),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('approvaldatetime', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'ApprovalTransaction',
                'db_table': 'ApprovalTransaction',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ApproverMatrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_approver', models.CharField(blank=True, max_length=100, null=True)),
                ('secondary_approver', models.CharField(blank=True, max_length=100, null=True)),
                ('sequence', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name_plural': 'ApproverMatrix',
                'db_table': 'ApproverMatrix',
            },
        ),
    ]
