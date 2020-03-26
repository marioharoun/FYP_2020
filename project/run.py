import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
        
    from app import api_bp, signup_bp, login_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(signup_bp, url_prefix='/signup')

        
    from Model import db
    db.init_app(app)
    return app



if __name__ == "__main__":
    app = create_app('config')
    app.run(debug=True)
