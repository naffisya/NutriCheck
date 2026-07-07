"""
Controller Pemeriksaan — Logika bisnis untuk pemeriksaan gizi balita.
Mengintegrasikan perhitungan Z-Score.
"""

from flask import jsonify, request
from models.pemeriksaan import PemeriksaanModel
from models.balita import BalitaModel
from services.zscore_service import hitung_zscore
from models.tips import TipsModel


class PemeriksaanController:

    @staticmethod
    def get_all():
        """Mengambil semua data pemeriksaan."""
        try:
            data = PemeriksaanModel.get_all()
            return jsonify({
                "status": "success",
                "message": "Data pemeriksaan berhasil diambil.",
                "data": data,
                "total": len(data),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data pemeriksaan.",
                "detail": str(e),
            }), 500

    @staticmethod
    def get_by_id(pemeriksaan_id):
        """Mengambil data pemeriksaan berdasarkan ID."""
        try:
            data = PemeriksaanModel.get_by_id(pemeriksaan_id)
            if not data:
                return jsonify({
                    "status": "error",
                    "message": f"Pemeriksaan dengan ID {pemeriksaan_id} tidak ditemukan.",
                }), 404
            return jsonify({
                "status": "success",
                "message": "Data pemeriksaan berhasil diambil.",
                "data": data,
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data pemeriksaan.",
                "detail": str(e),
            }), 500

    @staticmethod
    def get_by_balita(balita_id):
        """Mengambil riwayat pemeriksaan untuk balita tertentu."""
        try:
            data = PemeriksaanModel.get_by_balita_id(balita_id)
            return jsonify({
                "status": "success",
                "message": f"Riwayat pemeriksaan balita ID {balita_id}.",
                "data": data,
                "total": len(data),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil riwayat pemeriksaan.",
                "detail": str(e),
            }), 500

    @staticmethod
    def create():
        """
        Membuat pemeriksaan baru dan otomatis menghitung Z-Score.
        """
        try:
            body = request.get_json()

            # Validasi field wajib
            required_fields = ["balita_id", "umur_bulan", "berat_badan", "tinggi_badan"]
            for field in required_fields:
                if field not in body or body[field] is None:
                    return jsonify({
                        "status": "error",
                        "message": f"Field '{field}' wajib diisi.",
                    }), 400

            balita_id = body["balita_id"]
            umur_bulan = int(body["umur_bulan"])
            berat_badan = float(body["berat_badan"])
            tinggi_badan = float(body["tinggi_badan"])

            # Validasi range
            if umur_bulan < 0 or umur_bulan > 60:
                return jsonify({
                    "status": "error",
                    "message": "Umur harus antara 0-60 bulan.",
                }), 400

            if berat_badan <= 0 or berat_badan > 50:
                return jsonify({
                    "status": "error",
                    "message": "Berat badan tidak valid (harus > 0 dan <= 50 kg).",
                }), 400

            if tinggi_badan <= 0 or tinggi_badan > 150:
                return jsonify({
                    "status": "error",
                    "message": "Tinggi badan tidak valid (harus > 0 dan <= 150 cm).",
                }), 400

            # Ambil data balita untuk jenis kelamin
            balita = BalitaModel.get_by_id(balita_id)
            if not balita:
                return jsonify({
                    "status": "error",
                    "message": f"Balita dengan ID {balita_id} tidak ditemukan.",
                }), 404

            jenis_kelamin = balita["jenis_kelamin"]

            # Hitung Z-Score
            hasil_zscore = hitung_zscore(
                jenis_kelamin=jenis_kelamin,
                umur_bulan=umur_bulan,
                berat_badan=berat_badan,
                tinggi_badan=tinggi_badan,
            )
            # Ambil rekomendasi berdasarkan status gizi
            rekomendasi = TipsModel.get_rekomendasi(
             hasil_zscore["status_gizi"]
            )

            # Siapkan data pemeriksaan
            data_pemeriksaan = {
                "balita_id": balita_id,
                "umur_bulan": umur_bulan,
                "berat_badan": berat_badan,
                "tinggi_badan": tinggi_badan,
                "tanggal_pemeriksaan": body.get("tanggal_pemeriksaan"),
                "zscore_bb_u": hasil_zscore["zscore_bb_u"],
                "zscore_tb_u": hasil_zscore["zscore_tb_u"],
                "zscore_bb_tb": hasil_zscore["zscore_bb_tb"],
                "status_bb_u": hasil_zscore["status_bb_u"],
                "status_tb_u": hasil_zscore["status_tb_u"],
                "status_bb_tb": hasil_zscore["status_bb_tb"],
                "status_gizi": hasil_zscore["status_gizi"],
                "ringkasan_analisis": hasil_zscore["ringkasan_analisis"],
                "rekomendasi_nutrisi": rekomendasi,
            }

            result = PemeriksaanModel.create(data_pemeriksaan)

            return jsonify({
                "status": "success",
                "message": "Pemeriksaan berhasil disimpan.",
                "data": result,
                "rekomendasi": rekomendasi
            }), 201

        except ValueError as e:
            return jsonify({
                "status": "error",
                "message": "Format data tidak valid.",
                "detail": str(e),
            }), 400
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal menyimpan pemeriksaan.",
                "detail": str(e),
            }), 500

    @staticmethod
    def delete(pemeriksaan_id):
        """Menghapus data pemeriksaan."""
        try:
            result = PemeriksaanModel.delete(pemeriksaan_id)
            return jsonify({
                "status": "success",
                "message": "Data pemeriksaan berhasil dihapus.",
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal menghapus data pemeriksaan.",
                "detail": str(e),
            }), 500
