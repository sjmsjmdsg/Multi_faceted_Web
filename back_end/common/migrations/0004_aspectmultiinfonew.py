# Generated by Django 3.2.13 on 2022-06-08 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_cveinfoplus'),
    ]

    operations = [
        migrations.CreateModel(
            name='AspectMultiInfoNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aspect_1', models.CharField(max_length=60)),
                ('aspect_2_ori', models.CharField(max_length=60)),
                ('aspect_2', models.CharField(max_length=1000)),
                ('co_appear_time', models.IntegerField()),
            ],
        ),
    ]
