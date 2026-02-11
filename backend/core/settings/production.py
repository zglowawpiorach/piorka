from .base import *

DEBUG = False

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"][
    "BACKEND"
] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Logging overrides for production - reduce verbosity
LOGGING = {
    'handlers': {
        'console': {
            'level': 'INFO',
        },
        'file': {
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'level': 'WARNING',
        },
        'api': {
            'level': 'INFO',
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
