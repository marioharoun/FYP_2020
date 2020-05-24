from flask import request
from flask_restful import Resource
from Model import db, Etudiants, Enseignants, Lecons, Salles, Session, SessionSchema
from .Login import token_required


session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

class CreatesessionResource(Resource):
    @token_required
    def post(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        
        data, errors = session_schema.load(json_data)
        if errors:
            return errors, 422

        lecon = Lecons.query.filter_by(id=data['lecons_id']).first()
        enseignant = Enseignants.query.filter_by(id=lecon.enseignant_id).first()

        if not current_user[0]==enseignant:
            return {'message': 'Action Forbidden!'}, 403
        
        session = Session(
            salles_id=data['salles_id'],
            date_debut=data['date_debut'],
            lecons_id=data['lecons_id'],
            )
        
        db.session.add(session)
        db.session.commit()
        session = Session.query.filter_by(lecons_id=data['lecons_id']).all()
        result = sessions_schema.dump(session).data
        result = result[len(result)-1]

        return 'Le numero de la seance est: ' +str(result['id']), 201
