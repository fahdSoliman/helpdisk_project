# Generated by Django 3.1.5 on 2021-04-04 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0008_auto_20210402_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='phone',
            field=models.CharField(default='+963', max_length=255),
        ),
        migrations.AlterField(
            model_name='finanicalresponse',
            name='phone',
            field=models.CharField(default='+963', max_length=255),
        ),
        migrations.AlterField(
            model_name='technicalresponse',
            name='phone',
            field=models.CharField(default='+963', max_length=255),
        ),
    ]
