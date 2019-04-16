import os
basedir = os.path.abspath(os.path.dirname(__file__))

"""Konfigurationen für die Applikation """
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TU-Dortmund-ITPL'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/postgres'
    #'postgresql://localhost/postgres'

        #'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False