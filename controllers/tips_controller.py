"""
Controller Tips Nutrisi — Logika bisnis untuk manajemen tips nutrisi.
"""

from flask import jsonify, request
from models.tips import TipsModel


class TipsController:

    @staticmethod
    def get_all():
        """Mengambil semua tips nutrisi."""
        try:
            data = TipsModel.get_all()
            return jsonify({
                "status": "success",
                "message": "Data tips nutrisi berhasil diambil.",
                "data": data,
                "total": len(data),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data tips nutrisi.",
                "detail": str(e),
            }), 500

    @staticmethod
    def get_by_id(tips_id):
        """Mengambil tips nutrisi berdasarkan ID."""
        try:
            data = TipsModel.get_by_id(tips_id)
            if not data:
                return jsonify({
                    "status": "error",
                    "message": f"Tips dengan ID {tips_id} tidak ditemukan.",
                }), 404
            return jsonify({
                "status": "success",
                "message": "Data tips nutrisi berhasil diambil.",
                "data": data,
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data tips nutrisi.",
                "detail": str(e),
            }), 500

    @staticmethod
    def get_by_kategori(kategori):
        """Mengambil tips nutrisi berdasarkan kategori."""
        try:
            data = TipsModel.get_by_kategori(kategori)
            return jsonify({
                "status": "success",
                "message": f"Tips nutrisi kategori '{kategori}'.",
                "data": data,
                "total": len(data),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data tips nutrisi.",
                "detail": str(e),
            }), 500

    @staticmethod
    def create():
        """Membuat tips nutrisi baru."""
        try:
            body = request.get_json()

            # Validasi field wajib
            required_fields = ["judul", "deskripsi"]
            for field in required_fields:
                if field not in body or not body[field]:
                    return jsonify({
                        "status": "error",
                        "message": f"Field '{field}' wajib diisi.",
                    }), 400

            data = {
                "judul": body["judul"],
                "deskripsi": body["deskripsi"],
                "kategori": body.get("kategori", "Umum"),
                "ikon": body.get("ikon"),
            }

            result = TipsModel.create(data)
            return jsonify({
                "status": "success",
                "message": "Tips nutrisi berhasil ditambahkan.",
                "data": result,
            }), 201
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal menambahkan tips nutrisi.",
                "detail": str(e),
            }), 500

    @staticmethod
    def update(tips_id):
        """Mengupdate tips nutrisi."""
        try:
            body = request.get_json()

            allowed_fields = ["judul", "deskripsi", "kategori", "ikon"]
            data = {k: v for k, v in body.items() if k in allowed_fields}

            if not data:
                return jsonify({
                    "status": "error",
                    "message": "Tidak ada data yang diupdate.",
                }), 400

            result = TipsModel.update(tips_id, data)
            if not result:
                return jsonify({
                    "status": "error",
                    "message": f"Tips dengan ID {tips_id} tidak ditemukan.",
                }), 404

            return jsonify({
                "status": "success",
                "message": "Tips nutrisi berhasil diupdate.",
                "data": result,
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengupdate tips nutrisi.",
                "detail": str(e),
            }), 500

    @staticmethod
    def delete(tips_id):
        """Menghapus tips nutrisi (soft delete)."""
        try:
            result = TipsModel.delete(tips_id)
            if not result:
                return jsonify({
                    "status": "error",
                    "message": f"Tips dengan ID {tips_id} tidak ditemukan.",
                }), 404

            return jsonify({
                "status": "success",
                "message": "Tips nutrisi berhasil dihapus.",
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal menghapus tips nutrisi.",
                "detail": str(e),
            }), 500
            
    @staticmethod
    def get_by_target(target):
        try:
            data = TipsModel.get_by_target(target)

            return jsonify({
                "status": "success",
                "data": data
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "detail": str(e)
        }), 500