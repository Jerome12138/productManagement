# Generated by Django 3.2.10 on 2022-01-17 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0032_rename_voicefunction_id_fmproductvoicefunction_voicefunctionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='fmproductinfo',
            name='appStatus',
            field=models.CharField(blank=True, db_column='app_status', max_length=255, null=True),
        ),
    ]