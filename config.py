import os # os means operating system

basedir = os.path.abspath(os.path.dirname(__file__)) # absolute path to the current operatoring system that the file is inside of
# Gives access to the project in ANY os we find ourselves in
# Allows outside files/folders to be added to the project from
# the base directory 

class Config():
    """
    Sets configuration variables for our Flask app here
    Eventually will use hidden variable items - but for now,
    we'll leave them exposed in config
    """
    SECRET_KEY = "You will never guess..."
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Decreases unncessary outpunt in terminal