from flask import Blueprint
from flask_restful import Api
from flask_oauthlib.provider import OAuth2Provider
from resources.Hello import Hello
from resources.Presence import PresenceResource
from resources.Absence import AbsenceResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/Hello')
api.add_resource(PresenceResource, '/Presence')
api.add_resource(AbsenceResource, '/Absence')
