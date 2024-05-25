from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Añadir Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Configurar la clave secreta
    app.secret_key = 'your_secret_key_here'

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Inicializar Flask-Migrate

    login_manager.login_view = 'login'

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app



