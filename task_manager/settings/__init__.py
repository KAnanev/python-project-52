import os

from split_settings.tools import optional, include

ENV = os.environ.get('DJANGO_ENV') or 'development'

base_settings = [
    'components/base.py',
    'components/database.py',
    'environments/{0}.py'.format(ENV),
    optional('environments/local.py'),
]

include(*base_settings)
