import sys

from flask import (
    Blueprint,
    abort,
    jsonify,
    request
)

from .database.models import Company, Partner
from .auth.auth import requires_auth

companies_blueprint = Blueprint('companies_blueprint', __name__)


@companies_blueprint.route('/companies', methods=['GET'])
@requires_auth('get:companies')
def companies(jwt):
    """Retrieves a list of all companies from the database.

    Args:
        jwt (str): the JSON Web Token used by the user.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - companies (list): A list with all companies in the
              following format:
                - id (int)
                - fiscal_number (str)
                - name (str)
                - partners (list): list of owners of the company
                  in the following format:
                    - id (int)
                    - document (str)
                    - name (str)
                - sanctions (list): list of sanctions the company received
                    - id (int)
                    - organization (str)
    """
    try:
        companies = Company.query.all()

        companies_lst = [company.format() for company in companies]
    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'companies': companies_lst
    }), 200


@companies_blueprint.route('/companies', methods=['POST'])
@requires_auth('post:companies')
def new_company(jwt):
    """Create a new company in the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        fiscal_number (str): Fiscal number of the company.
        name (str): Name of the company.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - created (int): Id of the created company.
    """
    try:
        data = request.get_json()

        fiscal_number = data.get('fiscal_number')
        name = data.get('name')

        company = Company(fiscal_number=fiscal_number, name=name)

        company.insert()
    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'created': company.id
    }), 201


@companies_blueprint.route('/companies/<int:id>', methods=['PATCH'])
@requires_auth('patch:companies')
def update_company(jwt, id):
    """Update information about a company in the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        id (int): Id of the company to be updated.
        fiscal_number (str): Fiscal number of the company.
        name (str): Name of the company.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - updated (int): Id of the updated company.
    """
    company = Company.query.get_or_404(id)
    try:
        data = request.get_json()
        fiscal_number = data.get('fiscal_number')
        name = data.get('name')

        if fiscal_number:
            company.fiscal_number = fiscal_number
        if name:
            company.name = name

        company.update()
    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'updated': company.id
    }), 200


@companies_blueprint.route('/companies/<int:id>', methods=['DELETE'])
@requires_auth('delete:companies')
def delete_company(jwt, id):
    """Delete a company from the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        id (int): Id of the company to be deleted.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - deleted (int): Id of the deleted company.
    """
    company = Company.query.get_or_404(id)

    try:
        company.delete()

    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'deleted': id
    }), 200


@companies_blueprint.route(
    '/companies/<int:company_id>/partners/<int:partner_id>',
    methods=['PUT']
)
@requires_auth('put:partners')
def add_partner_to_company(jwt, company_id, partner_id):
    """Associate a partner with its company.

    Args:
        jwt (str): the JSON Web Token used by the user.
        company_id (int): Id of the company we want to add a partner.
        partner_id (int): Id of the partner we want to add to the company.

    Returns:
        JSON: A JSON with the following key:
            - success (bool): Indicates if the request was successful.
    """
    company = Company.query.get_or_404(company_id)
    partner = Partner.query.get_or_404(partner_id)
    try:
        company.partners.append(partner)
        company.update()
    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True
    }), 200
