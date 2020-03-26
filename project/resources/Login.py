from flask import request, make_response
from flask_restful import Resource
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from Model import db, Etudiants, Enseignants
import jwt
import datetime
from config import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'message' : 'Token is missing!'}, 401
        data = jwt.decode(token, SECRET_KEY)

        current_user = Enseignants.query.filter_by(public_id=data['public_id']).first()
        if current_user:
            return f([current_user,True], *args, **kwargs)

        current_user = Etudiants.query.filter_by(public_id=data['public_id']).first()
        if current_user:
            return f([current_user,False], *args, **kwargs)
        return {'message' : 'Token is missing!'}, 401

    return decorated

class LoginResource(Resource):
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm=Login required!'})
        enseignant = Enseignants.query.filter_by(id=auth.username).first()
        etudiant = Etudiants.query.filter_by(id=auth.username).first()
        if not enseignant and not etudiant:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm=Login required!'})
        if enseignant:
            if check_password_hash(enseignant.password, auth.password):
                token = jwt.encode({'public_id' : enseignant.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}, SECRET_KEY)
                return {'token' : token.decode('UTF-8')}
        if etudiant:
            if check_password_hash(etudiant.password, auth.password):
                token = jwt.encode({'public_id' : etudiant.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
                return {'token' : token.decode('UTF-8')}

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm=Login required!'})
