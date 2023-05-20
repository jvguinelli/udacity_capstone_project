from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app):
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()


ownerships = db.Table(
    'ownerships',
    db.Column('company_id', db.Integer, db.ForeignKey('companies.id'),
              primary_key=True),
    db.Column('partner_id', db.Integer, db.ForeignKey('partners.id'),
              primary_key=True)
)


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    fiscal_number = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)

    partners = db.relationship('Partner', secondary=ownerships, lazy=True,
                               backref=db.backref('companies', lazy=True))
    sanctions = db.relationship('Sanction', lazy=True,
                                backref=db.backref('company', lazy=False))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self, partners_info=True, sanctions_info=True):
        company_dict = {
            'id': self.id,
            'fiscal_number': self.fiscal_number,
            'name': self.name
        }

        if partners_info:
            partners_lst = [partner.format(companies_info=False)
                            for partner in self.partners]

            company_dict['partners'] = partners_lst

        if sanctions_info:
            sanctions_lst = [sanction.format() for sanction in self.sanctions]

            company_dict['sanctions'] = sanctions_lst

        return company_dict


class Partner(db.Model):
    __tablename__ = "partners"

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self, companies_info=True):
        partner_dict = {
            'id': self.id,
            'document': self.document,
            'name': self.name
        }

        if companies_info:
            companies_lst = [
                company.format(partners_info=False)
                for company in self.companies
            ]
            partner_dict['companies'] = companies_lst

        return partner_dict


class Sanction(db.Model):
    __tablename__ = "sanctions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'organization': self.organization
        }
