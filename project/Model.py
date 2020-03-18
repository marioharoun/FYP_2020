##import werkzeug
##werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from sqlalchemy.dialects.postgresql import UUID
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Etudiants(db.Model):
    __tablename__ = 'etudiants'
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(45), nullable=False)
    nom = db.Column(db.String(45), nullable=False)
    mac_address = db.Column(db.String(48))
    presence = db.relationship('Presence', backref='presence_etudiants')
    absence = db.relationship('Absence', backref='absence_etudiants')
    

    def __init__(self, prenom, nom):
        self.prenom = prenom
        self.nom = nom


class Enseignants(db.Model):
    __tablename__ = 'enseignants'
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(45), nullable=False)
    nom = db.Column(db.String(45), nullable=False)
    lecon = db.relationship('Lecons', backref='lecon_enseignant')

    def __init__(self, prenom, nom):
        self.prenom = prenom
        self.nom = nom

class Lecons(db.Model):
    __tablename__ = 'lecons'
    id = db.Column(db.Integer, primary_key=True)
    sujet = db.Column(db.String(45), nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignants.id'))
    session = db.relationship('Session', backref='session_lecons')

    def __init__(self, sujet, enseignant_id):
        self.sujet = sujet
        self.enseignant_id = enseignant_id

class Salles(db.Model):
    __tablename__ = 'salles'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(128)) #ou db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    nom_salle = db.Column(db.String(45), nullable=False)
    session = db.relationship('Session', backref='session_salles')

    def __init__(self, diffuseur_uuid, nom_salle):
        self.diffuseur_uuid = diffuseur_uuid
        self.nom_salle = nom_salle

class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    lecons_id = db.Column(db.Integer, db.ForeignKey('lecons.id'), nullable=False)
    salles_id = db.Column(db.Integer, db.ForeignKey('salles.id'), nullable=False)
    date_debut = db.Column(db.DATETIME, nullable=False)
    date_fin = db.Column(db.DATETIME, nullable=False)
    presence = db.relationship('Presence', backref='presence_session')
    absence = db.relationship('Absence', backref='absence_session')

    def __init__(self, date_debut, date_fin):
        self.date_debut = date_debut
        self.date_fin = date_fin

class Presence(db.Model):
    __tablename__ = 'presence'
    session_id = db.Column(db.Integer, db.ForeignKey('session.id') ,nullable=False)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'),nullable=False)
    date_message = db.Column(db.String, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('etudiant_id', 'session_id'),
        {},)

class Absence(db.Model):
    __tablename__ = 'absence'
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),nullable=False)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'),primary_key=True)

class EtudiantSchema(ma.Schema):
    mac_address = fields.String(required=True)

class PresenceSchema(ma.Schema):
    session_id = fields.Integer(required=True)
    etudiant_id = fields.Integer(required=True)
    date_message = fields.String(required=True)
    uuid = fields.String(required=True)
    mac_address = fields.String(required=True)

class AbsenceSchema(ma.Schema):
    session_id = fields.Integer(required=True)
    etudiant_id = fields.Integer(required=True)

class SalleSchema(ma.Schema):
    uuid = fields.String(required=True)
    
##class Client(db.Model):
##    # human readable name, not required
##    name = db.Column(db.String(40))
##
##    # human readable description, not required
##    description = db.Column(db.String(400))
##
##    # creator of the client, not required
##    user_id = db.Column(db.ForeignKey('user.id'))
##    # required if you need to support client credential
##    user = db.relationship('user')
##
##    client_id = db.Column(db.String(40), primary_key=True)
##    client_secret = db.Column(db.String(55), unique=True, index=True,
##                              nullable=False)
##
##    # public or confidential
##    is_confidential = db.Column(db.Boolean)
##
##    _redirect_uris = db.Column(db.Text)
##    _default_scopes = db.Column(db.Text)
##
##    @property
##    def client_type(self):
##        if self.is_confidential:
##            return 'confidential'
##        return 'public'
##
##    @property
##    def redirect_uris(self):
##        if self._redirect_uris:
##            return self._redirect_uris.split()
##        return []
##
##class Grant(db.Model):
##    id = db.Column(db.Integer, primary_key=True)
##
##    user_id = db.Column(
##        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
##    )
##    user = db.relationship('user')
##
##    client_id = db.Column(
##        db.String(40), db.ForeignKey('client.client_id'),
##        nullable=False,
##    )
##    client = db.relationship('Client')
##
##    code = db.Column(db.String(255), index=True, nullable=False)
##
##    redirect_uri = db.Column(db.String(255))
##    expires = db.Column(db.DateTime)
##
##    _scopes = db.Column(db.Text)
##
##    def delete(self):
##        db.session.delete(self)
##        db.session.commit()
##        return self
##
##    @property
##    def scopes(self):
##        if self._scopes:
##            return self._scopes.split()
##        return []
##
##class Token(db.Model):
##    id = db.Column(db.Integer, primary_key=True)
##    client_id = db.Column(
##        db.String(40), db.ForeignKey('client.client_id'),
##        nullable=False,
##    )
##    client = db.relationship('Client')
##
##    user_id = db.Column(
##        db.Integer, db.ForeignKey('user.id')
##    )
##    user = db.relationship('user')
##
##    # currently only bearer is supported
##    token_type = db.Column(db.String(40))
##
##    access_token = db.Column(db.String(255), unique=True)
##    refresh_token = db.Column(db.String(255), unique=True)
##    expires = db.Column(db.DateTime)
##    _scopes = db.Column(db.Text)
##
##    def delete(self):
##        db.session.delete(self)
##        db.session.commit()
##        return self
##
##    @property
##    def scopes(self):
##        if self._scopes:
##            return self._scopes.split()
##        return []
##
##    @property
##    def default_redirect_uri(self):
##        return self.redirect_uris[0]
##
##    @property
##    def default_scopes(self):
##        if self._default_scopes:
##            return self._default_scopes.split()
##        return []
##
##class user(db.Model):
##    id = db.Column(db.Integer, primary_key=True)
##    username = db.Column(db.String(20), unique=True, nullable=False)
##    email = db.Column(db.String(120), unique=True, nullable=False)
##    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
##    password = db.Column(db.String(60), nullable=False)
