# Generated by Django 2.1.4 on 2019-02-02 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnairecategorymember',
            name='questionnaire',
            field=models.OneToOneField(on_delete='CASCADE', to='questionnaires.Questionnaire'),
        ),
    ]
