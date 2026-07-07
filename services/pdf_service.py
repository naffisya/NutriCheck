"""
Service PDF — Generate laporan PDF dari data pemeriksaan balita.
Menggunakan ReportLab untuk pembuatan dokumen PDF.
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


# Direktori penyimpanan file PDF
STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "laporan")

# Pastikan direktori ada
os.makedirs(STORAGE_DIR, exist_ok=True)


def generate_laporan_pdf(data_pemeriksaan, data_balita):
    """
    Generate laporan PDF dari data pemeriksaan dan data balita.

    Parameters:
        data_pemeriksaan (dict): Data hasil pemeriksaan (termasuk z-score & status)
        data_balita (dict): Data balita (nama, jenis_kelamin, tanggal_lahir, dsb)

    Returns:
        dict: { 'nama_file': str, 'file_path': str, 'ukuran_file': int }
    """
    # Buat nama file unik
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nama_balita_safe = data_balita.get("nama", "balita").replace(" ", "_").lower()
    nama_file = f"laporan_{nama_balita_safe}_{timestamp}.pdf"
    file_path = os.path.join(STORAGE_DIR, nama_file)

    # Buat dokumen PDF
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CustomTitle",
        parent=styles["Title"],
        fontSize=18,
        spaceAfter=6,
        textColor=colors.HexColor("#1a5276"),
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=12,
        textColor=colors.HexColor("#5d6d7e"),
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#1a5276"),
        borderWidth=1,
        borderColor=colors.HexColor("#2980b9"),
        borderPadding=4,
    ))
    styles.add(ParagraphStyle(
        name="BodyJustify",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        name="SmallGray",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.HexColor("#95a5a6"),
        alignment=TA_CENTER,
    ))

    # ---- Bangun konten PDF ----
    elements = []

    # Header / Judul
    elements.append(Paragraph("LAPORAN PEMERIKSAAN GIZI BALITA", styles["CustomTitle"]))
    elements.append(Paragraph("NutriCheck — Sistem Monitoring Gizi Balita", styles["Subtitle"]))
    elements.append(HRFlowable(
        width="100%", thickness=2,
        color=colors.HexColor("#2980b9"),
        spaceAfter=12
    ))

    # ---- Data Balita ----
    elements.append(Paragraph("Data Balita", styles["SectionHeader"]))

    tanggal_lahir = data_balita.get("tanggal_lahir", "-")
    data_balita_table = [
        ["Nama", ":", data_balita.get("nama", "-")],
        ["Jenis Kelamin", ":", data_balita.get("jenis_kelamin", "-")],
        ["Tanggal Lahir", ":", tanggal_lahir],
        ["Nama Orang Tua", ":", data_balita.get("nama_orang_tua", "-")],
        ["Alamat", ":", data_balita.get("alamat", "-")],
    ]

    t_balita = Table(data_balita_table, colWidths=[4.5 * cm, 0.5 * cm, 11 * cm])
    t_balita.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_balita)
    elements.append(Spacer(1, 8))

    # ---- Data Pemeriksaan ----
    elements.append(Paragraph("Data Pemeriksaan", styles["SectionHeader"]))

    data_periksa_table = [
        ["Tanggal Pemeriksaan", ":", data_pemeriksaan.get("tanggal_pemeriksaan", "-")],
        ["Umur", ":", f"{data_pemeriksaan.get('umur_bulan', '-')} bulan"],
        ["Berat Badan", ":", f"{data_pemeriksaan.get('berat_badan', '-')} kg"],
        ["Tinggi Badan", ":", f"{data_pemeriksaan.get('tinggi_badan', '-')} cm"],
    ]

    t_periksa = Table(data_periksa_table, colWidths=[4.5 * cm, 0.5 * cm, 11 * cm])
    t_periksa.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(t_periksa)
    elements.append(Spacer(1, 8))

    # ---- Hasil Z-Score ----
    elements.append(Paragraph("Hasil Perhitungan Z-Score", styles["SectionHeader"]))

    zscore_header = ["Indikator", "Z-Score", "Status"]
    zscore_rows = [
        zscore_header,
        [
            "BB/U (Berat Badan / Umur)",
            str(data_pemeriksaan.get("zscore_bb_u", "-")),
            data_pemeriksaan.get("status_bb_u", "-"),
        ],
        [
            "TB/U (Tinggi Badan / Umur)",
            str(data_pemeriksaan.get("zscore_tb_u", "-")),
            data_pemeriksaan.get("status_tb_u", "-"),
        ],
        [
            "BB/TB (Berat Badan / Tinggi Badan)",
            str(data_pemeriksaan.get("zscore_bb_tb", "-")),
            data_pemeriksaan.get("status_bb_tb", "-"),
        ],
    ]

    t_zscore = Table(zscore_rows, colWidths=[6.5 * cm, 3 * cm, 6.5 * cm])
    t_zscore.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2980b9")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGNMENT", (0, 0), (-1, 0), "CENTER"),
        # Data rows
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGNMENT", (1, 1), (1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#eaf2f8")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.HexColor("#eaf2f8"), colors.white
        ]),
        # Grid
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_zscore)
    elements.append(Spacer(1, 8))

    # ---- Status Gizi Keseluruhan ----
    elements.append(Paragraph("Status Gizi Keseluruhan", styles["SectionHeader"]))

    status_gizi = data_pemeriksaan.get("status_gizi", "-")
    status_color = _get_status_color(status_gizi)

    status_table = Table(
        [[Paragraph(
            f'<font size="14" color="{status_color}"><b>{status_gizi}</b></font>',
            styles["BodyJustify"]
        )]],
        colWidths=[16 * cm]
    )
    status_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(status_color)),
    ]))
    elements.append(status_table)
    elements.append(Spacer(1, 8))

    # ---- Ringkasan Analisis ----
    ringkasan = data_pemeriksaan.get("ringkasan_analisis", "")
    if ringkasan:
        elements.append(Paragraph("Ringkasan Analisis", styles["SectionHeader"]))
        # Ganti newline dengan <br/>
        ringkasan_html = ringkasan.replace("\n", "<br/>")
        elements.append(Paragraph(ringkasan_html, styles["BodyJustify"]))
        elements.append(Spacer(1, 8))

    # ---- Rekomendasi Nutrisi ----
    rekomendasi = data_pemeriksaan.get("rekomendasi_nutrisi", [])
    if rekomendasi:
        elements.append(Paragraph("Rekomendasi Nutrisi", styles["SectionHeader"]))

        for i, rekom in enumerate(rekomendasi, 1):
            judul = rekom.get("judul", "")
            deskripsi = rekom.get("deskripsi", "")
            prioritas = rekom.get("prioritas", "sedang")
            icon = "🔴" if prioritas == "tinggi" else "🟡"
            elements.append(Paragraph(
                f'<b>{i}. {judul}</b> <font size="8" color="gray">[{prioritas}]</font>',
                styles["BodyJustify"]
            ))
            elements.append(Paragraph(f"   {deskripsi}", styles["BodyJustify"]))
            elements.append(Spacer(1, 4))

    # ---- Footer ----
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(
        width="100%", thickness=1,
        color=colors.HexColor("#bdc3c7"),
        spaceAfter=6
    ))
    elements.append(Paragraph(
        f"Laporan ini di-generate oleh NutriCheck pada {datetime.now().strftime('%d %B %Y, %H:%M WIB')}",
        styles["SmallGray"]
    ))
    elements.append(Paragraph(
        "Dokumen ini bukan pengganti konsultasi medis profesional.",
        styles["SmallGray"]
    ))

    # Build PDF
    doc.build(elements)

    # Ukuran file
    ukuran_file = os.path.getsize(file_path)

    return {
        "nama_file": nama_file,
        "file_path": file_path,
        "ukuran_file": ukuran_file,
    }


def _get_status_color(status_gizi):
    """Mengembalikan warna hex berdasarkan status gizi."""
    status_colors = {
        "Gizi Buruk": "#e74c3c",
        "Gizi Kurang": "#e67e22",
        "Gizi Baik": "#27ae60",
        "Gizi Lebih": "#f39c12",
        "Obesitas": "#c0392b",
    }
    return status_colors.get(status_gizi, "#2c3e50")
