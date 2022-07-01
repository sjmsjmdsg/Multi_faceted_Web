# Generated by Django 4.0.1 on 2022-02-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AspectCompare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cveid', models.CharField(max_length=50)),
                ('nvd_product', models.CharField(max_length=120, null=True)),
                ('nvd_version', models.CharField(max_length=120, null=True)),
                ('nvd_vultype', models.CharField(max_length=120, null=True)),
                ('nvd_component', models.CharField(max_length=120, null=True)),
                ('nvd_root', models.CharField(max_length=120, null=True)),
                ('nvd_vector', models.CharField(max_length=120, null=True)),
                ('nvd_impact', models.CharField(max_length=120, null=True)),
                ('ibm_product', models.CharField(max_length=120, null=True)),
                ('ibm_version', models.CharField(max_length=120, null=True)),
                ('ibm_vultype', models.CharField(max_length=120, null=True)),
                ('ibm_component', models.CharField(max_length=120, null=True)),
                ('ibm_root', models.CharField(max_length=120, null=True)),
                ('ibm_vector', models.CharField(max_length=120, null=True)),
                ('ibm_impact', models.CharField(max_length=120, null=True)),
                ('openwall_product', models.CharField(max_length=120, null=True)),
                ('openwall_version', models.CharField(max_length=120, null=True)),
                ('openwall_vultype', models.CharField(max_length=120, null=True)),
                ('openwall_component', models.CharField(max_length=120, null=True)),
                ('openwall_root', models.CharField(max_length=120, null=True)),
                ('openwall_vector', models.CharField(max_length=120, null=True)),
                ('openwall_impact', models.CharField(max_length=120, null=True)),
                ('exploitdb_product', models.CharField(max_length=120, null=True)),
                ('exploitdb_version', models.CharField(max_length=120, null=True)),
                ('exploitdb_vultype', models.CharField(max_length=120, null=True)),
                ('exploitdb_component', models.CharField(max_length=120, null=True)),
                ('exploitdb_root', models.CharField(max_length=120, null=True)),
                ('exploitdb_vector', models.CharField(max_length=120, null=True)),
                ('exploitdb_impact', models.CharField(max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DatabaseIndicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cveid', models.CharField(max_length=50)),
                ('nvd_link', models.CharField(max_length=100)),
                ('ibm_link', models.CharField(max_length=100)),
                ('openwall_link', models.CharField(max_length=100)),
                ('exploitdb_link', models.CharField(max_length=100)),
            ],
        ),
    ]