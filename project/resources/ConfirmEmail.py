from flask import Flask, request, url_for
from flask_mail import Mail, Message
from flask_restful import Resource
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from config import SECRET_KEY
from Model import db, Etudiants, Enseignants

mail = Mail()
s = URLSafeTimedSerializer(SECRET_KEY)

def send_email(email):
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='attendance.usj@outlook.com', recipients=[email])

    link = url_for('confirmation.confirmemailresource', token=token, _external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)


class ConfirmEmailResource(Resource):
    def get(self):
        token=request.args['token']
        try:
            email_sent = s.loads(token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            return {'error' : 'Link has expired!'}
        etudiant = Etudiants.query.filter_by(email=email_sent).first()
        enseignant = Enseignants.query.filter_by(email=email_sent).first()
        if etudiant:
            etudiant.confirmation=True
            db.session.commit()
            return {'sucess' : 'Email Verified!'}
        if enseignant:
            enseignant.confirmation=True
            db.session.commit()
            return {'sucess' : 'Email Verified!'}
