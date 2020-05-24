from flask import request
from flask_restful import Resource
from Model import db, Presence, PresenceSchema, Etudiants, EtudiantSchema, Salles, Session, PresenceSchema_2
from .Login import token_required
from datetime import date

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
        j=0
        session=request.args.getlist('session_id')
        lecon=request.args.getlist('lecon_id')
        if session[0]=='all':
            sessions = Session.query.filter_by(lecons_id=int(lecon[0])).all()
            session=[]
            for elmt in sessions:
                session.append(elmt.id)
        for presences in session:
            duplicate=[]
            count = {}
            presences = Presence.query.filter_by(session_id=session[i]).all()
            for elmt in presences:
                if elmt.etudiant_id:
                    if elmt.etudiant_id in count.keys():
                        count[elmt.etudiant_id]+=1
                        if count[elmt.etudiant_id] >= 2  and elmt.etudiant_id not in duplicate:
                            duplicate.append(elmt.etudiant_id)
                            presences_data.append({'seance':session[i],'matricule':elmt.etudiant_id,'date':str(elmt.date_message)})
                    else:
                        count[elmt.etudiant_id]=1
                if elmt.etudiant_id_non_registre:
                    if elmt.etudiant_id_non_registre in count.keys():
                        count[elmt.etudiant_id_non_registre]+=1
                        if count[elmt.etudiant_id_non_registre] >= 2  and elmt.etudiant_id_non_registre not in duplicate:
                            duplicate.append(elmt.etudiant_id_non_registre)
                            presences_data.append({'seance':session[i],'matricule':elmt.etudiant_id_non_registre,'date':str(elmt.date_message)})
                    else:
                        count[elmt.etudiant_id_non_registre]=1
            
            i=i+1
        return presences_data, 200

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
        entries = Presence.query.filter_by(etudiant_id=data['etudiant_id'],
                                           session_id=data['session_id']).all()
        num_entries = len(entries)
        if entries != []:
            if entries[num_entries - 1].minor == data['minor']:
                return {'message': 'Wait for another submission!'}, 400
            if not (num_entries <= 2):
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
        elif etudiant1 != [] and etudiant.mac_address != []:
            for i in etudiant1:
                if i.id != data['etudiant_id']:
                    return {'message': 'Invalid device!'}, 400
        elif etudiant1 != [] and etudiant.mac_address == []:
            return {'message': 'Invalid device!'}, 400
        
        db.session.commit()

        presence = Presence(
            session_id=data['session_id'],
            etudiant_id=data['etudiant_id'],
            date_message=data['date_message'],############### Differs in heroku
            major=data['major'],
            minor=data['minor']
            )
        
        db.session.add(presence)
        db.session.commit()

        result = presence_schema.dump(presence).data

        return { "status": 'success', 'data': result }, 201

    @token_required
    def put(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        session_id=request.args.get('session_id')
        etudiant_id=request.args.get('etudiant_id')
        
        if etudiant_id != None and session_id == None:
            return { 'message': 'Pas de seance inclut!'}, 400
        elif etudiant_id == None and session_id == None:
            return { 'message': 'Pas darguments!'}, 400
        elif etudiant_id == None and session_id != None:
            return { 'message': 'pas detudiant inclut!'}, 400
        else:
            query_1 = Etudiants.query.filter_by(id = etudiant_id).first()
            query_2 = Session.query.filter_by(id = session_id).first()
            
        if query_1 and query_2:
            presence_1 = Presence(
            session_id=session_id,
            etudiant_id=etudiant_id,
            date_message=date.today())

            presence_2 = Presence(
            session_id=session_id,
            etudiant_id=etudiant_id,
            date_message=date.today())

            db.session.add(presence_1)
            db.session.add(presence_2)

            try:
                db.session.commit()
            except:
                return { 'message': 'Échec dajouter la ressource!'}, 400
            return { 'message': 'Resource ajoutee avec succes!'}, 200
        elif not query_1:
            presence_1 = Presence(
            session_id=session_id,
            etudiant_id_non_registre=etudiant_id,
            date_message=date.today())

            presence_2 = Presence(
            session_id=session_id,
            etudiant_id_non_registre=etudiant_id,
            date_message=date.today())

            db.session.add(presence_1)
            db.session.add(presence_2)
            try:
                db.session.commit()
            except:
                return { 'message': 'Échec dajouter la ressource!'}, 400
            return { 'message': 'Resource ajoutee avec succes!'}, 200
        else:
            return { 'message': 'Échec dajouter la ressource!'}, 400
        

    @token_required
    def delete(current_user, self):
        if current_user[1]==False:
            return {'message': 'Access Denied!'}, 403
        session_id=request.args.get('session_id')
        etudiant_id=request.args.get('etudiant_id')
        
        if etudiant_id != None and session_id == None:
            query = Presence.query.filter_by(etudiant_id= etudiant_id).all()
        elif etudiant_id == None and session_id == None:
            return { 'message': 'No arguments included!'}, 400
        elif etudiant_id == None and session_id != None:
            query = Presence.query.filter_by(session_id= session_id).all()
        else:
            query_1 = Presence.query.filter_by(session_id= session_id,
                                             etudiant_id= etudiant_id).all()
            query_2 = Presence.query.filter_by(session_id= session_id,
                                             etudiant_id_non_registre= etudiant_id).all()
            if query_1:
                for i in query:
                    db.session.delete(i)
            if query_2:
                for i in query:
                    db.session.delete(i)
        
        try:
            db.commit()
        except:
            { 'message': 'Resource deleted successfully!'}, 200
            

