# Generated by Django 2.1.4 on 2019-01-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaireitem',
            name='questionnaire',
        ),
        migrations.AddField(
            model_name='questionnaireitem',
            name='questionnaire',
            field=models.ForeignKey(default=1, on_delete='CASCADE', to='questionnaires.Questionnaire'),
        ),
    ]
