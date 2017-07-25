from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    API_VERSION = 'v1'
    SECRET_KEY = 'secret key'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True

    CACHE_TYPE = 'null'
    CACHE_NO_NULL_WARNING = True

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False
