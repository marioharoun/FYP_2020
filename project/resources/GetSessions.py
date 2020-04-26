from flask import request
from flask_restful import Resource
from Model import db, Session
from .Login import token_required



class GetSessionsResource(Resource):
    @token_required
    def get(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        data={}
        lecon=request.args.getlist('lecon_id')
        for i in lecon:
            sessions_data={}
            query = Session.query.filter_by(lecons_id=i)
            for j in query:
                sessions_data[j.id]=str(j.date_debut)
            data[i]=sessions_data
        return data, 200
        
