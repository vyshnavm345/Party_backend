import os

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
SECRET_KEY = "django-insecure-h$@e96=hy*fn*k#pu=738t6&z#oer4s_q@nkiqtk0v!+l-_km2"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *  # noqa: F403
except ImportError:
    pass
