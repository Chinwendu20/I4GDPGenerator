# Generated by Django 4.0.3 on 2022-03-24 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Height',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='Position_x',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='Position_y',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='Width',
            field=models.CharField(max_length=200),
        ),
    ]