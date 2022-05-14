from flask import Flask
from flask_login import LoginManager
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from os import environ
from dotenv import load_dotenv
from database import db
import config
from utils import read_api_config


load_dotenv()

CONFIGS = {
    'dev': config.DevelopmentConfig,
    'prod': config.ProductionConfig,
    'test': config.TestingConfig
}

API_CONFIG = read_api_config()


def add_views(app):
    import auth.controllers as auth_blueprint

    app.register_blueprint(auth_blueprint.auth)

    import chat.controllers as chat_blueprint

    app.register_blueprint(chat_blueprint.chat)

    import main.controllers as main_blueprint

    app.register_blueprint(main_blueprint.main)

    import market.controllers as market_blueprint

    app.register_blueprint(market_blueprint.market)

    return app


def create_api_and_doc(app):
    api = Api(app)
    docs = FlaskApiSpec(app)

    from auth import endpoints as auth_endpoints
    api.add_resource(auth_endpoints.UserApi, '/api/user')
    docs.register(auth_endpoints.UserApi)
    api.add_resource(auth_endpoints.UserSettingsApi, '/api/users/<int:user_id>')
    docs.register(auth_endpoints.UserSettingsApi)
    api.add_resource(auth_endpoints.UsersApi, '/api/users')
    docs.register(auth_endpoints.UsersApi)

    return app


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIGS[environ['APP_MODE']])
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title=API_CONFIG['TITLE'],
            version=API_CONFIG['API_VERSION'],
            plugins=[MarshmallowPlugin()],
            openapi_version=API_CONFIG['OPENAPI_VERSION']
        ),
        'APISPEC_SWAGGER_URL': API_CONFIG['APISPEC_SWAGGER_URL'],
        'APISPEC_SWAGGER_UI_URL': API_CONFIG['APISPEC_SWAGGER_UI_URL']
    })
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from auth.models import User
    from chat.models import Member, Membership, Room, Message
    from market.models import House, Photo

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.test_request_context():
        db.create_all()

    app = add_views(app)

    app = create_api_and_doc(app)

    return app