import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '542bed3a43a4a42ec1a5cbdbfac2d9015343bfb3f885061c'
    
    # Fix the DATABASE_URL by replacing 'postgres://' with 'postgresql://'
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://")

    SQLALCHEMY_DATABASE_URI = database_url or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
