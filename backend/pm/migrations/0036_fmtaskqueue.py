# Generated by Django 3.2.4 on 2022-02-19 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0035_fmuser_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='FmTaskQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskType', models.CharField(blank=True, db_column='task_type', max_length=255, null=True)),
                ('developTaskId', models.IntegerField(blank=True, db_column='develop_task_id', null=True)),
                ('userId', models.IntegerField(blank=True, db_column='user_id', null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
                ('createDateTime', models.DateTimeField(auto_now_add=True, db_column='create_date_time', null=True)),
                ('updateDateTime', models.DateTimeField(auto_now=True, db_column='update_date_time', null=True)),
            ],
            options={
                'db_table': 'fm_task_queue',
            },
        ),
    ]