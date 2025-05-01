import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
AUTH_FILE = os.path.join(DATA_DIR, "authorizations.xml")


class Config:
    DEBUG = True
    DATA_DIR = DATA_DIR
    AUTHORIZATIONS_FILE = AUTH_FILE
