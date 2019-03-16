from django.db import models

from questionnaires.models import Questionnaire


class QuestionnaireCategory(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=75, unique=True)


class QuestionnaireCategoryMember(models.Model):
    questionnaire = models.OneToOneField(Questionnaire, on_delete="CASCADE")
    category = models.ForeignKey(QuestionnaireCategory, on_delete="CASCADE")

