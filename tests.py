"""Testumgebung für die Datenbankabstraktionsschicht"""

import unittest
from app import app, db
from app.models import Site, SKU
from sqlalchemy.sql import text


class UserModelCase(unittest.TestCase):
    """Erstellen der Testdatenbank in Memory"""
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    """Löschen der Testdatenbank"""
    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_sites_skus(self):
        """Erstelle 4 Sites"""
        s1 = Site(name='Dortmund', region='NRW', adresse='44135')
        s2 = Site(name='Münster', region='NRW', adresse='48143')
        s3 = Site(name='Berlin', region='Berlin', adresse='10115')
        s4 = Site(name='Hamburg', region='Hamburg', adresse='20095')
        db.session.add_all([s1, s2, s3, s4])

        """Erstelle 4 SKU"""
        sku1 = SKU(name='nike', sortiment='schuhe', gewicht='0.5')
        sku2 = SKU(name='adidas', sortiment='schuhe', gewicht='0.5')
        sku3 = SKU(name='puma', sortiment='schuhe', gewicht='0.5')
        sku4 = SKU(name='erima', sortiment='schuhe', gewicht='0.5')
        db.session.add_all([sku1, sku2, sku3, sku4])
        db.session.commit()

        """Ordne jeweils einer Site ein SKU zu"""
        sku1.standort = s1
        sku2.standort = s2
        sku3.standort = s3
        sku4.standort = s4
        db.session.commit()

        """Überprüfe die Einträge per Query"""

        f1 = Site.query.all()
        f2 = SKU.query.all()
        f3 = Site.query.get(1)
        f3.skus.all()

    def test_core(self):
        """Test von plain SQL"""
        db.engine.execute(text("INSERT INTO site (name, region, adresse) VALUES ('Dortmund', 'NRW', '44135');"))

if __name__ == '__main__':
    unittest.main(verbosity=2)