from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic.base import TemplateView

from questionnaires.models import Questionnaire, QuestionnaireItem, ItemResponseOptions

from .models import MeasurementSession, MeasurementResponse


class SessionFinished(Exception):
    pass


class MeasurementFinishedView(LoginRequiredMixin, TemplateView):
    template_name = "measurements/finished.html"


class MeasurementItemView(LoginRequiredMixin, TemplateView):
    template_name = "measurements/item.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        item = kwargs["item"]
        q_name = kwargs["name"]
        session_id = kwargs["session_id"]

        # Get the questionnaire
        q = Questionnaire.objects.get(name=q_name)
        # Get the item
        try:
            i = QuestionnaireItem.objects.get(questionnaire=q, order=item)
        except QuestionnaireItem.DoesNotExist:
            # This should happen only if a questionnaire is finished.
            # i.e. item == Questionnaire.length.
            assert item == q.length

            s = MeasurementSession.objects.get(id=session_id)
            s.finished = True
            s.active = False
            s.save()

            raise SessionFinished

        # Get the response options
        r = ItemResponseOptions.objects.filter(item=i).order_by("value")

        context["i"] = i
        context["response_options"] = r
        context["session_id"] = session_id
        context["q"] = q

        return context

    def get(self, request, *args, **kwargs):
        # Check if someone's requesting a finished questionnaire:
        try:
            MeasurementSession.objects.get(id=kwargs["session_id"], active=True)
        except MeasurementSession.DoesNotExist:
            Http404("Trying to reach inactive session.")

        try:
            context = self.get_context_data(**kwargs)
        except SessionFinished:
            return redirect("measurements:finished")

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        item_response = request.POST["item_response"]
        item = kwargs["item"]
        q_name = kwargs["name"]
        session_id = kwargs["session_id"]

        # Get the item
        s = MeasurementSession.objects.get(id=session_id)
        i = QuestionnaireItem.objects.get(questionnaire__name=q_name, order=item)
        r = ItemResponseOptions.objects.get(name=item_response)

        try:
            response_entry = MeasurementResponse.objects.get(item=i, session=s)
        except MeasurementResponse.DoesNotExist:
            response_entry = MeasurementResponse(item=i, session=s)

        response_entry.response = r
        response_entry.save()

        return redirect(
            "measurements:item", session_id=s.id, name=q_name, item=item + 1
        )


class StartMeasurementView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        q_name = kwargs["name"]

        q = Questionnaire.objects.get(name=q_name)

        m = MeasurementSession(questionnaire=q, user=request.user)

        try:
            m.save()
        except Exception as e:
            raise (e)

        return redirect("measurements:item", session_id=m.id, name=q.name, item=0)


class MeasurementHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "measurements/history.html"

    def get_context_data(self, *args, **kwargs):

        context = {}

        q_name = kwargs["name"]
        user = self.request.user

        # Get measurement sessions of user
        measurement_sessions = MeasurementSession.objects.filter(
            user=user, questionnaire__name=q_name, finished=True, active=False
        )

        context["history"] = map(
            lambda x: {"q_name": x.questionnaire.name, "scores": x.score_session()},
            measurement_sessions,
        )

        return context
