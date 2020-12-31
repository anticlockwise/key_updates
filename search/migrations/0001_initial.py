# Generated by Django 3.1.4 on 2020-12-31 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupBuyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('store_name', models.CharField(max_length=200)),
                ('expected_ship_date', models.CharField(max_length=200)),
                ('status', models.TextField()),
                ('update_time', models.DateTimeField()),
            ],
        ),
    ]
