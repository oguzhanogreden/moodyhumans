# Generated by Django 2.1.4 on 2019-03-16 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('measurements', '0001_initial'), ('measurements', '0002_auto_20190112_1858'), ('measurements', '0003_auto_20190112_2222'), ('measurements', '0004_measurementsession_active')]

    initial = True

    dependencies = [
        ('questionnaires', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questionnaires', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete='CASCADE', to='questionnaires.QuestionnaireItem')),
                ('response', models.ManyToManyField(to='questionnaires.ItemResponseOptions')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('finished', models.BooleanField(default=False)),
                ('questionnaire', models.ForeignKey(default=None, on_delete='CASCADE', to='questionnaires.Questionnaire')),
                ('user', models.ForeignKey(default=1, on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='measurementresponse',
            name='session',
            field=models.ForeignKey(on_delete='CASCADE', to='measurements.MeasurementSession'),
        ),
        migrations.RemoveField(
            model_name='measurementresponse',
            name='response',
        ),
        migrations.AddField(
            model_name='measurementresponse',
            name='response',
            field=models.ForeignKey(default=None, on_delete='CASCADE', to='questionnaires.ItemResponseOptions'),
            preserve_default=False,
        ),
    ]
