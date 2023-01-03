import os

class Configuration(object):

    # === Main Settings === #

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://[database_owner_name]:[password]@127.0.0.1:5432/[database_name]"  
    SECRET_KEY = "jn232hjwe^EFWe2323f09F7wf9e8EH1FWf=mjtyyj="
    SECURITY_PASSWORD_SALT = 'salt'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
