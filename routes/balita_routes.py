"""
Routes Balita — Definisi endpoint API untuk manajemen data balita.
"""

from flask import Blueprint
from controllers.balita_controller import BalitaController

balita_bp = Blueprint("balita", __name__, url_prefix="/api/balita")


# GET /api/balita — Ambil semua data balita
@balita_bp.route("", methods=["GET"])
def get_all():
    return BalitaController.get_all()


# GET /api/balita/search?q=keyword — Cari balita berdasarkan nama
@balita_bp.route("/search", methods=["GET"])
def search():
    return BalitaController.search()


# GET /api/balita/<id> — Ambil data balita berdasarkan ID
@balita_bp.route("/<int:balita_id>", methods=["GET"])
def get_by_id(balita_id):
    return BalitaController.get_by_id(balita_id)


# POST /api/balita — Tambah data balita baru
@balita_bp.route("", methods=["POST"])
def create():
    return BalitaController.create()


# PUT /api/balita/<id> — Update data balita
@balita_bp.route("/<int:balita_id>", methods=["PUT"])
def update(balita_id):
    return BalitaController.update(balita_id)


# DELETE /api/balita/<id> — Hapus data balita (soft delete)
@balita_bp.route("/<int:balita_id>", methods=["DELETE"])
def delete(balita_id):
    return BalitaController.delete(balita_id)
