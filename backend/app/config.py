

SECRET_KEY = 'SECRET_KEY'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
SECURITY_PASSWORD_SALT = 'SALT'
SECURITY_PASSWORD_HASH = 'bcrypt'
WTF_CSRF_ENABLED = False
JWT_SECRET_KEY = 'BOOKSHOW_KEY'
DEBUG = False
REDIS_URL = "redis://localhost:6379"
CACHE_TYPE = "RedisCache"
CACHE_REDIS_HOST = "localhost"
CACHE_REDIS_PORT = 6379
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"