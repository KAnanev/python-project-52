ALLOWED_HOSTS = [
    'https://python-project-52-production-b33a.up.railway.app/',
]

CSRF_TRUSTED_ORIGINS = [
    'https://python-project-52-production-b33a.up.railway.app/'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
