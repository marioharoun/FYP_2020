from flask import request
from flask_restful import Resource
from Model import db, Presence, PresenceSchema
from .Login import token_required

presences_schema = PresenceSchema(many=True)

class GetEtudiantsResource(Resource):
    @token_required
    def get(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        data={}
        session=request.args.getlist('session_id')
        for i in session:
            etudiants_data={}
            query = Presence.query.filter_by(session_id=i)
            for j in query:
                if j.etudiant_id not in etudiants_data.keys():
                    etudiants_data[j.etudiant_id] = 1
                else:
                    etudiants_data[j.etudiant_id] = etudiants_data[j.etudiant_id] + 1
            data[i]=etudiants_data
        return data, 200
        
