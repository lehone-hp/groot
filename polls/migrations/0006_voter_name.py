# Generated by Django 2.2 on 2019-05-01 09:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20190501_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]