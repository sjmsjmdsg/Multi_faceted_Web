# Generated by Django 4.0.1 on 2022-02-28 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_wordthesaurus_wordtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordType2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50, null=True)),
                ('type', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
