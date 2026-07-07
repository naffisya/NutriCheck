"""
Controller Laporan — Logika bisnis untuk generate dan manajemen laporan PDF.
"""

import os
from flask import jsonify, request, send_file
from models.laporan import LaporanModel
from models.pemeriksaan import PemeriksaanModel
from models.balita import BalitaModel
from services.pdf_service import generate_laporan_pdf


class LaporanController:

    @staticmethod
    def get_all():
        """Mengambil semua data laporan."""
        try:
            data = LaporanModel.get_all()
            return jsonify({
                "status": "success",
                "message": "Data laporan berhasil diambil.",
                "data": data,
                "total": len(data),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data laporan.",
                "detail": str(e),
            }), 500

    @staticmethod
    def get_by_id(laporan_id):
        """Mengambil data laporan berdasarkan ID."""
        try:
            data = LaporanModel.get_by_id(laporan_id)
            if not data:
                return jsonify({
                    "status": "error",
                    "message": f"Laporan dengan ID {laporan_id} tidak ditemukan.",
                }), 404
            return jsonify({
                "status": "success",
                "message": "Data laporan berhasil diambil.",
                "data": data,
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengambil data laporan.",
                "detail": str(e),
            }), 500

    @staticmethod
    def generate(pemeriksaan_id):
        """
        Generate laporan PDF dari data pemeriksaan.
        """
        try:
            # Ambil data pemeriksaan
            pemeriksaan = PemeriksaanModel.get_by_id(pemeriksaan_id)
            if not pemeriksaan:
                return jsonify({
                    "status": "error",
                    "message": f"Pemeriksaan dengan ID {pemeriksaan_id} tidak ditemukan.",
                }), 404

            # Ambil data balita
            balita_id = pemeriksaan.get("balita_id")
            balita = BalitaModel.get_by_id(balita_id)
            if not balita:
                return jsonify({
                    "status": "error",
                    "message": "Data balita tidak ditemukan.",
                }), 404

            # Generate PDF
            hasil_pdf = generate_laporan_pdf(
                data_pemeriksaan=pemeriksaan,
                data_balita=balita,
            )

            # Simpan record di database
            data_laporan = {
                "pemeriksaan_id": pemeriksaan_id,
                "nama_file": hasil_pdf["nama_file"],
                "file_url": f"/api/laporan/download/{hasil_pdf['nama_file']}",
                "ukuran_file": hasil_pdf["ukuran_file"],
            }

            record = LaporanModel.create(data_laporan)

            return jsonify({
                "status": "success",
                "message": "Laporan PDF berhasil di-generate.",
                "data": record,
            }), 201

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal generate laporan PDF.",
                "detail": str(e),
            }), 500

    @staticmethod
    def download(nama_file):
        """Download file PDF laporan."""
        try:
            storage_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "storage", "laporan"
            )
            file_path = os.path.join(storage_dir, nama_file)

            if not os.path.exists(file_path):
                return jsonify({
                    "status": "error",
                    "message": "File laporan tidak ditemukan.",
                }), 404

            return send_file(
                file_path,
                as_attachment=True,
                download_name=nama_file,
                mimetype="application/pdf",
            )
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal mengunduh file laporan.",
                "detail": str(e),
            }), 500

    @staticmethod
    def delete(laporan_id):
        """Menghapus data laporan dan file PDF-nya."""
        try:
            # Ambil data laporan dulu untuk mendapatkan nama file
            laporan = LaporanModel.get_by_id(laporan_id)
            if not laporan:
                return jsonify({
                    "status": "error",
                    "message": f"Laporan dengan ID {laporan_id} tidak ditemukan.",
                }), 404

            # Hapus file fisik jika ada
            storage_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "storage", "laporan"
            )
            file_path = os.path.join(storage_dir, laporan.get("nama_file", ""))
            if os.path.exists(file_path):
                os.remove(file_path)

            # Hapus record di database
            LaporanModel.delete(laporan_id)

            return jsonify({
                "status": "success",
                "message": "Laporan berhasil dihapus.",
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Gagal menghapus laporan.",
                "detail": str(e),
            }), 500
