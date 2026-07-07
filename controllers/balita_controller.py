"""
Controller Balita — Logika bisnis untuk manajemen data balita.
"""

from flask import jsonify, request
from models.balita import BalitaModel


class BalitaController:

    @staticmethod
    def get_all():
        """Mengambil semua data balita."""
        try:
            data = BalitaModel.get_all()
            return jsonify({
                "status": "success",
                "message": "Data balita berhasil diambil.",
                "data": data,
                "total": len(data),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data balita.",
                "detail": str(e),
            }), 500

    @staticmethod
    def get_by_id(balita_id):
        """Mengambil data balita berdasarkan ID."""
        try:
            data = BalitaModel.get_by_id(balita_id)
            if not data:
                return jsonify({
                    "status": "error",
                    "message": f"Balita dengan ID {balita_id} tidak ditemukan.",
                }), 404
            return jsonify({
                "status": "success",
                "message": "Data balita berhasil diambil.",
                "data": data,
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data balita.",
                "detail": str(e),
            }), 500

    @staticmethod
    def create():
        """Membuat data balita baru."""
        try:
            body = request.get_json()

            # Validasi field wajib
            required_fields = ["nama", "jenis_kelamin"]
            for field in required_fields:
                if field not in body or not body[field]:
                    return jsonify({
                        "status": "error",
                        "message": f"Field '{field}' wajib diisi.",
                    }), 400

            # Validasi jenis kelamin
            if body["jenis_kelamin"] not in ("Laki-laki", "Perempuan"):
                return jsonify({
                    "status": "error",
                    "message": "Jenis kelamin harus 'Laki-laki' atau 'Perempuan'.",
                }), 400

            # Siapkan data
            data = {
                "nama": body["nama"],
                "jenis_kelamin": body["jenis_kelamin"],
                "tanggal_lahir": body.get("tanggal_lahir"),
                "nama_orang_tua": body.get("nama_orang_tua"),
                "alamat": body.get("alamat"),
            }

            result = BalitaModel.create(data)
            return jsonify({
                "status": "success",
                "message": "Data balita berhasil ditambahkan.",
                "data": result,
            }), 201
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal menambahkan data balita.",
                "detail": str(e),
            }), 500

    @staticmethod
    def update(balita_id):
        """Mengupdate data balita."""
        try:
            body = request.get_json()

            # Validasi jenis kelamin jika ada
            if "jenis_kelamin" in body:
                if body["jenis_kelamin"] not in ("Laki-laki", "Perempuan"):
                    return jsonify({
                        "status": "error",
                        "message": "Jenis kelamin harus 'Laki-laki' atau 'Perempuan'.",
                    }), 400

            # Filter hanya field yang diizinkan
            allowed_fields = [
                "nama", "jenis_kelamin", "tanggal_lahir",
                "nama_orang_tua", "alamat"
            ]
            data = {k: v for k, v in body.items() if k in allowed_fields}

            if not data:
                return jsonify({
                    "status": "error",
                    "message": "Tidak ada data yang diupdate.",
                }), 400

            result = BalitaModel.update(balita_id, data)
            if not result:
                return jsonify({
                    "status": "error",
                    "message": f"Balita dengan ID {balita_id} tidak ditemukan.",
                }), 404

            return jsonify({
                "status": "success",
                "message": "Data balita berhasil diupdate.",
                "data": result,
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengupdate data balita.",
                "detail": str(e),
            }), 500

    @staticmethod
    def delete(balita_id):
        """Menghapus data balita (soft delete)."""
        try:
            result = BalitaModel.delete(balita_id)
            if not result:
                return jsonify({
                    "status": "error",
                    "message": f"Balita dengan ID {balita_id} tidak ditemukan.",
                }), 404

            return jsonify({
                "status": "success",
                "message": "Data balita berhasil dihapus.",
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal menghapus data balita.",
                "detail": str(e),
            }), 500

    @staticmethod
    def search():
        """Mencari balita berdasarkan nama."""
        try:
            keyword = request.args.get("q", "")
            if not keyword:
                return jsonify({
                    "status": "error",
                    "message": "Parameter pencarian 'q' wajib diisi.",
                }), 400

            data = BalitaModel.search(keyword)
            return jsonify({
                "status": "success",
                "message": f"Hasil pencarian untuk '{keyword}'.",
                "data": data,
                "total": len(data),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal melakukan pencarian.",
                "detail": str(e),
            }), 500
