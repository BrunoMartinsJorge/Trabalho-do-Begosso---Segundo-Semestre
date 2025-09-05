from flask import jsonify
from exceptions.ObjectExistsException import ObjectExistsException
from exceptions.ObjectNotExistsException import ObjectNotExistsException


def register_error_handlers(app):
    @app.errorhandler(ObjectExistsException)
    def handle_object_exists(error):
        return jsonify({"erro": str(error)}), 400

    @app.errorhandler(ObjectNotExistsException)
    def handle_object_not_exists(error):
        return jsonify({"erro": str(error)}), 400
