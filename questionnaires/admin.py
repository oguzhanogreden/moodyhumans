from django.contrib import admin

from .models import (
    Questionnaire,
    QuestionnaireItem,
    ItemResponseOptions,
    QuestionnaireScoringRule,
)

# Register your models here.

admin.site.register(Questionnaire)
admin.site.register(QuestionnaireItem)
admin.site.register(ItemResponseOptions)
admin.site.register(QuestionnaireScoringRule)
