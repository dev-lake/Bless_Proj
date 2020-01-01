import os

base_url = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'IJIIHUIJIUHIUHUH'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        default='sqlite:///' + os.path.join(base_url, 'data.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_AS_ASCII = False

    # API中每页显示条数
    API_ITEMS_PER_PAGE = 15

    # config for Flask-BaiscAuth
    BASIC_AUTH_USERNAME = 'admin'
    BASIC_AUTH_PASSWORD = 'bless'
