import os

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SECRET_KEY = "mysecrekey"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
#SQLALCHEMY_DATABASE_URI = "postgresql://marioharoun:@localhost/marioharoun"
MAIL_SERVER='smtp.gmail.com'
MAIL_USERNAME='attendance.usj@gmail.com'
MAIL_PASSWORD='groupe17FYP2020'
MAIL_PORT= 587
MAIL_USE_SSL=False
MAIL_USE_TLS=True
LDAP_PROVIDER_URL = 'ldap://ldap.forumsys.com:389/'
LDAP_PROTOCOL_VERSION = 3
