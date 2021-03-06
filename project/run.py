import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, render_template
from resources.Login import token_required

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    @app.route("/index.html")
    def index():
        return render_template("index.html")

    @app.route("/about.html")
    def about():
        return render_template("about.html")
        
    from app import api_bp, signup_bp, login_bp, confirmation_bp, diffuseur_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(signup_bp, url_prefix='/signup')
    app.register_blueprint(confirmation_bp, url_prefix='/confirm_email')
    app.register_blueprint(diffuseur_bp, url_prefix='/diffuseur')

    from resources.ConfirmEmail import mail
    mail.init_app(app)
    

    from Model import db
    db.init_app(app)
    return app



if __name__ == "__main__":
    my_app = create_app('config')
    my_app.run(debug=True)
