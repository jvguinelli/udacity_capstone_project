import unittest
import json
import random

from src import create_app
from src.database.models import db, Company, Partner, Sanction, ownerships


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres",
            "postgres",
            "localhost:5432",
            "capstone_project"
        )

        test_config = {
            'SQLALCHEMY_DATABASE_URI': self.database_path,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }

        self.app = create_app(test_config)
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            # create all tables
            self.db.create_all()

        self.admin_token = ""
        self.normal_user_token = ""

        self.admin_headers = {
            "Authorization": f"Bearer {self.admin_token}"
        }
        self.normal_user_headers = {
            "Authorization": f"Bearer {self.normal_user_token}"
        }

        self.new_santion = {
            "name": "CEIS - Cadastro de Empresas Inidôneas e Suspensas",
            "organization": "CGU - CONTROLADORIA GERAL DA UNIAO"
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    def assert_error404(self, res):
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "not found")

    # COMPANIES

    def test_get_companies_with_normal_user_headers(self):
        res = self.client().get('/companies',
                                headers=self.normal_user_headers)
        data = json.loads(res.data)

        with self.app.app_context():
            companies_lst = [c.format() for c in Company.query.all()]

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertListEqual(data['companies'], companies_lst)

    def test_create_company(self):
        new_company = {
            "fiscal_number": str(random.randint(1, 99999999999999)).zfill(14),
            "name": "INDELBROM DO BRASIL"
        }

        res = self.client().post('/companies',
                                 json=new_company,
                                 headers=self.admin_headers)
        data = json.loads(res.data)

        with self.app.app_context():
            self.assertEqual(res.status_code, 201)
            self.assertTrue(data['success'])
            self.assertTrue(data['created'])

            # assert the new company was created in database
            company_count = Company.query\
                .filter(Company.id == data['created'])\
                .count()
            self.assertEqual(company_count, 1)

    def test_error_422_create_company_with_existent_fiscal_number(self):
        with self.app.app_context():
            fiscal_number = Company.query \
                .with_entities(Company.fiscal_number) \
                .first()[0]

            new_company = {
                "fiscal_number": fiscal_number,
                "name": "INDELBROM DO BRASIL"
            }

            res = self.client().post('/companies',
                                     json=new_company,
                                     headers=self.admin_headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'unprocessable')

    def test_update_company(self):
        with self.app.app_context():
            # get id from first company in db
            company_id = Company.query \
                .with_entities(Company.id) \
                .order_by(Company.id) \
                .first()[0]
            res = self.client().patch(f'/companies/{company_id}',
                                      json={'name': 'INDELBROM DE SUMIDOURO'},
                                      headers=self.admin_headers)
            data = json.loads(res.data)
            company = Company.query \
                .filter(Company.id == company_id).one_or_none()

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(company.format()['name'],
                             'INDELBROM DE SUMIDOURO')

    def test_error_404_update_non_existent_company(self):
        with self.app.app_context():
            res = self.client().patch('/companies/100000',
                                      json={'name': 'INDELBROM DE SUMIDOURO'},
                                      headers=self.admin_headers)

            self.assert_error404(res)

    def test_del_company(self):
        with self.app.app_context():
            # get id of first company in db
            company_id = Company.query \
                .with_entities(Company.id) \
                .order_by(Company.id) \
                .first()[0]

            res = self.client().delete(f'/companies/{company_id}',
                                       headers=self.admin_headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], company_id)

            company = Company.query\
                .filter(Company.id == data['deleted'])\
                .one_or_none()

            self.assertEqual(company, None)

    def test_error_404_del_non_existent_company(self):
        with self.app.app_context():
            res = self.client().delete('/companies/100000',
                                       headers=self.admin_headers)

            self.assert_error404(res)

    def test_add_partner_to_company(self):
        with self.app.app_context():
            # get id of first company in db
            company_id = Company.query \
                .with_entities(Company.id) \
                .order_by(Company.id) \
                .first()[0]

            # get id of first partnet in db
            partner_id = Partner.query \
                .with_entities(Partner.id) \
                .order_by(Partner.id) \
                .first()[0]

            res = self.client().put(
                f'/companies/{company_id}/partners/{partner_id}',
                headers=self.admin_headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])

            ownerships_count = db.session.query(ownerships)\
                .filter(Company.id == company_id, Partner.id == partner_id) \
                .count()
            self.assertEqual(ownerships_count, 1)

    def test_error_404_add_partner_to_non_existent_company(self):
        with self.app.app_context():
            res = self.client().put(
                '/companies/100000/partners/100000',
                headers=self.admin_headers)

            self.assert_error404(res)

    # # PARTNERS

    def test_get_partners(self):
        res = self.client().get('/partners',
                                headers=self.admin_headers)
        data = json.loads(res.data)

        with self.app.app_context():
            partners_lst = [p.format() for p in Partner.query.all()]

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertListEqual(data['partners'], partners_lst)

    def test_create_partner(self):
        new_partner = {
            "document": str(random.randint(1, 99999999999)).zfill(11),
            "name": "ROSELINO SILVA",
        }

        res = self.client().post('/partners',
                                 json=new_partner,
                                 headers=self.admin_headers)
        data = json.loads(res.data)

        with self.app.app_context():
            self.assertEqual(res.status_code, 201)
            self.assertTrue(data['success'])
            self.assertTrue(data['created'])

            # assert the new partner was created in database
            partner_count = Partner.query\
                .filter(Partner.id == data['created'])\
                .count()
            self.assertEqual(partner_count, 1)

    def test_error_422_create_partner_with_existent_document(self):

        with self.app.app_context():
            document = Partner.query \
                .with_entities(Partner.document) \
                .first()[0]

            new_partner = {
                "document": document,
                "name": "ROSELINO SILVA",
            }

            res = self.client().post('/partners',
                                     json=new_partner,
                                     headers=self.admin_headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'unprocessable')

    def test_update_partner(self):
        with self.app.app_context():
            # get id of first partner in db
            partner_id = Partner.query \
                .with_entities(Partner.id) \
                .order_by(Partner.id) \
                .first()[0]
            res = self.client().patch(
                f'/partners/{partner_id}',
                json={'name': 'JOSELIMERSON DE SUMIDOURO'},
                headers=self.admin_headers
            )
            data = json.loads(res.data)
            partner = Partner.query \
                .filter(Partner.id == partner_id).one_or_none()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(partner.format()['name'],
                             'JOSELIMERSON DE SUMIDOURO')

    def test_error_404_update_non_existent_partner(self):
        with self.app.app_context():
            res = self.client().patch(
                '/partners/100000',
                json={'name': 'JOSELIMERSON DE SUMIDOURO'},
                headers=self.admin_headers
            )

            self.assert_error404(res)

    def test_del_partner(self):
        with self.app.app_context():
            # get id from last partner in db
            partner_id = Partner.query \
                .with_entities(Partner.id) \
                .order_by(Partner.id.desc()) \
                .first()[0]

            res = self.client().delete(f'/partners/{partner_id}',
                                       headers=self.admin_headers)

            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], partner_id)

            partner = Partner.query\
                .filter(Partner.id == data['deleted'])\
                .one_or_none()

            self.assertEqual(partner, None)

    def test_error_404_del_non_existing_partner(self):
        res = self.client().delete('/partners/100000',
                                   headers=self.admin_headers)

        self.assert_error404(res)

    # # SANCTIONS

    def test_create_sanction(self):
        with self.app.app_context():
            # get id from last company in db
            company_id = Company.query \
                .with_entities(Company.id) \
                .order_by(Company.id.desc()) \
                .first()[0]

            res = self.client().post(f'/companies/{company_id}/sanctions',
                                     json=self.new_santion,
                                     headers=self.admin_headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 201)
            self.assertTrue(data['success'])

            # assert the new sanction was created in database
            sanction_count = Sanction.query\
                .filter(Sanction.id == data['created'],
                        Sanction.company_id == company_id)\
                .count()
            self.assertEqual(sanction_count, 1)

    def test_error_404_create_sanction_for_non_existing_company(self):
        res = self.client().post('/companies/100000/sanctions',
                                 json=self.new_santion,
                                 headers=self.admin_headers)

        self.assert_error404(res)

    def test_del_sanction(self):
        with self.app.app_context():
            # get id from last sanction in db
            sanction_id = Sanction.query \
                .with_entities(Sanction.id) \
                .order_by(Sanction.id.desc()) \
                .first()[0]

            res = self.client().delete(f'/sanctions/{sanction_id}',
                                       headers=self.admin_headers)

            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], sanction_id)

            sanction = Sanction.query\
                .filter(Sanction.id == data['deleted'])\
                .one_or_none()

            self.assertEqual(sanction, None)

    def test_error_404_del_non_existing_sanction(self):
        res = self.client().delete('/sanctions/100000',
                                   headers=self.admin_headers)

        self.assert_error404(res)

    # # permission

    def test_error_401_no_authorization_header(self):
        res = self.client().delete('/companies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], '401')
        self.assertEqual(data['message'], 'Authorizarion header is necessary.')

    def test_error_403_normaluser_with_no_permission_to_del_company(self):
        res = self.client().delete('/companies/1',
                                   headers=self.normal_user_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], '403')
        self.assertEqual(data['message'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()
