"""
Routes Pemeriksaan — Definisi endpoint API untuk pemeriksaan gizi balita.
"""

from flask import Blueprint
from controllers.pemeriksaan_controller import PemeriksaanController

pemeriksaan_bp = Blueprint("pemeriksaan", __name__, url_prefix="/api/pemeriksaan")


# GET /api/pemeriksaan — Ambil semua data pemeriksaan
@pemeriksaan_bp.route("", methods=["GET"])
def get_all():
    return PemeriksaanController.get_all()


# GET /api/pemeriksaan/<id> — Ambil data pemeriksaan berdasarkan ID
@pemeriksaan_bp.route("/<int:pemeriksaan_id>", methods=["GET"])
def get_by_id(pemeriksaan_id):
    return PemeriksaanController.get_by_id(pemeriksaan_id)


# GET /api/pemeriksaan/balita/<balita_id> — Riwayat pemeriksaan per balita
@pemeriksaan_bp.route("/balita/<int:balita_id>", methods=["GET"])
def get_by_balita(balita_id):
    return PemeriksaanController.get_by_balita(balita_id)


# POST /api/pemeriksaan — Buat pemeriksaan baru (otomatis hitung Z-Score)
@pemeriksaan_bp.route("", methods=["POST"])
def create():
    return PemeriksaanController.create()


# DELETE /api/pemeriksaan/<id> — Hapus data pemeriksaan
@pemeriksaan_bp.route("/<int:pemeriksaan_id>", methods=["DELETE"])
def delete(pemeriksaan_id):
    return PemeriksaanController.delete(pemeriksaan_id)
