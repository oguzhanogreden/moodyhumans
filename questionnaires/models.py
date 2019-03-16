from django.db import models

# Create your models here.


class Questionnaire(models.Model):
    def __str__(self):
        return self.name

    def _calculate_length(self):
        """Function to calculate questionnaire length.

        This can be called once all items are added."""

        items = self.questionnaireitem_set.all()

        self.length = len(items)
        self.save()

    def _reverse_score_exists(self):
        items = self.questionnaireitem_set.all()
        return any(i.score_reversed for i in items)

    description = models.CharField(max_length=750)
    name = models.CharField(max_length=20, unique=True)
    length = models.IntegerField(null=True, blank=True)


class QuestionnaireItem(models.Model):
    def __str__(self):
        return self.name

    questionnaire = models.ForeignKey(Questionnaire, on_delete="CASCADE", default=1)
    name = models.CharField(max_length=20, unique=True)
    order = models.IntegerField()
    root = models.CharField(max_length=750)
    score_reversed = models.BooleanField()


class ItemResponseOptions(models.Model):
    def __str__(self):
        return self.name

    item = models.ManyToManyField(QuestionnaireItem)
    label = models.CharField(max_length=200)
    name = models.CharField(max_length=20, unique=True)
    value = models.IntegerField()


class QuestionnaireScoringRule(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete="CASCADE")
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=750)
    items = models.ManyToManyField("questionnaires.QuestionnaireItem")
