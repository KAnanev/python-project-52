ALLOWED_HOSTS = [
    'python-project-52-production-09bf.up.railway.app',
]

CSRF_TRUSTED_ORIGINS = [
    'https://python-project-52-production-09bf.up.railway.app'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
