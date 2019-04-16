"""Defintion des Datenbankschemas"""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

"""Relation für Benutzer"""
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    a= db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

"""Relation für Sites"""
class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    region = db.Column(db.String(64))
    adresse = db.Column(db.String(64))
    skus = db.relationship('SKU', backref='standort', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return "<Site(name='%s', region='%s', adresse='%s')>" % (
            self.name, self.region, self.adresse)

"""Relation für SKU"""
class SKU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    sortiment = db.Column(db.String(64))
    gewicht = db.Column(db.Float)
    site_name = db.Column(db.String, db.ForeignKey('site.name'))
    bestand = db.Column(db.Integer)

    def __repr__(self):
        return "<SKU(name='%s', sortiment='%s', gewicht='%s')>" % (
             self.name, self.sortiment, self.gewicht)