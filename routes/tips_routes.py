"""
Routes Tips Nutrisi — Definisi endpoint API untuk manajemen tips nutrisi.
"""

from flask import Blueprint
from controllers.tips_controller import TipsController

tips_bp = Blueprint("tips", __name__, url_prefix="/api/tips")


# GET /api/tips — Ambil semua tips nutrisi
@tips_bp.route("", methods=["GET"])
def get_all():
    return TipsController.get_all()


# GET /api/tips/<id> — Ambil tips nutrisi berdasarkan ID
@tips_bp.route("/<int:tips_id>", methods=["GET"])
def get_by_id(tips_id):
    return TipsController.get_by_id(tips_id)


# GET /api/tips/kategori/<kategori> — Ambil tips berdasarkan kategori
@tips_bp.route("/kategori/<string:kategori>", methods=["GET"])
def get_by_kategori(kategori):
    return TipsController.get_by_kategori(kategori)


# POST /api/tips — Tambah tips nutrisi baru
@tips_bp.route("", methods=["POST"])
def create():
    return TipsController.create()


# PUT /api/tips/<id> — Update tips nutrisi
@tips_bp.route("/<int:tips_id>", methods=["PUT"])
def update(tips_id):
    return TipsController.update(tips_id)


# DELETE /api/tips/<id> — Hapus tips nutrisi (soft delete)
@tips_bp.route("/<int:tips_id>", methods=["DELETE"])
def delete(tips_id):
    return TipsController.delete(tips_id)

@tips_bp.route("/target/<target>", methods=["GET"])
def get_target(target):
    return TipsController.get_by_target(target)