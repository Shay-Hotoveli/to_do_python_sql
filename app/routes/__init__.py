from .auth_routes import auth_bp
from .user_routes import user_bp
from .admin_routes import admin_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)