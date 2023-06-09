# Generated by Django 4.2 on 2023-06-09 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('GlobalEmpNo', models.CharField(blank=True, max_length=100, null=True)),
                ('YGSAccountCode', models.CharField(blank=True, max_length=100, null=True)),
                ('DomainId', models.CharField(blank=True, max_length=100, null=True)),
                ('YGSCostCenter', models.CharField(blank=True, max_length=100, null=True)),
                ('CostCenter', models.CharField(blank=True, max_length=100, null=True)),
                ('Sex', models.CharField(blank=True, max_length=100, null=True)),
                ('DOB', models.DateTimeField(blank=True, null=True)),
                ('BoolContract', models.BooleanField(default=False)),
                ('DOJ', models.DateField(blank=True, null=True)),
                ('DepartmentId', models.IntegerField(blank=True, null=True)),
                ('GroupId', models.IntegerField(blank=True, null=True)),
                ('DeptCode', models.CharField(blank=True, max_length=100, null=True)),
                ('Grade', models.CharField(blank=True, max_length=100, null=True)),
                ('Designation', models.CharField(blank=True, max_length=100, null=True)),
                ('FunctionalRoleId', models.IntegerField(blank=True, default=0, null=True)),
                ('OldEmail', models.EmailField(blank=True, max_length=100, null=True)),
                ('HODEmpNo', models.CharField(blank=True, max_length=100, null=True)),
                ('BoolHOD', models.BooleanField(blank=True, default=False, null=True)),
                ('MobileNo', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('OrgDepartmentId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.orgdepartment')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'EmployeeUser',
                'db_table': 'EmployeeUser',
                'ordering': ['id'],
                'managed': True,
            },
        ),
    ]
