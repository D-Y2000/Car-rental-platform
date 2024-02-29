import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Energy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Engine name', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Transmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Transmission name', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Type of vehicle', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('agency_admin', 'Agency Admin'), ('agency_employer', 'Agency Employer'), ('default', 'Default')], default='default', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_validated', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=150)),
                ('bio', models.TextField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=14)),
                ('website', models.URLField(blank=True)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('license_doc', models.ImageField(blank=True, null=True, upload_to='')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_agency', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=14)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_branches', to='api_agency.agency')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Model', max_length=100)),
                ('series', models.CharField(blank=True, help_text='Model', max_length=100, null=True)),
                ('make_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_agency.make')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('mileage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('current_location', models.CharField(blank=True, max_length=30, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('seats', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('doors', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, help_text='Small description (1000)', max_length=1000, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('engine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.energy')),
                ('make', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.make')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.model')),
                ('options', models.ManyToManyField(blank=True, to='api_agency.option')),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_cars', to='api_agency.branch')),
                ('transmission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.transmission')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_agency.type')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
