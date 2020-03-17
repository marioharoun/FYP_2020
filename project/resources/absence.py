from flask import jsonify, request
from flask_restful import Resource
from Model import db, Absence, AbsenceSchema

absences_schema = AbsenceSchema(many=True)
absence_schema = AbsenceSchema()

class AbsenceResource(Resource):
    def get(self):
        absences = Absence.query.all()
        absences = absences_schema.dump(absences).data
        return {"status":"success", "data":absences}, 200

##    def post(self):
##        json_data = request.get_json(force=True)
##        if not json_data:
##               return {'message': 'No input data provided'}, 400
##        # Validate and deserialize input
##        data, errors = comment_schema.load(json_data)
##        if errors:
##            return {"status": "error", "data": errors}, 422
##        category_id = Category.query.filter_by(id=data['category_id']).first()
##        if not category_id:
##            return {'status': 'error', 'message': 'comment category not found'}, 4
##

