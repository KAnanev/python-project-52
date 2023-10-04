import os

HOST = os.environ.get('HOST') or '*'

ALLOWED_HOSTS = [
    HOST,
]

CSRF_TRUSTED_ORIGINS = [
    HOST,
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
