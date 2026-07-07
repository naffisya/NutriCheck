"""
Routes Laporan — Definisi endpoint API untuk generate dan download laporan PDF.
"""

from flask import Blueprint
from controllers.laporan_controller import LaporanController

laporan_bp = Blueprint("laporan", __name__, url_prefix="/api/laporan")


# GET /api/laporan — Ambil semua data laporan
@laporan_bp.route("", methods=["GET"])
def get_all():
    return LaporanController.get_all()


# GET /api/laporan/<id> — Ambil data laporan berdasarkan ID
@laporan_bp.route("/<int:laporan_id>", methods=["GET"])
def get_by_id(laporan_id):
    return LaporanController.get_by_id(laporan_id)


# POST /api/laporan/generate/<pemeriksaan_id> — Generate laporan PDF
@laporan_bp.route("/generate/<int:pemeriksaan_id>", methods=["POST"])
def generate(pemeriksaan_id):
    return LaporanController.generate(pemeriksaan_id)


# GET /api/laporan/download/<nama_file> — Download file PDF
@laporan_bp.route("/download/<string:nama_file>", methods=["GET"])
def download(nama_file):
    return LaporanController.download(nama_file)


# DELETE /api/laporan/<id> — Hapus data laporan dan file PDF
@laporan_bp.route("/<int:laporan_id>", methods=["DELETE"])
def delete(laporan_id):
    return LaporanController.delete(laporan_id)
