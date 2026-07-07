"""
NutriCheck Backend — Entry Point Aplikasi Flask.

Sistem Monitoring dan Analisis Gizi Balita.
Menyediakan REST API untuk:
- Manajemen data balita
- Pemeriksaan gizi dengan perhitungan Z-Score otomatis
- Tips nutrisi
- Generate laporan PDF
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Muat environment variables
load_dotenv()

# Import blueprints
from routes.balita_routes import balita_bp
from routes.pemeriksaan_routes import pemeriksaan_bp
from routes.tips_routes import tips_bp
from routes.laporan_routes import laporan_bp

# Import middleware
from middleware.error_handler import register_error_handlers


def create_app():
    """Factory function untuk membuat instance Flask app."""

    app = Flask(__name__)

    # ---- Konfigurasi ----
    app.config["JSON_SORT_KEYS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Max 16MB

    # ---- CORS ----
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    # ---- Register Blueprints ----
    app.register_blueprint(balita_bp)
    app.register_blueprint(pemeriksaan_bp)
    app.register_blueprint(tips_bp)
    app.register_blueprint(laporan_bp)

    # ---- Register Error Handlers ----
    register_error_handlers(app)

    # ---- Root Endpoint ----
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "status": "success",
            "message": "🍎 NutriCheck API — Sistem Monitoring Gizi Balita",
            "version": "1.0.0",
            "endpoints": {
                "balita": "/api/balita",
                "pemeriksaan": "/api/pemeriksaan",
                "tips": "/api/tips",
                "laporan": "/api/laporan",
            },
        }), 200

    # ---- Health Check ----
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "NutriCheck API",
        }), 200

    return app


# ---- Main ----
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
    )
