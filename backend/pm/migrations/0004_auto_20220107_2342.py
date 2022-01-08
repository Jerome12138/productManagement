# Generated by Django 3.2.10 on 2022-01-07 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0003_auto_20220107_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricboardfunctiondata',
            name='productType',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='electricboardfunctiontypedata',
            name='productType',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='functiondata',
            name='functionKey',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='functiondata',
            name='productType',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='functiondata',
            name='typeKey',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='functiontypedata',
            name='productType',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='functiontypedata',
            name='typeKey',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='taskdata',
            name='productType',
            field=models.CharField(max_length=32),
        ),
    ]