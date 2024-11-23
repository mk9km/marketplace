import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'marketplace.db')

SECRET_KEY = 'very-secret-key'
SESSION_TYPE = 'filesystem'
