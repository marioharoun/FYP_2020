import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
#from flask_oauthlib.provider import OAuth2Provider

#oauth = OAuth2Provider()
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

 #   oauth.init_app(app)
    
    from Model import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
