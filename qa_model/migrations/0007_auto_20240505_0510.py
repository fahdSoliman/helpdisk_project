# Generated by Django 3.2 on 2024-05-05 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa_model', '0006_alter_qa_passages'),
    ]

    operations = [
        migrations.AddField(
            model_name='qa',
            name='ar_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='qa',
            name='ar_question',
            field=models.TextField(blank=True, null=True),
        ),
    ]
