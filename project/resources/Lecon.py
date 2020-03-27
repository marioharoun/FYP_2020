from flask import request
from flask_restful import Resource
from Model import db, Lecons, LeconSchema, Enseignants
from .Login import token_required

lecons_schema = LeconSchema(many=True)

class LeconResource(Resource):
    @token_required
    def get(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        
        lecons = Lecons.query.filter_by(enseignant_id=current_user[0].id).all()
        lecons = lecons_schema.dump(lecons).data
        return {'status': 'success', 'data': lecons}, 200
