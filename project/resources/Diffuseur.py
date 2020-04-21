from flask import request
from flask_restful import Resource
from Model import db, Salles, SalleSchema

salle_schema = SalleSchema()

class DiffuseurResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = salle_schema.load(json_data)
        if errors:
            return errors, 422
        salle = Salles.query.filter_by(major=data['major']).first()
        if salle:
            salle.minor = data['minor']
            db.session.commit()
            result = salle_schema.dump(salle).data
            return { "status": 'success', 'data': result }, 201
        else:
            salle = Salles(
                major = data['major'],
                minor = data['minor']
                )
            db.session.add(salle)
            db.session.commit()
            result = salle_schema.dump(salle).data
            return { "status": 'success', 'data': result }, 201
            
