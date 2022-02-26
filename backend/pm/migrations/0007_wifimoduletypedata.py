# Generated by Django 3.2.10 on 2022-01-09 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0006_heatingtubetypedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='WifiModuleTypeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(max_length=32)),
                ('networkingMode', models.CharField(max_length=32)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('create_user_id', models.CharField(max_length=16, null=True)),
                ('update_user_id', models.CharField(max_length=16, null=True)),
            ],
        ),
    ]