from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, SiteaddrandomForm, SiteForm, SiteupdateForm, SitedeleteForm, \
    SitedeleteallForm, SKUaddForm, SQLForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Site, SKU
from werkzeug.urls import url_parse
from sqlalchemy.sql import text


@app.route('/index')
@login_required
def index():
    sites = Site.query.all()
    sku = SKU.query.all()
    return render_template('Welcome.html', sites=sites, anzahl=len(sites), sku=len(sku))


@app.route('/addSite', methods=['GET', 'POST'])
@login_required
def addSite():
    addSite = [('Bochum', 'NRW', '44787'), ('Berlin', 'Berlin', '10115'), ('Köln', 'NRW', '50667')]
    form1 = SiteaddrandomForm()
    form2 = SiteForm()
    if form1.submit1.data and form1.validate_on_submit():
        check = Site.query.filter_by(name='Bochum').first()
        flash('bereits hinzugefügt!')
        if check is None:
            sites = []
            for name, region, adresse in addSite:
                site = Site(name=name, region=region, adresse=adresse)
                sites.append(site)
            for site in sites:
                db.session.add(site)
            db.session.commit()
            flash('hinzugefügt!')

    if form2.submit2.data and form2.validate_on_submit():
        site = Site(name=form2.name.data, region=form2.region.data, adresse=form2.adresse.data)

        db.session.add(site)
        db.session.commit()
        flash('Site hinzugefügt')
        return redirect(url_for('addSite'))

    return render_template('addSite.html', form1=form1, form2=form2)


@app.route('/updateSite', methods=['GET', 'POST'])
@login_required
def updateSite():
    form = SiteupdateForm()
    if form.validate_on_submit():
        x = form.name.data
        site = Site.query.filter_by(name=x.name).first()
        site.adresse = form.adresse.data
        site.region = form.region.data
        db.session.commit()
    return render_template('updateSite.html', form=form)


@app.route('/deleteSite', methods=['GET', 'POST'])
@login_required
def deleteSite():
    form = SitedeleteForm()
    form1 = SitedeleteallForm()
    if form.submit.data and form.validate_on_submit():
        x = form.name.data
        print(x.name)
        site = Site.query.filter_by(name=x.name).first()
        db.session.delete(site)
        db.session.commit()
    if form1.submit1.data and form1.validate_on_submit():
        sites = Site.query.all()
        for site in sites:
            db.session.delete(site)
        db.session.commit()
    return render_template('deleteSite.html', form=form, form1=form1)


@app.route('/addSKU', methods=['GET', 'POST'] )
@login_required
def addSKU():
    form = SKUaddForm()
    if form.submit.data and form.validate_on_submit():
        sku = SKU(name=form.name.data, sortiment=form.sortiment.data, gewicht=form.gewicht.data, standort= form.standort.data)
        db.session.add(sku)
        db.session.commit()
    return render_template('addSKU.html', form=form)

@app.route('/SQL', methods=['GET', 'POST'] )
@login_required
def SQL():
    form = SQLForm()
    if form.submit.data and form.validate_on_submit():
        db.engine.execute(text(form.sql.data))
    return render_template('SQL.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Falscher/s Username oder Passwort')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))

    return render_template('login.html', title='Anmeldung', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sie sind nun regestriert!')
        return redirect(url_for('login'))
    return render_template('regestrieren.html', title='Register', form=form)
