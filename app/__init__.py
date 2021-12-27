from flask import Flask
from flask_login import LoginManager
from .database import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .auth.models import User
    from .chat.models import Member, Membership, Room, Message

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.test_request_context():
        db.create_all()

    import app.auth.controllers as auth_blueprint

    app.register_blueprint(auth_blueprint.auth)

    import app.chat.controllers as chat_blueprint

    app.register_blueprint(chat_blueprint.chat)

    return app