from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from Model import db, Etudiants, EtudiantSchema, Enseignants, EnseignantSchema, SignupSchema
import uuid

signup_schema = SignupSchema()
etudiant_schema = EtudiantSchema()
enseignant_schema = EnseignantSchema()

class SignupResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = signup_schema.load(json_data)
        if errors:
            return errors, 422
        hashed_password = generate_password_hash(data['password'], method='sha256')
        
        if data['enseignant'] == True:
            enseignant = Enseignants(
                id = data['id'],
                prenom = data['prenom'],
                nom = data['nom'],
                password = hashed_password,
                public_id=str(uuid.uuid4()),
                email = data['email']
                )
            db.session.add(enseignant)
            db.session.commit()
            result = enseignant_schema.dump(enseignant).data
            return { "status": 'success', 'data': result }, 201
        else:
            etudiant = Etudiants(
                id = data['id'],
                prenom = data['prenom'],
                nom = data['nom'],
                password = hashed_password,
                public_id=str(uuid.uuid4()),
                email = data['email']
                )
            db.session.add(etudiant)
            db.session.commit()
            result = etudiant_schema.dump(etudiant).data
            return { "status": 'success', 'data': result }, 201
