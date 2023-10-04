ALLOWED_HOSTS = [
    '*',
]

CSRF_TRUSTED_ORIGINS = [
    '*',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
