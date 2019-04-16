"""Formen für die vordefinierten Maßnahmen und den Login"""
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Site, SKU
from wtforms_alchemy.fields import QuerySelectField

"""Darstellung der Login Form"""
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('angemeldet bleiben')
    submit = SubmitField('Anmelden')

"""Darstellung der Regestrations Form"""
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Regestrieren')

    """Überprüfung auf bestehenden Usernamen"""
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Bitte benutzen Sie einen anderen Usernamen')

    """Überprüfung auf bestehende Email"""
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte benutzen Sie eine andere Emailadresse')

"""Erstellen von 3 fest definierten Sites"""
class SiteaddrandomForm(FlaskForm):
    submit1 = SubmitField('3 Sites hinzufügen')

    """Überprüfung ob die Sites schon existieren"""
    def validate_site(self):
        site = Site.query.filter_by(name='Bochum').first()
        if site is not None:
            raise ValidationError('Diese Sites existieren bereits')

"""Form zum erstellen von einer Site"""
class SiteForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], description="Dortmund")
    region = StringField('Region', validators=[DataRequired()], description="NRW" )
    adresse = StringField('Adresse', validators=[DataRequired()], description="44135")
    submit2 = SubmitField('Hinzufügen')

    def validate_name(self, name):
        name = Site.query.filter_by(name=name.data).first()
        if name is not None:
            raise ValidationError('Diese Site existiert bereits')


"""Query zur Abfrage von bestehenden Sites"""
def querySites():
    return Site.query

"""Form zum bearbeiten einer bestehenden Site"""
class SiteupdateForm(FlaskForm):
    name = QuerySelectField(query_factory=querySites)
    region = StringField('Region', description="NRW")
    adresse = StringField('Adresse', description="44135")
    submit = SubmitField('Bearbeiten')

"""Form zum Löschen von einer Site"""
class SitedeleteForm(FlaskForm):
    name = QuerySelectField(query_factory=querySites)
    submit = SubmitField('Löschen')

"""Form zum Löschen aller Sites"""
class SitedeleteallForm(FlaskForm):
    submit1 = SubmitField('Alle löschen')

"""Form zum erstellen von SKU"""
class SKUaddForm(FlaskForm):
    standort = QuerySelectField(query_factory=querySites)
    name = StringField('Name', validators=[DataRequired()], description="Nike7839")
    sortiment = StringField('Sortiment', description="Schuhe")
    gewicht = FloatField("Gewicht", description='0.500')
    submit = SubmitField('Hinzufügen')

    """Probleme beim validate!!!"""
    def validate_name_standort(self, name, standort):
        x = standort.data
        site = Site.query.filter_by(name=x.name).first()
        sitename = site.name

        skus = site.skus.filter_by(name=name.data).first()
        lol = skus.standort.name
        if sitename == lol:
            raise ValidationError('Diese SKU existiert bereits in diesem Standort')
"""Form zum erstellen von plain SQL"""
class SQLForm(FlaskForm):
    sql = TextAreaField('SQLStatement', validators=[DataRequired()], description="SQL")
    submit = SubmitField('Ausführen')