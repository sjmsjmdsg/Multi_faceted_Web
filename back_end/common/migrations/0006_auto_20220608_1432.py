# Generated by Django 3.2.13 on 2022-06-08 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20220608_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cveinfoplus',
            name='id',
        ),
        migrations.AlterField(
            model_name='cveinfoplus',
            name='cveid',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
