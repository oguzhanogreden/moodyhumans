from django.core.management.base import BaseCommand, CommandError
from questionnaires.models import Questionnaire, QuestionnaireItem, ItemResponseOptions

from django.db.utils import IntegrityError

import pdb

class Command(BaseCommand):
    help = 'Initializes the database'

    cesdr = {
        'name': 'CESD-R',
        'description': 'Center for Epidemiologic Studies Depression Scale (CESD).',
        'items': [{
                'name': "cesdr1",
                'root': "My appetite was poor.",
                'score_reversed': False
                
            },
            {
                'name': "cesdr2",
                'root': "I could not shake off the blues.?",
                'score_reversed': False
            },
            {
                'name': "cesdr3",
                'root': "I had trouble keeping my mind on what I was doing.",
                'score_reversed': False
            },
            {
                'name': "cesdr4",
                'root': "I felt depressed.",
                'score_reversed': False
            },
            {
                'name': "cesdr5",
                'root': "My sleep was restless.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr6",
                'root': "I felt sad.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr7",
                'root': "I could not get going.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr8",
                'root': "Nothing made me happy.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr9",
                'root': "I felt like a bad person.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr10",
                'root': "I lost interest in my usual activities.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr11",
                'root': "I slept much more than usual.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr12",
                'root': "I felt like I was moving too slowly.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr13",
                'root': "I felt fidgety.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr14",
                'root': "I wished I were dead.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr15",
                'root': "I wanted to hurt myself.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr16",
                'root': "I was tired all the time.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr17",
                'root': "I did not like myself.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr18",
                'root': "I lost a lot of weight without trying to.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr19",
                'root': "I had a lot of trouble getting to sleep.",
                'score_reversed': False
            
            },
            {
                'name': "cesdr20",
                'root': "I could not focus on the important things.",
                'score_reversed': False
            
            }
        ],
        'response_options': [{
            'value': 0,
            'label': 'None/Less than 1 days'
        },
        {
            'value': 1,
            'label': '1-2 days'
        },
        {
            'value': 2,
            'label': '3-4 days'
        },
        {
            'value': 3,
            'label': '5-7 days'
        },
        {
            'value': 4,
            'label': 'Nearly everyday for 2 weeks'
        }]
    }

    panas = {
        'name': 'PANAS',
        'description': 'Positive and Negative Affect Scale',
        'items': [
            {
                'name': "panastimeframe",
                'root': "For which time frame do you want to measure?",
                'score_reversed': False
            },
            {
                'name': "panas1",
                'root': "interested",
                'score_reversed': False
            },
            {
                'name': "panas2",
                'root': "distressed",
                'score_reversed': False
            },
            {
                'name': "panas3",
                'root': "excited",
                'score_reversed': False
            },
            {
                'name': "panas4",
                'root': "upset",
                'score_reversed': False
            },
            {
                'name': "panas5",
                'root': "strong",
                'score_reversed': False
            },
            {
                'name': "panas6",
                'root': "guilty",
                'score_reversed': False
            },
            {
                'name': "panas7",
                'root': "scared",
                'score_reversed': False
            },
            {
                'name': "panas8",
                'root': "hostile",
                'score_reversed': False
            },
            {
                'name': "panas9",
                'root': "enthusiastic",
                'score_reversed': False
            },
            {
                'name': "panas10",
                'root': "proud",
                'score_reversed': False
            },
            {
                'name': "panas11",
                'root': "irritable",
                'score_reversed': False
            },
            {
                'name': "panas12",
                'root': "alert",
                'score_reversed': False
            },
            {
                'name': "panas13",
                'root': "ashamed",
                'score_reversed': False
            },
            {
                'name': "panas14",
                'root': "inspired",
                'score_reversed': False
            },
            {
                'name': "panas15",
                'root': "nervous",
                'score_reversed': False
            },
            {
                'name': "panas16",
                'root': "determined",
                'score_reversed': False
            },
            {
                'name': "panas17",
                'root': "attentive",
                'score_reversed': False
            },
            {
                'name': "panas18",
                'root': "jittery",
                'score_reversed': False
            },
            {
                'name': "panas19",
                'root': "active",
                'score_reversed': False
            },
            {
                'name': "panas20",
                'root': "afraid",
                'score_reversed': False
            }
        ],
        'response_options': [
            {
                'value': 1,
                'label': "very slightly or not at all"
            },
            {
                'value': 2,
                'label': "a little"
            },
            {
                'value': 3,
                'label': "moderately"
            },
            {
                'value': 4,
                'label': "quite a bit"
            },
            {
                'value': 5,
                'label': "extremely"
            },
            {
                'value': 90,
                'label': "moment"
            },
            {
                'value': 91,
                'label': "today"
            },
            {
                'value': 92,
                'label': "past few days"
            },
            {
                'value': 93,
                'label': "past week"
            },
            {
                'value': 94,
                'label': "past few weeks"
            },
            {
                'value': 95,
                'label': "past year"
            },
            {
                'value': 96,
                'label': "general"
            }
        ]
    }

    rosenberg = {
        'name': 'RSES',
        'description': 'Rosenberg Self-Esteem Scale',
        'items': [
            {
                'name': "rses1",
                'root': "On the whole, I am satisfied with myself.",
                'score_reversed': "False"
            },
            {
                'name': "rses2",
                'root': "At times I think I am no good at all.",
                'score_reversed': "True"
            },
            {
                'name': "rses3",
                'root': "I feel that I have a number of good qualities.",
                'score_reversed': "False"
            },
            {
                'name': "rses4",
                'root': "I am able to do things as well as most other people.",
                'score_reversed': "False"
            },
            {
                'name': "rses5",
                'root': "I feel I do not have much to be proud of.",
                'score_reversed': "True"
            },
            {
                'name': "rses6",
                'root': "I certainly feel useless at times.",
                'score_reversed': "True"
            },
            {
                'name': "rses7",
                'root': "I feel that I'm a person of worth, at least on an equal plane with others.",
                'score_reversed': "False"
            },
            {
                'name': "rses8",
                'root': "I wish I could have more respect for myself.",
                'score_reversed': "True"
            },
            {
                'name': "rses9",
                'root': "All in all, I am inclined to feel that I am a failure.",
                'score_reversed': "True"
            },
            {
                'name': "rses10",
                'root': "I take a positive attitude toward myself.",
                'score_reversed': "False"
            }
        ],
        'response_options': [
            {
                'value': 4,
                'label': "Strongly agree"
            },
            {
                'value': 3,
                'label': "Agree"
            },
            {
                'value': 2,
                'label': "Disagree"
            },
            {
                'value': 1,
                'label': "Strongly disagree"
            }
        ]
    }

    def create_questionnaire_obj(self, name, description):
        q = Questionnaire(
            name=name,
            description=description
        )

        q.save()

        return q

    def create_questionnaire_items(self, q_obj, items):
        # pdb.set_trace()
        i_objs = []
        for ind, item in enumerate(items):
            try:
                i = QuestionnaireItem(
                    name=item['name'],
                    order=ind,
                    questionnaire=q_obj,
                    root=item['root'],
                    score_reversed=item['score_reversed']
                )

                i.save()
            except IntegrityError as e:
                i = QuestionnaireItem.objects.get(name=item['name'])
                pass        
            
            i_objs.append(i)            
            
        return i_objs

    def create_questionnaire_response_opts(self, q_obj, item_objs, response_options):
        # Assumes uniform response_options:
        for ind, r in enumerate(response_options):
            ir = ItemResponseOptions(
                label = r['label'],
                name = '{}_{}'.format(q_obj.name, ind),
                value = r['value']
            )

            ir.save()

            for i_obj in item_objs:
                ir.item.add(i_obj)

    def handle(self, *args, **options):

        # # Create CESD-R
        try:
            try:
                q = self.create_questionnaire_obj(self.cesdr['name'], self.cesdr['description'])
                q._calculate_length()
            except IntegrityError:
                q = Questionnaire.objects.get(name=self.cesdr['name'])
                pass

            i_objs = self.create_questionnaire_items(q, self.cesdr['items'])      
            self.create_questionnaire_response_opts(q, i_objs, self.cesdr['response_options'])
        except Exception as e:
            self.stderr.write('Trouble while initializing CESD-R.')
            print(e)
        
        # Create PANAS
        try:
            try:
                q = self.create_questionnaire_obj(self.panas['name'], self.panas['description'])
                q._calculate_length()
            except IntegrityError:
                q = Questionnaire.objects.get(name=self.panas['name'])
                pass

            i_objs = self.create_questionnaire_items(q, self.panas['items'])      
            self.create_questionnaire_response_opts(q, i_objs, self.panas['response_options'])
        except Exception as e:
            self.stderr.write('Trouble while initializing PANAS.')
            # self.stderr.write(e)
            

        # Create RSES
        try:
            try:
                q = self.create_questionnaire_obj(self.rosenberg['name'], self.rosenberg['description'])
                q._calculate_length()
            except IntegrityError:
                q = Questionnaire.objects.get(name=self.rosenberg['name'])
                pass

            i_objs = self.create_questionnaire_items(q, self.rosenberg['items'])      
            self.create_questionnaire_response_opts(q, i_objs, self.rosenberg['response_options'])
        except Exception as e:
            self.stderr.write('Trouble while initializing RSES.')
            # self.stderr.write(e)
            
        