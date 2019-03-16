from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.base import TemplateView

from .forms import SignupForm
from measurements.models import MeasurementSession
from questionnaires.models import Questionnaire
from main.models import QuestionnaireCategory

import json
import ohapi
import requests
import tempfile
import urllib.parse

from collections import defaultdict
from datetime import date, datetime
from openhumans.models import OpenHumansMember


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user measurement history:
        user_sessions = defaultdict(int)

        for s in MeasurementSession.objects.filter(user=user):
            if s.finished:
                user_sessions[s.questionnaire] += 1

        # Get active questionnaires to list them:
        questionnaires = Questionnaire.objects.all()

        # Get categories:
        q_categories = QuestionnaireCategory.objects.all()

        context["q_categories"] = q_categories
        context["questionnaires"] = questionnaires
        context["user_sessions"] = dict(user_sessions)

        return context

    # def post(self, request, *args, **kwargs):
    #     pass


class OpenHumansAuthStartView(View):
    def get(self, request, *args, **kwargs):
        oh_url_base = (
            "https://www.openhumans.org/direct-sharing/projects/oauth2/authorize?"
        )
        oh_url_vars = {
            "client_id": settings.OPENHUMANS_CLIENT_ID,
            "response_type": "code",
        }
        oh_url = oh_url_base + urllib.parse.urlencode(oh_url_vars)
        return redirect(oh_url)


class OpenHumansAuthCompleteView(View):
    def get(self, request, *args, **kwargs):

        user = self.request.user
        auth_code = request.GET["code"]

        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": settings.OPENHUMANS_APP_BASE_URL
            + "/accounts/openhumans/complete",
        }
        token_response = requests.post(
            "https://www.openhumans.org/oauth2/token/",
            data=data,
            auth=requests.auth.HTTPBasicAuth(
                settings.OPENHUMANS_CLIENT_ID, settings.OPENHUMANS_CLIENT_SECRET
            ),
        )

        token_data = token_response.json()

        # OpenHumansMember.get_create_member() does not work...
        oh_id = ohapi.api.exchange_oauth2_member(
            access_token=token_data["access_token"],
            base_url=settings.OPENHUMANS_OH_BASE_URL,
        )["project_member_id"]

        user_model = get_user_model()

        if user.is_authenticated:
            # User is trying to link link OH account to MH.
            try:
                user = user_model.objects.get(openhumansmember__oh_id=oh_id)

                # TODO: Link accounts to each other?
                self.request.session["OHMemberInUse"] = True

                return redirect("main:profile")
            except user_model.DoesNotExist:
                openhumansmember = OpenHumansMember.create(
                    oh_id=oh_id, data=token_data, user=user
                )
                openhumansmember.save()
        else:
            # User is trying to log in with an OH.
            try:
                user = user_model.objects.get(openhumansmember__oh_id=oh_id)
            except user_model.DoesNotExist:
                openhumansmember = OpenHumansMember.create(oh_id=oh_id, data=token_data)
                openhumansmember.save()
                user = openhumansmember.user

            login(self.request, user)

        return redirect("main:index")


class OpenHumansUploadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        user = self.request.user

        # Check if the user has openhumans authentication, otherwise redirect:
        try:
            oh_member = user.openhumansmember
        except django.contrib.auth.models.User.openhumansmember.RelatedObjectDoesNotExist:
            return redirect("main:oh_auth")

        temporary_file = tempfile.TemporaryFile(mode="w+")
        user_data = {}

        # Get data
        sessions = MeasurementSession.objects.filter(
            active=False, finished=True, user=user
        )

        for session in sessions:
            session_dict = {
                "date": session.datetime.strftime("%Y-%m-%d-%H-%M-%S"),
                "questionnaire": session.questionnaire.name,
                "scores": session.score_session(),
            }

            user_data[session.id] = session_dict

        json.dump(user_data, temporary_file)

        # Remove data
        user.openhumansmember.delete_all_files()

        # Push the file
        temporary_file.seek(0)
        user.openhumansmember.upload(
            temporary_file,
            f'moodyhumans_{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}.json',
            metadata={"description": "MoodyHumans data", "tags": ["mood tracking"]},
        )

        return redirect("main:oh_upload_complete")


class OpenHumansUploadCompleteView(TemplateView):
    template_name = "main/oh_upload_complete.html"
    pass


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "main/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # User tried to log in with an OH account linked to another MH account
            if self.request.session["OHMemberInUse"]:
                context["OHMemberInUse"] = True
                del self.request.session["OHMemberInUse"]
                return context
        except KeyError:
            pass

        user = self.request.user

        # Check if user is authenticated in OpenHumans:
        oh_authenticated = False
        if getattr(user, "openhumansmember", None):
            oh_authenticated = True

        context["oh_authenticated"] = oh_authenticated

        return context


class SignupFormView(View):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def _registration_abused(self):
        """Check if there's a registration abuse going on."""

        users_in_last_day = get_user_model().objects.filter(
            date_joined__gte=date.today()
        )

        if len(users_in_last_day) >= 50:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        if self._registration_abused():
            return redirect("main:index")

        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("main:index")
        else:
            return redirect("main:signup")
