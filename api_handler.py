from flask import Blueprint


# Create API Blueprint for modularity.
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/test', methods=['GET'])
def hello_world():
    return "Hello", 200


if __name__ == '__main__':
    pass
