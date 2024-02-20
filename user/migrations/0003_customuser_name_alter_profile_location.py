# Generated by Django 5.0.2 on 2024-02-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_customuser_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
