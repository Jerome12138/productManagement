# Generated by Django 3.2.10 on 2022-01-13 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0016_fmfunctiontype'),
    ]

    operations = [
        migrations.CreateModel(
            name='FmDevelopTaskPruduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developTaskId', models.IntegerField(blank=True, db_column='develop_task_id', null=True)),
                ('productType', models.CharField(db_column='product_type', max_length=255, null=True)),
                ('productCode', models.CharField(blank=True, db_column='product_code', max_length=255, null=True)),
                ('productSn8', models.CharField(blank=True, db_column='product_sn8', max_length=255, null=True)),
                ('createDateTime', models.DateTimeField(auto_now_add=True, db_column='create_date_time', null=True)),
                ('updateDateTime', models.DateTimeField(auto_now=True, db_column='update_date_time', null=True)),
            ],
            options={
                'db_table': 'fm_develop_task_product',
            },
        ),
    ]
