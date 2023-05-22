import sys

from flask import (
    Blueprint,
    abort,
    jsonify,
    request
)

from .database.models import Partner
from .auth.auth import requires_auth

partners_blueprint = Blueprint('partners_blueprint', __name__)


@partners_blueprint.route('/partners', methods=['GET'])
@requires_auth('get:partners')
def partners(jwt):
    """Retrieves a list of all partners in the database.

    Args:
        jwt (str): the JSON Web Token used by the user.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - partners (list): A list of all company owners in the
              following format:
                - id (int)
                - document (str)
                - name (str)
                - companies (list): A list with all companies owned by the
                  partner in following format:
                        - id (int)
                        - fiscal_number (str)
                        - name (str)
                        - sanctions (list): list of sanctions the company
                          received:
                            - id (int)
                            - organization (str)
    """
    try:
        partners = Partner.query.all()

        partners_lst = [partner.format() for partner in partners]
    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'partners': partners_lst
    }), 200


@partners_blueprint.route('/partners', methods=['POST'])
@requires_auth('post:partners')
def new_partner(jwt):
    """Create a new partner in the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        document (str): a document of the partner.
        name (str): Name of the partner.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - created (int): Id of the created partner.
    """
    try:
        data = request.get_json()

        document = data.get('document')
        name = data.get('name')

        partner = Partner(document=document, name=name)

        partner.insert()
    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'created': partner.id
    }), 201


@partners_blueprint.route('/partners/<int:id>', methods=['PATCH'])
@requires_auth('patch:partners')
def update_partner(jwt, id):
    """Update information about a company in the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        id (int): Id of the partner to be updated.
        document (str): a document of the partner.
        name (str): Name of the partner.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - updated (int): Id of the updated partner.
    """
    partner = Partner.query.get_or_404(id)

    try:
        data = request.get_json()

        document = data.get('document')
        name = data.get('name')

        if document:
            partner.document = document

        if name:
            partner.name = name

        partner.update()

    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'updated': partner.id
    }), 200


@partners_blueprint.route('/partners/<int:id>', methods=['DELETE'])
@requires_auth('delete:partners')
def delete_partner(jwt, id):
    """Delete a Partner from the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        id (int): Id of the partner to be deleted.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - deleted (int): Id of the deleted partner.
    """
    partner = Partner.query.get_or_404(id)

    try:
        partner.delete()

    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'deleted': id
    }), 200
