import os

from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('MH_TESTDBNAME'),
        'USER': os.getenv('MH_TESTDBUSER'),
        'PASSWORD': os.getenv('MH_TESTDBPASS'),
        'HOST': os.getenv('MH_TESTDBHOST'),
        'PORT': os.getenv('MH_TESTDBPORT')
    }
}
