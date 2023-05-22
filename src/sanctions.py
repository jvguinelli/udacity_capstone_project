import sys

from flask import (
    Blueprint,
    abort,
    jsonify,
    request
)

from .database.models import Company, Sanction
from .auth.auth import requires_auth

sanctions_blueprint = Blueprint('sanctions_blueprint', __name__)


@sanctions_blueprint.route('/companies/<int:id>/sanctions', methods=['POST'])
@requires_auth('post:sanctions')
def new_sanction(jwt, id):
    """Create a new sanction for a company in the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        name (str): name of the sanction.
        organization (str): name of the organization that applied the sanction.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - created (int): Id of the created sanction.
    """
    Company.query.get_or_404(id)
    try:
        data = request.get_json()

        name = data.get('name')
        organization = data.get('organization')

        sanction = Sanction(name=name,
                            organization=organization,
                            company_id=id)

        sanction.insert()
    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'created': sanction.id
    }), 201


@sanctions_blueprint.route('/sanctions/<int:id>', methods=['DELETE'])
@requires_auth('delete:sanctions')
def delete_sanction(jwt, id):
    """Delete a Sanction from the database.

    Args:
        jwt (str): the JSON Web Token used by the user.
        id (int): id of the santion to be deleted.

    Returns:
        JSON: A JSON with the following keys:
            - success (bool): Indicates if the request was successful.
            - created (int): Id of the deleted sanction.
    """
    sanction = Sanction.query.get_or_404(id)

    try:
        sanction.delete()

    except Exception:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'deleted': id
    }), 200
