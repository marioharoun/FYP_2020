from flask import request
from flask_restful import Resource
from Model import db, Lecons, LeconSchema, Enseignants
from .Login import token_required

lecon_schema = LeconSchema()

class LeconResource(Resource):
    @token_required
    def get(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        lecons_data=[]
        lecons = Lecons.query.filter_by(enseignant_id=current_user[0].id).all()
        for elmt in lecons:
            lecons_data.append(lecon_schema.dump(elmt).data)
        return lecons_data, 200
