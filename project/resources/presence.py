from flask import request
from flask_restful import Resource
from Model import db, Presence, PresenceSchema, Etudiants, EtudiantSchema, Salles

presences_schema = PresenceSchema(many=True)
presence_schema = PresenceSchema()

etudiants_schema = EtudiantSchema(many=True)
etudiant_schema = EtudiantSchema()

class PresenceResource(Resource):
    def get(self):
        presences = Presence.query.all()
        presences = presences_schema.dump(presences).data
        return {'status': 'success1', 'data': presences}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = presence_schema.load(json_data)
        if errors:
            return errors, 422
        uuid = Salles.query.filter_by(uuid=data['uuid']).first()
        if not uuid:
            return {'message': 'UUID invalide'}, 400
        etudiant = Etudiants.query.filter_by(id=json_data['etudiant_id'])
        etudiant.mac_address = json_data['mac_address']
        db.session.commit()

        presence = Presence(
            session_id=json_data['session_id'],
            etudiant_id=json_data['etudiant_id'],
            date_message=json_data['date_message']
            )
        
        db.session.add(presence)
        db.session.commit()

        result = presence_schema.dump(presence).data

        return { "status": 'success', 'data': result }, 201

##    def put(self):
##        json_data = request.get_json(force=True)
##        if not json_data:
##               return {'message': 'No input data provided'}, 400
##        # Validate and deserialize input
##        data, errors = category_schema.load(json_data)
##        if errors:
##            return errors, 422
##        category = Category.query.filter_by(id=data['id']).first()
##        if not category:
##            return {'message': 'Category does not exist'}, 400
##        category.name = data['name']
##        db.session.commit()
##
##        result = category_schema.dump(category).data
##
##        return { "status": 'success', 'data': result }, 204
##
##    def delete(self):
##        json_data = request.get_json(force=True)
##        if not json_data:
##               return {'message': 'No input data provided'}, 400
##        # Validate and deserialize input
##        data, errors = category_schema.load(json_data)
##        if errors:
##            return errors, 422
##        category = Category.query.filter_by(id=data['id']).delete()
##        db.session.commit()
##
##        result = category_schema.dump(category).data
##
##        return { "status": 'success', 'data': result}, 204
##
