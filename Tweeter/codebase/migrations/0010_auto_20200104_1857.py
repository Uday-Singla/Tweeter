# Generated by Django 3.0 on 2020-01-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codebase', '0009_auto_20200104_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='post_pics'),
        ),
    ]