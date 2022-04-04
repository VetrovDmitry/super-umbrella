from flask import Flask
from flask_login import LoginManager
from os import environ
from .database import db
from config import DevelopmentConfig, TestingConfig, ProductionConfig


CONFIGS = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIGS[environ['APP_MODE']])

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .auth.models import User
    from .chat.models import Member, Membership, Room, Message
    from .market.models import House, Photo

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.test_request_context():
        db.create_all()

    import app.auth.controllers as auth_blueprint

    app.register_blueprint(auth_blueprint.auth)

    import app.chat.controllers as chat_blueprint

    app.register_blueprint(chat_blueprint.chat)

    import app.main.controllers as main_blueprint

    app.register_blueprint(main_blueprint.main)

    import app.market.controllers as market_blueprint

    app.register_blueprint(market_blueprint.market)

    return app