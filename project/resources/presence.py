from flask import request
from flask_restful import Resource
from Model import db, Presence, PresenceSchema, Etudiants, EtudiantSchema, Salles, Session
from .Login import token_required

presences_schema = PresenceSchema(many=True)
presence_schema = PresenceSchema()

etudiants_schema = EtudiantSchema(many=True)
etudiant_schema = EtudiantSchema()


class PresenceResource(Resource):
    @token_required
    def get(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        presences_data=[]
        i=0
        session=request.args.getlist('session_id')
        for presences in session:
            presences = Presence.query.filter_by(session_id=session[i])
            presences_data.append(presences_schema.dump(presences).data)
            i=i+1
        return {'status': 'success1', 'data': presences_data}, 200

    @token_required
    def post(current_user, self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = presence_schema.load(json_data)
        if errors:
            return errors, 422
        if current_user[0].id!=data['etudiant_id']:
            return {'message': 'Access denied!'}, 403
        
        entries = len(db.session.query(Presence).filter(Presence.etudiant_id == data['etudiant_id'],
                                               Presence.session_id == data['session_id']).all())
        if not (entries <= 2):
            return {'message': 'Exceeded number of entries for the session!'}, 400
        
        salle = Salles.query.filter_by(uuid=data['uuid']).first()
        if not salle:
            return {'message': 'UUID invalide'}, 400
        salle = Salles.query.filter_by(major=data['major']).first()
        session = Session.query.filter_by(id=data['session_id']).first()
        if not salle:
            return {'message': 'Wrong class!'}, 400
        elif salle.id != session.salles_id:
            return {'message': 'Wrong class!'}, 400
        elif salle.minor != data['minor']:
            return {'message': 'Invalid data!'}, 400
        
        etudiant = Etudiants.query.filter_by(id=data['etudiant_id']).first()
        etudiant1 = Etudiants.query.filter_by(mac_address=data['mac_address']).all()
        if etudiant1 == []:
            etudiant.mac_address = data['mac_address']
        elif etudiant.mac_address != None and etudiant1 != []:
            for i in etudiant1:
                if i.id != data['etudiant_id']:
                    return {'message': 'Invalid device!'}, 400
        elif etudiant.mac_address = None:
            etudiant.mac_address = data['mac_address']
        
        db.session.commit()

        presence = Presence(
            session_id=data['session_id'],
            etudiant_id=data['etudiant_id'],
            date_message=data['date_message']
            )
        
        db.session.add(presence)
        db.session.commit()

        result = presence_schema.dump(presence).data

        return { "status": 'success', 'data': result }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        category = Category.query.filter_by(id=data['id']).first()
        if not category:
            return {'message': 'Category does not exist'}, 400
        category.name = data['name']
        db.session.commit()

        result = category_schema.dump(category).data

        return { "status": 'success', 'data': result }, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        category = Category.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = category_schema.dump(category).data

        return { "status": 'success', 'data': result}, 204

