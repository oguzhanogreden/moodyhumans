# Generated by Django 2.1.4 on 2019-01-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0004_auto_20190122_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaireitem',
            name='scoring_rules',
        ),
        migrations.AddField(
            model_name='questionnairescoringrule',
            name='items',
            field=models.ManyToManyField(to='questionnaires.QuestionnaireScoringRule'),
        ),
    ]
