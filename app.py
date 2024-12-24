from flask import Flask, render_template, redirect, url_for
from config import secret_key
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp


app = Flask(__name__)
app.secret_key = secret_key
app.config.from_pyfile('config.py')


app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.route("/", methods=["GET"])
def root_redirect():
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)