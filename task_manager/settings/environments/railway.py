import os

HOST = os.environ.get('HOST') or '*'
CSRF_HOST = os.environ.get('CSRF_HOST') or '*'

ALLOWED_HOSTS = [
    HOST,
]

CSRF_TRUSTED_ORIGINS = [
    CSRF_HOST,
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
