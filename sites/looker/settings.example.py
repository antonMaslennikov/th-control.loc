import os
from pathlib import Path

from django.db import connections
BASE_DIR = Path(__file__).resolve().parent.parent
DB = 'looker_db'
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
ROOT_URL = '/site/looker'
INSTALLED_APPS = [
    'looker',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
