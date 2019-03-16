from django.contrib.auth.models import User
from django.db import models

from questionnaires.models import QuestionnaireScoringRule

from collections import defaultdict


class MeasurementSession(models.Model):
    def score_session(self):
        """Scores a session."""

        assert self.finished
        assert not self.active

        score_dict = defaultdict(int)
        # Reverse scoring
        if self.questionnaire._reverse_score_exists():
            response_value_set = set()
            for item in self.questionnaire.questionnaireitem_set.all():
                response_value_set |= set(
                    r.value for r in item.itemresponseoptions_set.all()
                )

            response_value_list = list(response_value_set)
            response_value_list.sort()

            reversed_response_value_list = response_value_list.copy()
            reversed_response_value_list.sort(key=lambda x: -x)

        scoring_rules = QuestionnaireScoringRule.objects.filter(
            questionnaire=self.questionnaire
        )

        for rule in scoring_rules:
            responses = MeasurementResponse.objects.filter(
                session=self, item__in=rule.items.all()
            )

            for response in responses:
                # Todo: Can raw_value be zero?
                raw_value = response.response.value

                if not response.item.score_reversed:
                    score_dict[rule.name] += raw_value
                else:
                    rev_value = reversed_response_value_list[
                        response_value_list.index(raw_value)
                    ]
                    score_dict[rule.name] += rev_value

        return score_dict

    datetime = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    questionnaire = models.ForeignKey(
        "questionnaires.Questionnaire", on_delete="CASCADE"
    )
    user = models.ForeignKey(User, on_delete="CASCADE")


class MeasurementResponse(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey("questionnaires.QuestionnaireItem", on_delete="CASCADE")
    session = models.ForeignKey(MeasurementSession, on_delete="CASCADE")
    response = models.ForeignKey(
        "questionnaires.ItemResponseOptions", on_delete="CASCADE"
    )
