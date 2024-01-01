from flask import Blueprint
from app.response import Response

mining = Blueprint('mining', __name__)

@mining.route('/mine', methods=["GET"])
def mine():
    response_obj = Response("Test message", 450)
    return response_obj.return_error_response()