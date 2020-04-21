from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Presence import PresenceResource
from resources.Absence import AbsenceResource
from resources.Signup import SignupResource
from resources.Login import LoginResource
from resources.Createsession import CreatesessionResource
from resources.Lecon import LeconResource
from resources.ConfirmEmail import ConfirmEmailResource
from resources.Diffuseur import DiffuseurResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/Hello')
api.add_resource(PresenceResource, '/Presence')
api.add_resource(AbsenceResource, '/Absence')
api.add_resource(CreatesessionResource, '/Createsession')
api.add_resource(LeconResource, '/Lecon')


login_bp = Blueprint('login', __name__)
login = Api(login_bp)

# Route
login.add_resource(LoginResource, '/')


signup_bp = Blueprint('signup', __name__)
signup = Api(signup_bp)

# Route
signup.add_resource(SignupResource,'/')


confirmation_bp = Blueprint('confirmation', __name__)
confirmation = Api(confirmation_bp)

# Route
confirmation.add_resource(ConfirmEmailResource,'/')


diffuseur_bp = Blueprint('diffuseur', __name__)
diffuseur = Api(diffuseur_bp)

# Route
diffuseur.add_resource(DiffuseurResource,'/')

