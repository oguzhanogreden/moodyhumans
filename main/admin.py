from django.contrib import admin

from .models import QuestionnaireCategory, QuestionnaireCategoryMember

# Register your models here.

admin.site.register(QuestionnaireCategory)
admin.site.register(QuestionnaireCategoryMember)