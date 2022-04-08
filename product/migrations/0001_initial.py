# Generated by Django 3.1.5 on 2021-02-19 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type_file', models.FileField(null=True, upload_to='type_files/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product_description', models.TextField()),
                ('product_file', models.FileField(null=True, upload_to='product_files/')),
                ('year_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.type')),
            ],
        ),
    ]
