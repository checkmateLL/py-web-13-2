# Generated by Django 5.1.3 on 2024-11-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='mongo_id',
            field=models.CharField(default='unknown', max_length=24, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='author',
            name='born_date',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='author',
            name='born_location',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='author',
            name='fullname',
            field=models.CharField(max_length=200),
        ),
    ]
