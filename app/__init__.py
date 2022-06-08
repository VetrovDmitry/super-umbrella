from flask import Flask
from flask_login import LoginManager
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api
from flask_jwt_extended import JWTManager
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from os import environ
from dotenv import load_dotenv
from database import db
import config

from utils import read_api_config, api_key_scheme, jwt_scheme


load_dotenv()

CONFIGS = {
    'dev': config.DevelopmentConfig,
    'prod': config.ProductionConfig,
    'test': config.TestingConfig
}

API_CONFIG = read_api_config()


def add_views(app):
    import auth.views as auth_blueprint

    app.register_blueprint(auth_blueprint.auth)

    import chat.controllers as chat_blueprint

    app.register_blueprint(chat_blueprint.chat)

    import main.controllers as main_blueprint

    app.register_blueprint(main_blueprint.main)

    import market.views as market_blueprint

    app.register_blueprint(market_blueprint.market)

    return app


def create_api_and_doc(app):

    spec = APISpec(
        title=API_CONFIG['TITLE'],
        version=API_CONFIG['API_VERSION'],
        plugins=[MarshmallowPlugin()],
        openapi_version=API_CONFIG['OPENAPI_VERSION']
    )
    spec.components.security_scheme('apiKeyAuth', api_key_scheme)
    spec.components.security_scheme('JWT', jwt_scheme)

    app.config.update({
        'APISPEC_SPEC': spec,
        'APISPEC_SWAGGER_URL': API_CONFIG['APISPEC_SWAGGER_URL'],
        'APISPEC_SWAGGER_UI_URL': API_CONFIG['APISPEC_SWAGGER_UI_URL']
    })

    api = Api(app, prefix='/api')
    docs = FlaskApiSpec(app)
    JWTManager(app)

    def add_component(component, route):
        api.add_resource(component, route)
        docs.register(component)

    from auth import endpoints as auth_endpoints
    add_component(auth_endpoints.UserApi, '/user')
    add_component(auth_endpoints.UserSettingsApi, '/users/<int:user_id>')
    add_component(auth_endpoints.UsersApi, '/users')
    add_component(auth_endpoints.TokenApi, '/token')
    add_component(auth_endpoints.SignupApi, '/signup')
    add_component(auth_endpoints.CreateDeviceApi, '/create-device')

    from market import endpoints as market_endpoints
    api.add_resource(market_endpoints.CreateHouseApi, '/create-house')
    docs.register(market_endpoints.CreateHouseApi)

    return app


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIGS[environ['APP_MODE']])

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from auth.models import User
    from chat.models import Membership, Room, Message
    from market.models import House, Photo
    from main.models import Member


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.test_request_context():
        db.create_all()

    app = add_views(app)

    app = create_api_and_doc(app)

    return app