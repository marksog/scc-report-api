from flask import jsonify
from marshmallow import ValidationError

def init_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"errors": e.messages}), 422

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error":"Not Found"}), 404