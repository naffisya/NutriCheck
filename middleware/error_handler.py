"""
Middleware error handler global untuk aplikasi Flask.
Menangani semua error dan mengembalikan response JSON yang konsisten.
"""

from flask import jsonify


def register_error_handlers(app):
    """
    Mendaftarkan error handler global ke aplikasi Flask.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": "error",
            "code": 400,
            "message": "Bad Request - Data yang dikirim tidak valid.",
            "detail": str(error)
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "Not Found - Resource tidak ditemukan.",
            "detail": str(error)
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "code": 405,
            "message": "Method Not Allowed - HTTP method tidak diizinkan.",
            "detail": str(error)
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "status": "error",
            "code": 422,
            "message": "Unprocessable Entity - Data tidak dapat diproses.",
            "detail": str(error)
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Internal Server Error - Terjadi kesalahan pada server.",
            "detail": str(error)
        }), 500

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Menangkap semua exception yang tidak tertangani."""
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Terjadi kesalahan yang tidak terduga.",
            "detail": str(error)
        }), 500
