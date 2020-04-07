##import werkzeug
##werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from sqlalchemy.dialects.postgresql import UUID
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

ma = Marshmallow()
db = SQLAlchemy()

##Pour assurer la dependance des cles etrangeres sur SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
##

class Etudiants(db.Model):
    __tablename__ = 'etudiants'
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(45), nullable=False)
    nom = db.Column(db.String(45), nullable=False)
    public_id = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    mac_address = db.Column(db.String(48), unique=True)
    confirmation = db.Column(db.Boolean, unique=False, default=False)
    presence = db.relationship('Presence', backref='presence_etudiants')
    absence = db.relationship('Absence', backref='absence_etudiants')

class Enseignants(db.Model):
    __tablename__ = 'enseignants'
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(45), nullable=False)
    nom = db.Column(db.String(45), nullable=False)
    public_id = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    confirmation = db.Column(db.Boolean, unique=False, default=False)
    lecon = db.relationship('Lecons', backref='lecon_enseignant')

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
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    presence = db.relationship('Presence', backref='presence_session')
    absence = db.relationship('Absence', backref='absence_session')

class Presence(db.Model):
    __tablename__ = 'presence'
    session_id = db.Column(db.Integer, db.ForeignKey('session.id') ,nullable=False)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'),nullable=False)
    date_message = db.Column(db.Date, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('session_id','etudiant_id'),
        {},)

class Absence(db.Model):
    __tablename__ = 'absence'
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),nullable=False)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'),primary_key=True)

class EtudiantSchema(ma.Schema):
    id = fields.Integer(required=True)
    email = fields.String(required=True)
    nom = fields.String()
    prenom = fields.String()

class EnseignantSchema(ma.Schema):
    id = fields.Integer(required=True)
    email = fields.Email(required=True)
    nom = fields.String()
    prenom = fields.String()

class SignupSchema(ma.Schema):
    id = fields.Integer(required=True)
    email = fields.Email(required=True)
    nom = fields.String(required=True)
    prenom = fields.String(required=True)
    password = fields.String(required=True)
    enseignant = fields.Boolean(required=True)

class SessionSchema(ma.Schema):
    id = fields.Integer()
    salles_id = fields.Integer(required=True)
    date_debut = fields.DateTime(required=True)
    date_fin = fields.DateTime(required=True)
    lecons_id = fields.Integer(required=True)

class LeconSchema(ma.Schema):
    id = fields.Integer()
    sujet = fields.String(required=True)
    enseignant_id = fields.Integer(required=True)


class PresenceSchema(ma.Schema):
    session_id = fields.Integer(required=True)
    etudiant_id = fields.Integer(required=True)
    date_message = fields.DateTime(required=True)
    uuid = fields.String(required=True)
    mac_address = fields.String(required=True)

class AbsenceSchema(ma.Schema):
    session_id = fields.Integer(required=True)
    etudiant_id = fields.Integer(required=True)

class SalleSchema(ma.Schema):
    uuid = fields.String(required=True)
    
