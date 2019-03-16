from django.shortcuts import render

# Create your views here.
from .models import Questionnaire


def list(request):
    questionnaire_list = Questionnaire.objects.all()

    context = {"questionnaire_list": questionnaire_list}
    return render(request, "questionnaires/list.html", context)

