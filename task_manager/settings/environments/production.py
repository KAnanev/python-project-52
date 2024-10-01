import os

HOST = os.environ.get('HOST')
#   CSRF_HOST = os.environ.get('CSRF_HOST')

ALLOWED_HOSTS = [
    HOST,
]

# CSRF_TRUSTED_ORIGINS = [
#     CSRF_HOST,
# ]