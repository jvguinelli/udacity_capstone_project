import os

from flask import Flask, abort, jsonify, request, render_template
from flask_cors import CORS

from .database.models import setup_db, Company, Partner, Sanction
from .auth.auth import requires_auth, AuthError


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
            os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

    setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # COMPANY #

    @app.route('/companies', methods=['GET'])
    @requires_auth('get:companies')
    def companies(jwt):
        try:
            companies = Company.query.all()

            companies_lst = [company.format() for company in companies]
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'companies': companies_lst
        }), 200

    @app.route('/companies', methods=['POST'])
    @requires_auth('post:companies')
    def new_company(jwt):
        try:
            data = request.get_json()

            fiscal_number = data.get('fiscal_number', None)
            name = data.get('name', None)

            company = Company(fiscal_number=fiscal_number, name=name)

            company.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'created': company.id
        }), 201

    @app.route('/companies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:companies')
    def update_company(jwt, id):
        company = Company.query.get_or_404(id)
        try:
            data = request.get_json()
            fiscal_number = data.get('fiscal_number', None)
            name = data.get('name', None)

            if fiscal_number:
                company.fiscal_number = fiscal_number
            if name:
                company.name = name

            company.update()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'updated': company.id
        }), 200

    @app.route('/companies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:companies')
    def delete_company(jwt, id):
        company = Company.query.get_or_404(id)

        try:
            company.delete()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': id
        }), 200

    @app.route('/companies/<int:company_id>/partners/<int:partner_id>',
               methods=['PUT'])
    @requires_auth('put:partners')
    def add_partner_to_company(jwt, company_id, partner_id):
        company = Company.query.get_or_404(company_id)
        partner = Partner.query.get_or_404(partner_id)
        try:
            company.partners.append(partner)
            company.update()
        except Exception:
            abort(422)

        return jsonify({
            'success': True
        }), 200

    # PARTNER #

    @app.route('/partners', methods=['GET'])
    @requires_auth('get:partners')
    def partners(jwt):
        try:
            partners = Partner.query.all()

            partners_lst = [partner.format() for partner in partners]
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'partners': partners_lst
        }), 200

    @app.route('/partners', methods=['POST'])
    @requires_auth('post:partners')
    def new_partner(jwt):
        try:
            data = request.get_json()

            document = data.get('document', None)
            name = data.get('name', None)

            partner = Partner(document=document, name=name)

            partner.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'created': partner.id
        }), 201

    @app.route('/partners/<int:id>', methods=['PATCH'])
    @requires_auth('patch:partners')
    def update_partner(jwt, id):
        partner = Partner.query.get_or_404(id)

        try:
            data = request.get_json()

            document = data.get('document', None)
            name = data.get('name', None)

            if document:
                partner.document = document

            if name:
                partner.name = name

            partner.update()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'updated': partner.id
        }), 200

    @app.route('/partners/<int:id>', methods=['DELETE'])
    @requires_auth('delete:partners')
    def delete_partner(jwt, id):
        partner = Partner.query.get_or_404(id)

        try:
            partner.delete()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': id
        }), 200

    # SANCTIONS #

    @app.route('/companies/<int:id>/sanctions', methods=['POST'])
    @requires_auth('post:sanctions')
    def new_sanction(jwt, id):
        Company.query.get_or_404(id)
        try:
            data = request.get_json()

            name = data.get('name', None)
            organization = data.get('organization', None)

            sanction = Sanction(name=name,
                                organization=organization,
                                company_id=id)

            sanction.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'created': sanction.id
        }), 201

    @app.route('/sanctions/<int:id>', methods=['DELETE'])
    @requires_auth('delete:sanctions')
    def delete_sanction(jwt, id):
        sanction = Sanction.query.get_or_404(id)

        try:
            sanction.delete()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': id
        }), 200

    @app.route('/show_created_token', methods=['GET'])
    def show_created_token():
        return render_template("show_created_token.html")

    # ERROR HANDLER

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": str(error.status_code),
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400,

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
