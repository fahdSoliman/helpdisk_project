# Generated by Django 3.1.5 on 2021-04-02 12:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0004_remove_product_month_fees'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='type_file',
            new_name='des_file',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='name',
            new_name='type_name',
        ),
        migrations.CreateModel(
            name='SharedHosting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_name', models.CharField(max_length=255)),
                ('operation', models.IntegerField(choices=[(0, 'windows'), (1, 'linux')], null=True)),
                ('transfer_website', models.BooleanField()),
                ('backup_website', models.BooleanField()),
                ('is_valid', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('start_date', models.DateField(default=datetime.datetime(2021, 4, 2, 12, 4, 11, 987929, tzinfo=utc))),
                ('expire_date', models.DateField(default=datetime.datetime(2022, 4, 2, 12, 4, 11, 987929, tzinfo=utc))),
                ('my_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.URLField()),
                ('activate', models.BooleanField()),
                ('primary_name_server', models.CharField(max_length=255)),
                ('secondary_name_server', models.CharField(max_length=255)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('start_date', models.DateField(default=datetime.datetime(2021, 4, 2, 12, 4, 11, 987929, tzinfo=utc))),
                ('expire_date', models.DateField(default=datetime.datetime(2022, 4, 2, 12, 4, 11, 987929, tzinfo=utc))),
                ('my_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HostDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.URLField()),
                ('ip_address', models.GenericIPAddressField()),
                ('is_valid', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('start_date', models.DateField(default=datetime.datetime(2021, 4, 2, 12, 4, 11, 987929, tzinfo=utc))),
                ('expire_date', models.DateField(default=datetime.datetime(2022, 4, 2, 12, 4, 11, 987929, tzinfo=utc))),
                ('my_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
