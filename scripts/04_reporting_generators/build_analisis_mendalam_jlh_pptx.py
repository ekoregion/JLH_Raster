import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deep_analysis_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY = RGBColor(20, 42, 74)        # #142A4A Primary Dark
    C_BLUE = RGBColor(36, 82, 122)       # #24527A Secondary
    C_TEAL = RGBColor(23, 107, 135)      # #176B87 Accent Teal
    C_GOLD = RGBColor(218, 165, 32)      # #DAA520 Accent Gold
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(30, 35, 42)
    C_MUTED = RGBColor(90, 101, 119)
    C_BG_CARD = RGBColor(243, 246, 250)
    C_BORDER = RGBColor(203, 213, 225)

    # Class Badge Colors
    CLS_COLORS = {
        "Sangat Tinggi": RGBColor(21, 115, 71),   # Deep Green
        "Tinggi": RGBColor(40, 167, 69),          # Green
        "Sedang": RGBColor(217, 130, 15),         # Amber/Gold
        "Rendah": RGBColor(220, 88, 42),          # Orange-Red
        "Sangat Rendah": RGBColor(185, 28, 28)    # Crimson Red
    }

    def add_header(slide, title_text, subtitle_text="ANALISIS FAKTOR KBA, KVA & PENUTUPAN LAHAN SERTA KOMPARASI GDB VS RASTER 0.5M"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.08))
        banner.fill.solid()
        banner.fill.fore_color.rgb = C_NAVY
        banner.line.color.rgb = C_NAVY

        tx_sub = slide.shapes.add_textbox(Inches(0.6), Inches(0.08), Inches(12.1), Inches(0.28))
        tf_s = tx_sub.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle_text.upper()
        p_s.font.size = Pt(9)
        p_s.font.bold = True
        p_s.font.color.rgb = C_GOLD

        tx_t = slide.shapes.add_textbox(Inches(0.6), Inches(0.36), Inches(12.1), Inches(0.6))
        tf_t = tx_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(18.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.08), Inches(13.333), Inches(0.05))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_GOLD
        bar.line.color.rgb = C_GOLD

    def add_styled_table(slide, headers, rows_data, col_widths, left=Inches(0.5), top=Inches(1.25), height=Inches(5.8), font_size=8.8):
        n_rows = len(rows_data) + 1
        n_cols = len(headers)
        total_w = sum(col_widths)
        tbl_shape = slide.shapes.add_table(n_rows, n_cols, left, top, total_w, height)
        tbl = tbl_shape.table

        for i, w in enumerate(col_widths):
            tbl.columns[i].width = w

        # Header formatting
        for c_idx, h_text in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.text = h_text
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(font_size + 0.7)
            p.font.bold = True
            p.font.color.rgb = C_WHITE

        # Rows formatting
        for r_idx, r_vals in enumerate(rows_data, start=1):
            bg_col = RGBColor(248, 250, 252) if r_idx % 2 == 1 else C_WHITE
            for c_idx, val in enumerate(r_vals):
                cell = tbl.cell(r_idx, c_idx)
                cell.text = str(val)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg_col
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = cell.text_frame.paragraphs[0]
                p.font.size = Pt(font_size)
                p.font.color.rgb = C_DARK

                # Colorize first column if it matches a class name
                val_str = str(val).strip()
                if c_idx == 0 and val_str in CLS_COLORS:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = CLS_COLORS[val_str]
                    p.font.bold = True
                    p.font.color.rgb = C_WHITE
                    p.alignment = PP_ALIGN.CENTER
                elif c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = C_NAVY
                    p.alignment = PP_ALIGN.LEFT
                elif c_idx == 1 and len(val_str) <= 14:
                    p.alignment = PP_ALIGN.CENTER
                    p.font.bold = True
                else:
                    p.alignment = PP_ALIGN.LEFT

        return tbl_shape

    def add_card(slide, title, items, left, top, width, height, header_color=C_TEAL):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_BG_CARD
        card.line.color.rgb = C_BORDER

        hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.48))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = header_color
        hdr.line.color.rgb = header_color
        tf_h = hdr.text_frame
        p_h = tf_h.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(10.5)
        p_h.font.bold = True
        p_h.font.color.rgb = C_WHITE
        p_h.alignment = PP_ALIGN.CENTER

        tx = slide.shapes.add_textbox(left + Inches(0.12), top + Inches(0.55), width - Inches(0.24), height - Inches(0.62))
        tf = tx.text_frame
        tf.word_wrap = True
        for idx, (b_head, b_body) in enumerate(items):
            p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
            p.space_after = Pt(5)
            p.line_spacing = 1.12
            r1 = p.add_run()
            r1.text = f"▪ {b_head}: "
            r1.font.bold = True
            r1.font.size = Pt(9.2)
            r1.font.color.rgb = C_NAVY
            r2 = p.add_run()
            r2.text = b_body
            r2.font.size = Pt(9.0)
            r2.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.color.rgb = C_NAVY

    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(0.95), Inches(0.14), Inches(5.6))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_GOLD
    accent.line.color.rgb = C_GOLD

    tx1 = s1.shapes.add_textbox(Inches(1.15), Inches(1.05), Inches(11.3), Inches(5.4))
    tf1 = tx1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "KEMENTERIAN LINGKUNGAN HIDUP / BADAN PENGENDALIAN LINGKUNGAN HIDUP (BPLH)\nDIREKTORAT PENYELENGGARAAN SUMBER DAYA ALAM BERKELANJUTAN"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p.space_after = Pt(18)

    p = tf1.add_paragraph()
    p.text = "ANALISIS KAUSALITAS JASA LINGKUNGAN HIDUP (JLH)\nBERDASARKAN PARAMETER KBA, KVA & PENUTUPAN LAHAN\nSERTA KOMPARASI GDB VS RASTER 0.5 METER"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = (
        "1. Mengapa suatu wilayah di Sumatera Barat memiliki kelas Sangat Tinggi hingga Sangat Rendah pada tiap jenis JLH?\n"
        "2. Mengapa terdapat perbedaan Nilai Skor dan Luasan (Ha) antara JLH_2025_ALL.gdb dengan Raster Seamless 0.5 Meter?"
    )
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = RGBColor(210, 224, 240)
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "Provinsi Sumatera Barat • Analisis Empiris 37.001 Poligon GDB & 175,2 Miliar Piksel Raster 0.5m • 2025–2026"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_GOLD

    # =========================================================================
    # SLIDE 2: MEKANISME 3 PARAMETER PEMBENTUK KELAS JLH (KBA, KVA, PL)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Mekanisme Pembentukan Kelas JLH dari Parameter KBA, KVA, dan PL")

    add_card(s2, "1. KARAKTERISTIK BENTANG ALAM (KBA - Bobot 15% s.d. 32%)", [
        ("Peran Fisik Abiotik", "Mencerminkan geomorfologi, lereng, dan batuan induk (litologi) yang mengontrol proses hidro-orologis dan kesuburan tanah."),
        ("KBA Bernilai Tinggi (Skor 4–5)", "Dataran/Lembah Aluvial & Dataran Vulkanik Piroklastik (skor 4–5 pada PYA & PGN karena akuifer dangkal & tanah andosol subur); Karst & Pegunungan Vulkanik (skor 4–5 pada PGA karena permeabilitas resapan air tinggi); Dataran Gambut (skor 5 pada PPK & PKU)."),
        ("KBA Bernilai Rendah (Skor 1–2)", "Perbukitan Struktural Plutonik Batuan Beku Dalam / Metamorfik (skor 1–2 pada PYA, PHK, PGN karena batuan masif kedap air dan solum tanah tipis/miskin hara); Dataran Fluvial (skor 1 pada PGA karena zona limpasan/banjir).")
    ], Inches(0.5), Inches(1.25), Inches(4.0), Inches(4.3), C_NAVY)

    add_card(s2, "2. KARAKTERISTIK VEGETASI ALAMI (KVA - Bobot 8% s.d. 25%)", [
        ("Peran Bioregion Klimaks", "Merepresentasikan potensi ekosistem vegetasi asli sebelum intervensi manusia sebagai penopang relung habitat & stok biomassa."),
        ("KVA Bernilai Tinggi (Skor 4–5)", "Vegetasi Hutan Dipterokarpa Pamah & Non-Dipterokarpa Pamah (mencakup 2,86 juta Ha / 68% Sumbar) memiliki skor 4–5 di hampir semua JLH karena struktur kanopi berlapis, perakaran dalam, dan keanekaragaman spesies tertinggi."),
        ("KVA Bernilai Rendah (Skor 1–2)", "Vegetasi Hutan Pegunungan Atas/Subalpin & Batuan Ultrabasa/Kerangas (skor 1–2 pada PHK, PGN, PGA karena faktor pembatas suhu dingin ekstrem, tanah asam miskin hara, dan tajuk kerdil).")
    ], Inches(4.66), Inches(1.25), Inches(4.0), Inches(4.3), C_TEAL)

    add_card(s2, "3. PENUTUPAN LAHAN AKTUAL 2025 (PL - Bobot Dominan 60%)", [
        ("Faktor Penentu Utama (60%)", "Karena bobotnya 0.60, perubahan tutupan lahan mampu mengangkat atau menjatuhkan kelas JLH secara drastis."),
        ("PL Pengangkat Kelas (Skor 4–5)", "Hutan Lahan Kering Primer/Sekunder & Mangrove (skor 4–5 pada PGA, PHK, PPK, PKU); Sawah & Rawa (skor 5 pada PGN); Tubuh Air/Danau (skor 5 pada PYA & PGA)."),
        ("PL Penjatuh Kelas (Skor 1–2)", "Lahan Terbuka, Pertambangan, Permukiman, Jalan, Bandara (skor 1–2 di seluruh JLH). Bahkan jika KBA & KVA bernilai 5, jika PL = 1 (Lahan Terbuka), skor maksimal hanya (5×0.40)+(1×0.60) = 2.60 (Kelas Rendah)!")
    ], Inches(8.83), Inches(1.25), Inches(4.0), Inches(4.3), C_BLUE)

    # Formula Banner at bottom
    f_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.7), Inches(12.33), Inches(1.45))
    f_box.fill.solid()
    f_box.fill.fore_color.rgb = RGBColor(254, 249, 231)
    f_box.line.color.rgb = C_GOLD
    tf_f = f_box.text_frame
    tf_f.word_wrap = True
    p_f1 = tf_f.paragraphs[0]
    p_f1.text = "KUNCI MATEMATIS MENGAPA SUATU TEMPAT BERKELAS SANGAT TINGGI (4.21–5.00) VS SANGAT RENDAH (1.00–1.80):"
    p_f1.font.size = Pt(10)
    p_f1.font.bold = True
    p_f1.font.color.rgb = C_NAVY
    p_f2 = tf_f.add_paragraph()
    p_f2.text = (
        "• Rumus Umum: Skor JLH = (W_KBA × Skor KBA) + (W_KVA × Skor KVA) + (0.60 × Skor PL).\n"
        "• Syarat Mutlak Kelas SANGAT TINGGI (> 4.20): Wajib memiliki Skor PL ≥ 4 (Hutan/Sawah/Air) DITAMBAH dukungan KBA/KVA bernilai ≥ 3. (Jika PL = 3, skor maksimum teoritis hanya 5×0.40 + 3×0.60 = 3.80 → mentok di Kelas Tinggi!).\n"
        "• Syarat Terjadinya Kelas SANGAT RENDAH (≤ 1.80): Terjadi ketika Skor PL = 1 atau 2 (Permukiman, Lahan Terbuka, Tambang, atau Hutan Sekunder pada PYA) yang berhimpitan dengan KBA batuan kedap air/miskin hara (Skor KBA = 1–2)."
    )
    p_f2.font.size = Pt(9.2)
    p_f2.font.color.rgb = C_DARK

    # Helper for 6 Indicator Anatomy Slides
    anat_headers = [
        "Kelas & Rentang",
        "Contoh Skor & Sebaran Utama",
        "Parameter KBA (Bentang Alam)",
        "Parameter KVA (Vegetasi Alami)",
        "Parameter PL (Penutupan Lahan)",
        "Sintesis Kausalitas Ekologis & Geospasial"
    ]
    anat_widths = [Inches(1.35), Inches(1.55), Inches(2.35), Inches(2.05), Inches(1.85), Inches(3.18)]

    # =========================================================================
    # SLIDE 3: ANATOMI PGA (PENGATURAN AIR)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "1. Analisis KBA, KVA & PL pada JLH Pengaturan Air (PGA)")
    pga_rows = [
        [
            "Sangat Tinggi",
            "Skor: 4.44\n(Mentawai, Pesisir Selatan, Pasaman)\n1,43–2,11 Juta Ha",
            "[Skor KBA = 3–5]\nPerbukitan struktural sedimen, pegunungan vulkanik piroklastik & karst",
            "[Skor KVA = 5]\nVegetasi hutan dipterokarpa & non-dipterokarpa pamah",
            "[Skor PL = 5]\nHutan Lahan Kering Primer & Sekunder / Badan Air",
            "Perhitungan: 3(0.28)+5(0.12)+5(0.60) = 4.44. Tajuk hutan berlapis menahan intersepsi hujan & serasah tebal memaksimalkan infiltrasi ke batuan berpori."
        ],
        [
            "Tinggi",
            "Skor: 3.52\n(Pesisir Selatan, Pasaman, Agam)\n716–733 Ribu Ha",
            "[Skor KBA = 4]\nPerbukitan/pegunungan vulkanik campuran beku luar & piroklastik",
            "[Skor KVA = 5]\nVegetasi hutan pamah tropika basah",
            "[Skor PL = 3]\nPertanian Lahan Kering Campur (Agroforestri)",
            "Perhitungan: 4(0.28)+5(0.12)+3(0.60) = 3.52. Meskipun tutupan lahan berupa kebun campur (PL=3), porositas batuan piroklastik (KBA=4) menjaga daya atur air tetap Tinggi."
        ],
        [
            "Sedang",
            "Skor: 2.96\n(Dharmasraya, Pasaman Barat)\n1,15–1,75 Juta Ha",
            "[Skor KBA = 2–3]\nDataran vulkanik berombak & perbukitan struktural lipatan",
            "[Skor KVA = 4–5]\nVegetasi hutan pamah / pegunungan bawah",
            "[Skor PL = 3]\nPerkebunan (Sawit/Karet), Sawah & Semak Belukar",
            "Perhitungan: 2(0.28)+5(0.12)+3(0.60) = 2.96. Monokultur perkebunan & sawah memiliki kapasitas retensi air moderat dengan limpasan permukaan menengah."
        ],
        [
            "Rendah",
            "Skor: 2.44\n(Pasaman Barat, Agam, Dharmasraya)\n309–357 Ribu Ha",
            "[Skor KBA = 1]\nDataran fluvial bermaterial aluvium (zona akumulasi banjir)",
            "[Skor KVA = 3]\nVegetasi terna rawa air tawar / tepian sungai",
            "[Skor PL = 3]\nPerkebunan / Pertanian Lahan Kering di dataran rendah",
            "Perhitungan: 1(0.28)+3(0.12)+3(0.60) = 2.44. Dataran aluvial datar berdrainase terhambat (KBA=1) dengan tutupan kebun tidak mampu meredam fluktuasi debit."
        ],
        [
            "Sangat Rendah",
            "Skor: 1.48–1.64\n(Pesisir Selatan, Kota Padang, Pasaman)\n9–29 Ribu Ha",
            "[Skor KBA = 1–2]\nDataran aluvial pantai / dataran gambut terdegradasi",
            "[Skor KVA = 3–4]\nVegetasi pantai / hutan gambut",
            "[Skor PL = 1–2]\nLahan Terbuka, Pertambangan, Jalan & Permukiman Padat",
            "Perhitungan: 2(0.28)+4(0.12)+1(0.60) = 1.64. Permukaan kedap air (beton/aspal) atau tanah kupasan tambang menghilangkan fungsi infiltrasi (100% menjadi run-off)."
        ]
    ]
    add_styled_table(s3, anat_headers, pga_rows, anat_widths, font_size=8.5)

    # =========================================================================
    # SLIDE 4: ANATOMI PYA (PENYEDIA AIR BERSIH)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "2. Analisis KBA, KVA & PL pada JLH Penyedia Air Bersih (PYA)")
    pya_rows = [
        [
            "Sangat Tinggi",
            "Skor: 4.84\n(Agam, Tanah Datar, Solok)\n35–42 Ribu Ha",
            "[Skor KBA = 5]\nDanau kaldera/tektonik & Lembah sungai aluvium utama",
            "[Skor KVA = 3–4]\nVegetasi hutan danau & tepian sungai air tawar",
            "[Skor PL = 5]\nTubuh Air (Danau Maninjau, Singkarak, Diatas, Dibawah, Sungai)",
            "Perhitungan: 5(0.32)+3(0.08)+5(0.60) = 4.84. Bobot KBA tertinggi (32%) berpadu dengan tubuh air tawar permanen (PL=5) sebagai cadangan air baku utama."
        ],
        [
            "Tinggi",
            "Skor: 3.64\n(Lima Puluh Kota, Pasaman Barat)\n18–240 Ribu Ha",
            "[Skor KBA = 4–5]\nLembah sungai aluvium & dataran vulkanik piroklastik (akuifer produktif)",
            "[Skor KVA = 3–4]\nVegetasi terna rawa air tawar & hutan pamah",
            "[Skor PL = 3]\nSawah Irigasi & Hutan Lahan Kering Primer di cekungan vulkanik",
            "Perhitungan: 5(0.32)+3(0.08)+3(0.60) = 3.64. Lembah aluvial dan kipas piroklastik menyimpan air tanah dangkal melimpah dengan mata air berdebit besar."
        ],
        [
            "Sedang",
            "Skor: 3.08\n(Pesisir Selatan, Pasaman Barat, Agam)\n1,75–3,11 Juta Ha",
            "[Skor KBA = 3]\nPegunungan vulkanik campuran & perbukitan sedimen",
            "[Skor KVA = 4]\nVegetasi hutan pamah dipterokarpa / non-dipterokarpa",
            "[Skor PL = 3]\nHutan Lahan Kering Primer (di GDB) & Hutan Alami (di Raster 0.5m)",
            "Perhitungan: 3(0.32)+4(0.08)+3(0.60) = 3.08. Hutan di lereng pegunungan menjaga aliran dasar sungai (baseflow), namun potensi akuifer lokalnya sedang."
        ],
        [
            "Rendah",
            "Skor: 2.48\n(Mentawai, Pesisir Selatan, Sijunjung)\n0,89–2,36 Juta Ha",
            "[Skor KBA = 2–3]\nPerbukitan struktural lipatan sedimen & batuan beku luar",
            "[Skor KVA = 4]\nVegetasi hutan dipterokarpa pamah",
            "[Skor PL = 2]\nHutan Sekunder (di GDB PL=2), Perkebunan & Kebun Campur",
            "Perhitungan: 3(0.32)+4(0.08)+2(0.60) = 2.48. Evapotranspirasi tajuk sekunder/perkebunan tinggi sementara batuan sedimen lipatan miskin akuifer air tanah."
        ],
        [
            "Sangat Rendah",
            "Skor: 1.76\n(Solok, Agam, Sijunjung)\n46–93 Ribu Ha",
            "[Skor KBA = 1]\nPerbukitan struktural plutonik batuan beku dalam (granit masif kedap air)",
            "[Skor KVA = 2–3]\nVegetasi hutan pegunungan bawah / savana",
            "[Skor PL = 1–2]\nLahan Terbuka, Tambang, Jalan, atau Hutan Sekunder di batuan plutonik",
            "Perhitungan: 1(0.32)+3(0.08)+2(0.60) = 1.76. Batuan plutonik/metamorfik masif tidak memiliki pori akuifer (air hujan langsung terbuang sebagai aliran permukaan)."
        ]
    ]
    add_styled_table(s4, anat_headers, pya_rows, anat_widths, font_size=8.5)

    # =========================================================================
    # SLIDE 5: ANATOMI PGN (PENYEDIA PANGAN)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "3. Analisis KBA, KVA & PL pada JLH Penyedia Pangan (PGN)")
    pgn_rows = [
        [
            "Sangat Tinggi",
            "Skor: 5.00\n(Agam, Pasaman, Pesisir Selatan)\n171–231 Ribu Ha",
            "[Skor KBA = 5]\nDataran fluvial aluvium & Dataran vulkanik piroklastik subur",
            "[Skor KVA = 5]\nVegetasi hutan pamah tropika",
            "[Skor PL = 5]\nSawah Irigasi Teknis, Tambak & Ekosistem Mangrove/Rawa",
            "Perhitungan: 5(0.28)+5(0.12)+5(0.60) = 5.00. Kombinasi sempurna tanah aluvial/andosol kaya mineral (KBA=5) dengan lahan sawah produktif (PL=5)."
        ],
        [
            "Tinggi",
            "Skor: 3.84–4.12\n(Pesisir Selatan, Pasaman Barat, Solok)\n1,64–3,19 Juta Ha",
            "[Skor KBA = 3–4]\nPegunungan/perbukitan vulkanik piroklastik & sedimen",
            "[Skor KVA = 4–5]\nVegetasi hutan pamah & pegunungan bawah",
            "[Skor PL = 4]\nHutan Primer & Sawah/Tanaman Pangan (di Raster PL=4)",
            "Perhitungan: 4(0.28)+5(0.12)+4(0.60) = 4.12. Tanah vulkanik lereng gunung api (Marapi, Singgalang, Talang, Pasaman) sangat subur untuk hortikultura & pangan."
        ],
        [
            "Sedang",
            "Skor: 3.24\n(Mentawai, Lima Puluh Kota, Pasaman)\n0,67–2,20 Juta Ha",
            "[Skor KBA = 3]\nPerbukitan struktural lipatan batuan sedimen non-karbonat",
            "[Skor KVA = 5]\nVegetasi hutan dipterokarpa pamah",
            "[Skor PL = 3]\nPertanian Lahan Kering, Kebun Campur, Perkebunan & Hutan Sekunder (GDB)",
            "Perhitungan: 3(0.28)+5(0.12)+3(0.60) = 3.24. Kemiringan lereng perbukitan struktural membatasi mekanisasi pertanian namun mendukung agroforestri pangan."
        ],
        [
            "Rendah",
            "Skor: 2.40–2.60\n(Pasaman Barat, Dharmasraya, Sijunjung)\n113–307 Ribu Ha",
            "[Skor KBA = 2]\nPerbukitan struktural batuan metamorfik & dataran gambut asam",
            "[Skor KVA = 2–3]\nVegetasi hutan batuan ultrabasa / kerangas / gambut",
            "[Skor PL = 2–3]\nPadang Rumput/Semak Belukar atau Perkebunan di tanah miskin hara",
            "Perhitungan: 2(0.28)+2(0.12)+3(0.60) = 2.60. Tanah ultrabasa/metamorfik dan gambut memiliki keasaman (pH) tinggi dan toksisitas logam yang menghambat tanaman pangan."
        ],
        [
            "Sangat Rendah",
            "Skor: 1.52–1.80\n(Kota Padang, Bukittinggi, Sijunjung)\n26–38 Ribu Ha",
            "[Skor KBA = 2–3]\nDataran marin berpasir & perbukitan plutonik batuan beku dalam",
            "[Skor KVA = 3]\nVegetasi hutan pantai / pegunungan",
            "[Skor PL = 1]\nPermukiman Perkotaan, Bangunan Gedung, Jalan & Lahan Terbuka",
            "Perhitungan: 3(0.28)+3(0.12)+1(0.60) = 1.80. Konversi lahan permanen menjadi kawasan terbangun menghilangkan kapasitas produksi biomassa pangan secara mutlak."
        ]
    ]
    add_styled_table(s5, anat_headers, pgn_rows, anat_widths, font_size=8.5)

    # =========================================================================
    # SLIDE 6: ANATOMI PKU (PENGATUR KUALITAS UDARA)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "4. Analisis KBA, KVA & PL pada JLH Pengatur Kualitas Udara (PKU)")
    pku_rows = [
        [
            "Sangat Tinggi",
            "Skor: 4.85\n(Mentawai, Pesisir Selatan, Pasaman)\n1,94–2,87 Juta Ha",
            "[Skor KBA = 4–5]\nPerbukitan sedimen, vulkanik & dataran gambut",
            "[Skor KVA = 5]\nVegetasi hutan dipterokarpa pamah & hutan gambut (Bobot KVA 25%!)",
            "[Skor PL = 5]\nHutan Lahan Kering Primer/Sekunder, Mangrove & Rawa",
            "Perhitungan: 4(0.15)+5(0.25)+5(0.60) = 4.85. Bobot KVA terbesar (25%) berpadu dengan kanopi hutan rapat (PL=5) yang menyerap polutan & memproduksi O2 maksimal."
        ],
        [
            "Tinggi",
            "Skor: 3.80–4.05\n(Pesisir Selatan, Lima Puluh Kota)\n622–938 Ribu Ha",
            "[Skor KBA = 4–5]\nDataran organik gambut & perbukitan vulkanik piroklastik",
            "[Skor KVA = 4–5]\nVegetasi hutan gambut & hutan pamah",
            "[Skor PL = 3–4]\nPerkebunan (di Raster PL=4; di GDB PL=3 pada KBA/KVA=5) & Hutan Tanaman",
            "Perhitungan: 5(0.15)+5(0.25)+3(0.60) = 3.80. Tegakan pohon perkebunan dan agroforestri tetap menyediakan indeks luas daun (LAI) tinggi untuk filtrasi udara."
        ],
        [
            "Sedang",
            "Skor: 3.25–3.40\n(Dharmasraya, Pasaman Barat)\n0,52–1,63 Juta Ha",
            "[Skor KBA = 3–4]\nDataran vulkanik berombak & perbukitan struktural metamorfik",
            "[Skor KVA = 4]\nVegetasi hutan pamah non-dipterokarpa",
            "[Skor PL = 3]\nSawah, Pertanian Lahan Kering, Semak Belukar & Perkebunan (di GDB)",
            "Perhitungan: 4(0.15)+4(0.25)+3(0.60) = 3.40. Vegetasi tanaman semusim (padi/palawija) dan semak memiliki tinggi tajuk rendah sehingga kapasitas serapan aerosol sedang."
        ],
        [
            "Rendah",
            "Skor: 2.35–2.60\n(Kota Padang, Pesisir Selatan, Pasaman)\n23–44 Ribu Ha",
            "[Skor KBA = 3–5]\nDataran aluvial pantai, dataran vulkanik & gambut",
            "[Skor KVA = 4–5]\nVegetasi hutan pantai / pamah / gambut",
            "[Skor PL = 1–2]\nPermukiman (PL=2) & Lahan Terbuka di atas KBA/KVA bernilai 5",
            "Perhitungan: 5(0.15)+5(0.25)+1(0.60) = 2.60. Di GDB, karena KBA minimum bernilai 2 dan KVA minimum bernilai 3, nilai terendah PKU tertahan di ~2.20–2.60 (Kelas Rendah)."
        ],
        [
            "Sangat Rendah",
            "Skor: 1.55–1.75\n(Koridor Jalan & Gedung di Raster 0.5m)\n6.840 Ha (Raster)",
            "[Skor KBA = 2–3]\nPerbukitan struktural / dataran aluvial perkotaan",
            "[Skor KVA = 2–3]\nVegetasi savana / terna tepian sungai",
            "[Skor PL = 1]\nJaringan Jalan Aspal (Kode 14), Bangunan Gedung (Kode 15) & Tanah Terbuka",
            "Perhitungan: 2(0.15)+3(0.25)+1(0.60) = 1.65. Muncul pada Raster 0.5m karena bangunan dan jalan raya bebas vegetasi terdeteksi murni sebagai piksel PL=1."
        ]
    ]
    add_styled_table(s6, anat_headers, pku_rows, anat_widths, font_size=8.5)

    # =========================================================================
    # SLIDE 7: ANATOMI PHK (HABITAT & KEHATI)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "5. Analisis KBA, KVA & PL pada JLH Pendukung Habitat & Kehati (PHK)")
    phk_rows = [
        [
            "Sangat Tinggi",
            "Skor: 4.28–5.00\n(Pesisir Selatan, Pasaman, Mentawai)\n1,36–1,58 Juta Ha",
            "[Skor KBA = 2–5]\nPegunungan vulkanik, dataran aluvial & Zona Inti Konservasi (KK1)",
            "[Skor KVA = 5]\nVegetasi hutan dipterokarpa & non-dipterokarpa pamah",
            "[Skor PL = 5]\nHutan Lahan Kering Primer (di GDB) & Hutan Alami (di Raster) + Override KK1=5.0",
            "Perhitungan Alami: 2(0.24)+5(0.16)+5(0.60) = 4.28. Hutan klimaks utuh dan kawasan TN Kerinci Seblat / Siberut menjadi habitat inti Harimau Sumatera & primata endemik."
        ],
        [
            "Tinggi",
            "Skor: 3.68–4.00\n(Mentawai, Pesisir Selatan, Pasaman)\n0,34–1,40 Juta Ha",
            "[Skor KBA = 2–3]\nPerbukitan struktural lipatan batuan sedimen & vulkanik",
            "[Skor KVA = 5]\nVegetasi hutan dipterokarpa pamah",
            "[Skor PL = 4]\nHutan Lahan Kering Sekunder & Mangrove Primer (di GDB PL=4) + Override KK2/3=4.0",
            "Perhitungan: 2(0.24)+5(0.16)+4(0.60) = 3.68. Hutan sekunder masih mempertahankan konektivitas kanopi sebagai koridor jelajah satwa liar."
        ],
        [
            "Sedang",
            "Skor: 2.96\n(Dharmasraya, Pasaman Barat)\n0,70–1,07 Juta Ha",
            "[Skor KBA = 3–4]\nDataran vulkanik berombak piroklastik & dataran gambut",
            "[Skor KVA = 4–5]\nVegetasi hutan pamah & hutan gambut",
            "[Skor PL = 2–3]\nSemak Belukar, Hutan Rawa Sekunder (PL=3) & Perkebunan pada KBA=4 (PL=2)",
            "Perhitungan: 4(0.24)+5(0.16)+2(0.60) = 2.96. Lanskap mosaik kebun dan belukar hanya mampu mendukung spesies adaptif/generalis (burung kecil, reptil, mamalia kecil)."
        ],
        [
            "Rendah",
            "Skor: 2.24\n(Sijunjung, Dharmasraya, 50 Kota)\n0,77–1,41 Juta Ha",
            "[Skor KBA = 1–2]\nPerbukitan struktural metamorfik & plutonik batuan beku dalam",
            "[Skor KVA = 4–5]\nVegetasi hutan pamah",
            "[Skor PL = 2]\nPerkebunan Monokultur, Pertanian Lahan Kering & Kebun Campur",
            "Perhitungan: 1(0.24)+5(0.16)+2(0.60) = 2.24. Konversi hutan menjadi monokultur di atas bentang alam metamorfik memutus rantai makanan dan relung mikro-habitat."
        ],
        [
            "Sangat Rendah",
            "Skor: 1.48–1.68\n(Agam, Tanah Datar, Kota Padang)\n87–184 Ribu Ha",
            "[Skor KBA = 1–2]\nTubuh Danau, Perbukitan plutonik & lahan terbangun",
            "[Skor KVA = 3–4]\nVegetasi danau / pegunungan bawah",
            "[Skor PL = 1]\nSawah Monokultur (PL_PHK=1), Permukiman, Lahan Terbuka & Tubuh Air (PL_PHK=1)",
            "Perhitungan: 1(0.24)+4(0.16)+1(0.60) = 1.48. Pada indeks habitat darat (terestrial), tubuh air terbuka, sawah intensif, dan permukiman memiliki skor PL=1."
        ]
    ]
    add_styled_table(s7, anat_headers, phk_rows, anat_widths, font_size=8.5)

    # =========================================================================
    # SLIDE 8: ANATOMI PPK (PENYERAP & SIMPAN KARBON)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "6. Analisis KBA, KVA & PL pada JLH Penyerap & Penyimpan Karbon (PPK)")
    ppk_rows = [
        [
            "Sangat Tinggi",
            "Skor: 4.40–5.00\n(Mentawai, Pesisir Selatan, Pasaman)\n1,21–2,51 Juta Ha",
            "[Skor KBA = 2–5]\nDataran organik gambut (KBA=5) & perbukitan sedimen/vulkanik (KBA=2)",
            "[Skor KVA = 5]\nVegetasi hutan dipterokarpa & non-dipterokarpa pamah (Bobot 20%)",
            "[Skor PL = 5]\nHutan Lahan Kering Primer dan Hutan Lahan Kering Sekunder",
            "Perhitungan: 2(0.20)+5(0.20)+5(0.60) = 4.40 (di Gambut mencapai 5.00!). Tegakan pohon Dipterocarpaceae berdiameter besar & tanah gambut menyimpan ratusan ton C/Ha."
        ],
        [
            "Tinggi",
            "Skor: 3.60–4.20\n(Pesisir Selatan, Solok, Pasaman)\n170–641 Ribu Ha",
            "[Skor KBA = 2–5]\nPegunungan vulkanik Bukit Barisan (KBA=2) & rawa gambut (KBA=5)",
            "[Skor KVA = 4]\nVegetasi hutan pegunungan bawah & hutan gambut",
            "[Skor PL = 3–5]\nHutan Primer di Pegunungan Bawah (Skor 4.20) & Hutan Rawa/Mangrove (PL=3–4)",
            "Perhitungan: 2(0.20)+4(0.20)+5(0.60) = 4.20. Hutan montane di lereng atas Gunung Kerinci, Singgalang & Talang memiliki pertumbuhan biomassa lebih lambat dari hutan pamah."
        ],
        [
            "Sedang",
            "Skor: 2.80–3.00\n(Pesisir Selatan, Mentawai, Pasbar)\n102–930 Ribu Ha",
            "[Skor KBA = 5]\nDataran organik bermaterial gambut (cadangan karbon bawah tanah tinggi)",
            "[Skor KVA = 4]\nVegetasi hutan gambut / rawa air tawar",
            "[Skor PL = 2]\nPerkebunan, Pertanian Lahan Kering & Semak Belukar di atas lahan gambut",
            "Perhitungan: 5(0.20)+4(0.20)+2(0.60) = 3.00. Walaupun tutupan atas berupa perkebunan/semak (PL=2), kandungan karbon tanah gambut (KBA=5) menahan skor di kelas Sedang."
        ],
        [
            "Rendah",
            "Skor: 2.20–2.60\n(Pasaman Barat, Dharmasraya)\n0,64–2,12 Juta Ha",
            "[Skor KBA = 2]\nDataran vulkanik piroklastik & perbukitan struktural mineral non-gambut",
            "[Skor KVA = 4–5]\nVegetasi hutan pamah",
            "[Skor PL = 2]\nPerkebunan (Sawit/Karet), Pertanian Lahan Kering Campur & Semak Belukar",
            "Perhitungan: 2(0.20)+5(0.20)+2(0.60) = 2.60. Pada tanah mineral biasa (KBA=2), konversi hutan menjadi perkebunan/kebun campur (PL=2) menurunkan stok karbon ke 2.60."
        ],
        [
            "Sangat Rendah",
            "Skor: 1.40–1.80\n(Solok, Agam, Tanah Datar, Padang)\n134–144 Ribu Ha",
            "[Skor KBA = 1–2]\nDanau, dataran aluvial & perbukitan struktural mineral",
            "[Skor KVA = 2–4]\nVegetasi hutan pegunungan atas / danau / pantai",
            "[Skor PL = 1]\nSawah (PL_PPK=1), Permukiman, Lahan Terbuka, Tambang & Tubuh Air",
            "Perhitungan: 2(0.20)+4(0.20)+1(0.60) = 1.80. Sawah semusim, badan air, dan permukiman memiliki biomassa tegakan pohon mendekati nol (PL=1)."
        ]
    ]
    add_styled_table(s8, anat_headers, ppk_rows, anat_widths, font_size=8.5)

    # =========================================================================
    # SLIDE 9: MENGAPA NILAI SKOR GDB BERBEDA DENGAN RASTER 0.5 METER?
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Mengapa NILAI SKOR JLH_2025_ALL.gdb Berbeda dengan Raster 0.5 Meter?",
               "DIAGNOSTIK MATEMATIS & TEMATIK: PERBEDAAN SKEMA KLASIFIKASI PENUTUPAN LAHAN DAN DEKOMPOSISI PIKSEL")

    diff_val_headers = [
        "Faktor Penyebab",
        "Mekanisme pada JLH_2025_ALL.gdb (Vektor KLHK)",
        "Mekanisme pada Raster Seamless 0.5 Meter",
        "Dampak Nyata pada Nilai Skor & Pergeseran Kelas JLH"
    ]
    diff_val_widths = [Inches(2.1), Inches(3.2), Inches(3.2), Inches(3.83)]
    diff_val_rows = [
        [
            "1. Perbedaan Skor PL pada Hutan Sekunder\n(1.171.166 Ha / 27,8% Sumbar)",
            "Memisahkan Hutan Primer (2001) dan Hutan Sekunder (2002).\nPada Hutan Sekunder:\n• PL_PYA = 2\n• PL_PHK = 4\n• PL_PGN = 3",
            "Citra 0.5m menggabungkan tajuk hutan rapat ke kelas Natural Forest (Kode 2) dengan skor:\n• PL_PYA = 3 (+1 poin)\n• PL_PHK = 5 (+1 poin)\n• PL_PGN = 4 (+1 poin)",
            "Karena bobot PL = 0.60, selisih +1 poin PL menambah +0.60 pada skor total:\n• PYA: Skor naik dari 2.48 (Rendah) → 3.08 (Sedang).\n• PHK Alami: Skor naik dari 3.68 (Tinggi) → 4.28 (Sangat Tinggi).\n• PGN: Skor naik dari 3.24 (Sedang) → 3.84 (Tinggi)."
        ],
        [
            "2. Dekomposisi Kebun Campur / Agroforestri\n(763.755 Ha / 18,1% Sumbar)",
            "Poligon Pertanian Lahan Kering Campur (20092) diberi 1 skor seragam (PL=2 pada PYA, PHK, PPK; PL=3 pada PGA, PGN, PKU).",
            "Resolusi 50 cm mendeteksi objek fisik di dalam kebun campur secara terpisah: kanopi pohon tua terdeteksi sebagai Pohon/Hutan (skor 4–5), petak tanaman sebagai Crops (skor 3–4).",
            "Pada Raster 0.5m, jutaan pohon pelindung/agroforestri di dalam kebun masyarakat mengangkat skor PKU, PPK, dan PGA dari kelas Rendah/Sedang menjadi Tinggi & Sangat Tinggi."
        ],
        [
            "3. Perbedaan Skor PL pada Perkebunan & Sawah\n(891.232 Ha / 21,1% Sumbar)",
            "• Perkebunan (2010): PL_PKU = 3.\n• Sawah (20093): PL_PGN = 5, namun Pertanian Lahan Kering (20091): PL_PGN = 3.",
            "• Plantation (Kode 12): PL_PKU = 4 (+1 poin).\n• Crops (Kode 5): Mencakup sawah & pertanian pangan dengan PL_PGN = 4 dan PL_PYA = 3.",
            "• Pada PKU: Perkebunan naik dari skor 3.40 (Sedang) menjadi 4.00 (Tinggi).\n• Pada PGN: Lahan pertanian kering naik dari skor 3.12 (Sedang) menjadi 3.72 (Tinggi)."
        ],
        [
            "4. Aturan Batas Ambang Kelas (Interval ≤ vs <)",
            "Menggunakan batas tertutup atas (≤):\n• Skor 2.60 → masuk Kelas Rendah\n• Skor 3.40 → masuk Kelas Sedang\n• Skor 4.20 → masuk Kelas Tinggi",
            "Menggunakan batas terbuka atas (<):\n• Skor 2.60 → masuk Kelas Sedang [2.6–3.4)\n• Skor 3.40 → masuk Kelas Tinggi [3.4–4.2)\n• Skor 4.20 → masuk Sangat Tinggi [4.2–5.0]",
            "Kombinasi bobot genap menghasilkan ratusan ribu hektar bernilai persis 2.60 (misal PPK Perkebunan: 2×0.2 + 5×0.2 + 2×0.6 = 2.60). Di GDB masuk Rendah, di Raster masuk Sedang!"
        ]
    ]
    add_styled_table(s9, diff_val_headers, diff_val_rows, diff_val_widths, font_size=8.6)

    # =========================================================================
    # SLIDE 10: MENGAPA LUASAN (HEKTAR) GDB BERBEDA DENGAN RASTER 0.5 METER?
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Mengapa LUASAN (Hektar) JLH_2025_ALL.gdb Berbeda dengan Raster 0.5 Meter?",
               "DIAGNOSTIK KARTOGRAFIS & GEODETIS: TOTAL LUAS (4,21 JUTA HA VS 4,38 JUTA HA) SERTA DISTRIBUSI LUAS KELAS")

    add_card(s10, "1. SELISIH TOTAL CAKUPAN WILAYAH (+166.582 Ha / +3,95%)", [
        ("GDB Vektor (4.213.812 Ha)", "Menggunakan batas poligon daratan skala 1:250.000 / 1:50.000 (37.001 poligon). Pulau-pulau karang kecil, gosong pantai, dan atol mikro tereliminasi saat generalisasi peta dasar."),
        ("Raster 0.5m (4.380.394 Ha)", "Mencakup 3.206 grid tile resolusi 50 cm (175,2 miliar piksel daratan). Seluruh gugusan pulau kecil di Kepulauan Mentawai, Pesisir Selatan, dan Pasaman Barat serta sabuk pantai terpetakan utuh."),
        ("Distorsi Proyeksi Grid (EPSG:3857)", "Raster dihitung pada grid Web Mercator (0.25 m²/piksel), sedangkan kolom LUAS_HA pada GDB dihitung pada sistem proyeksi silinder sama-luas (Equal-Area / Geodesic).")
    ], Inches(0.5), Inches(1.25), Inches(6.0), Inches(2.85), C_NAVY)

    add_card(s10, "2. EFEK MINIMUM MAPPING UNIT (MMU) VS PIKSEL 0.25 m²", [
        ("Generalisasi Kartografi GDB", "Poligon penutupan lahan KLHK memiliki MMU ~6,25 Ha (2,5 mm × 2,5 mm pada skala 1:50.000). Objek yang lebih kecil dari 6,25 Ha dilebur (dissolved) ke dalam poligon dominan di sekelilingnya."),
        ("Resolusi Ultra-Tinggi 0.25 m²", "Pada raster 0.5m, setiap elemen berukuran 50 cm × 50 cm memiliki kelas sendiri. Tidak ada penyederhanaan batas poligon."),
        ("Akibat pada Distribusi Luas", "Jaringan jalan raya, jalan lingkungan, rumah terpencar di pedesaan, alur sungai kecil, dan kolam rakyat terhitung luasnya secara riil pada Raster 0.5m, namun hilang/terserap di GDB.")
    ], Inches(6.83), Inches(1.25), Inches(6.0), Inches(2.85), C_TEAL)

    add_card(s10, "3. EFEK KONTINUITAS RASTER KBA & KVA PADA SEMPADAN & DANAU", [
        ("Tubuh Air & Danau", "Di GDB, Danau Singkarak & Maninjau terpotong tegas sebagai poligon tunggal. Di Raster 0.5m, zona ekoton tepian danau, rawa musiman, dan badan sungai bermeander terpetakan mengikuti piksel air aktual tahun 2025."),
        ("Pergeseran Luas Antar Kelas", "Akibat gabungan (1) detail piksel 0.5m, (2) perbedaan skor lookup PL Hutan Sekunder/Kebun, dan (3) batas ambang kelas, terjadi pergeseran luasan masif dari kelas Rendah/Sedang (di GDB) menuju kelas Sedang/Tinggi/Sangat Tinggi (di Raster 0.5m).")
    ], Inches(0.5), Inches(4.25), Inches(12.33), Inches(1.65), C_BLUE)

    # Bottom Summary Strip
    strip = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.02), Inches(12.33), Inches(1.1))
    strip.fill.solid()
    strip.fill.fore_color.rgb = RGBColor(235, 245, 251)
    strip.line.color.rgb = C_TEAL
    tf_st = strip.text_frame
    tf_st.word_wrap = True
    p_st1 = tf_st.paragraphs[0]
    p_st1.text = "KESIMPULAN KOMPARASI GDB VS RASTER 0.5 METER:"
    p_st1.font.size = Pt(10)
    p_st1.font.bold = True
    p_st1.font.color.rgb = C_NAVY
    p_st2 = tf_st.add_paragraph()
    p_st2.text = (
        "Kedua dataset menggunakan BOBOT RUMUS YANG 100% IDENTIK. Perbedaan nilai dan luasan bukan karena kesalahan hitung, melainkan konsekuensi ilmiah dari: "
        "(1) Skala pengamatan (Makro 1:50.000/1:250.000 vs Mikro 0.5m), (2) Klasifikasi Hutan Sekunder & Kebun Campur pada tabel skor PL, serta (3) Konvensi batas interval kelas (≤ vs <). "
        "Gunakan GDB untuk pelaporan RPPLH/KLHS makro tingkat provinsi, dan gunakan Raster 0.5m untuk analisis tapak, AMDAL, dan mitigasi bencana lokal."
    )
    p_st2.font.size = Pt(9.2)
    p_st2.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 11: MATRIKS RINGKASAN KOMPARASI 6 INDIKATOR (REKAPITULASI LENGKAP)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Matriks Rekapitulasi Perbandingan Luasan & Penyebab Utama per Indikator")

    rec_headers = [
        "Indikator JLH\n(Bobot KBA : KVA : PL)",
        "Kelas Dominan di\nJLH_2025_ALL.gdb",
        "Kelas Dominan di\nRaster 0.5 Meter",
        "Selisih Utama\n(Raster vs GDB)",
        "Akar Penyebab Perbedaan Nilai & Luasan\n(Berdasarkan Parameter KBA, KVA, dan PL)"
    ]
    rec_widths = [Inches(2.05), Inches(2.2), Inches(2.2), Inches(2.1), Inches(3.78)]
    rec_rows = [
        [
            "1. PGA - Pengaturan Air\n(0.28 : 0.12 : 0.60)",
            "Sedang: 41,57%\n(1.751.883 Ha)\nSangat Tinggi: 33,88%",
            "Sangat Tinggi: 48,19%\n(2.110.935 Ha)\nSedang: 26,24%",
            "Sangat Tinggi:\n+683.121 Ha (+14,3%)\nSedang: -602.445 Ha",
            "Di dalam poligon Pertanian Lahan Kering Campur (763 ribu Ha, GDB PL=3), citra 0.5m mendeteksi kanopi pepohonan rapat sebagai Hutan/Pohon (PL=5), sehingga skor naik dari 2.96 (Sedang) ke 4.16–4.44 (Tinggi/Sangat Tinggi)."
        ],
        [
            "2. PYA - Penyedia Air\n(0.32 : 0.08 : 0.60)",
            "Rendah: 56,12%\n(2.364.620 Ha)\nSedang: 41,53%",
            "Sedang: 71,08%\n(3.113.503 Ha)\nRendah: 20,35%",
            "Sedang:\n+1.363.643 Ha (+29,6%)\nRendah: -1.473.315 Ha",
            "Pada GDB, Hutan Sekunder (1,17 juta Ha) diberi skor PL_PYA = 2 (Skor = 2.48 → Rendah). Pada Raster 0.5m, Natural Forest diberi skor PL_PYA = 3 dan Crops PL_PYA = 3 (Skor = 3.08 → Sedang)."
        ],
        [
            "3. PGN - Penyedia Pangan\n(0.28 : 0.12 : 0.60)",
            "Sedang: 52,22%\n(2.200.546 Ha)\nTinggi: 38,97%",
            "Tinggi: 72,86%\n(3.191.533 Ha)\nSedang: 15,33%",
            "Tinggi:\n+1.549.535 Ha (+33,9%)\nSedang: -1.528.874 Ha",
            "Pada GDB, Hutan Sekunder & Pertanian Lahan Kering diberi PL_PGN = 3 (Skor 3.24 → Sedang). Pada Raster 0.5m, Natural Forest & Crops diberi PL_PGN = 4 sehingga di atas tanah vulkanik/sedimen skornya 3.84 (Tinggi)."
        ],
        [
            "4. PKU - Kualitas Udara\n(0.15 : 0.25 : 0.60)",
            "Sangat Tinggi: 46,07%\n(1.941.460 Ha)\nSedang: 38,62%",
            "Sangat Tinggi: 65,54%\n(2.870.741 Ha)\nTinggi: 21,43%",
            "Sangat Tinggi:\n+929.281 Ha (+19,5%)\nSedang: -1.107.689 Ha",
            "Pada GDB, Perkebunan diberi PL_PKU = 3 (Skor 3.40 → masuk Sedang karena aturan ≤ 3.40). Pada Raster 0.5m, Plantation diberi PL_PKU = 4 dan tajuk pohon kebun campur terdeteksi sebagai hutan (PL=5 → Sangat Tinggi)."
        ],
        [
            "5. PHK - Habitat & Kehati\n(0.24 : 0.16 : 0.60)",
            "Alami: Rendah 33,5%, Tinggi 33,3%, ST 5,1%\nKK: Sangat Tinggi 37,5%",
            "Alami:\nTinggi: 31,12%\nSangat Tinggi: 31,09%",
            "Sangat Tinggi (Alami):\n+1.146.151 Ha (+26,0%)\nselaras dengan GDB KK",
            "Pada GDB Alami, Hutan Sekunder diberi PL_PHK = 4 (Skor 3.68 → Tinggi) dan baru menjadi 5.0 setelah dioverride KK. Pada Raster 0.5m, Natural Forest langsung bernilai PL_PHK = 5 (Skor 4.28 → Sangat Tinggi)."
        ],
        [
            "6. PPK - Simpan Karbon\n(0.20 : 0.20 : 0.60)",
            "Rendah: 50,22%\n(2.116.121 Ha)\nSangat Tinggi: 28,73%",
            "Sangat Tinggi: 57,21%\n(2.505.834 Ha)\nSedang: 21,24%",
            "Sangat Tinggi:\n+1.295.048 Ha (+28,5%)\nRendah: -1.476.629 Ha",
            "1) Skor 2.60 pada Perkebunan/Kebun di GDB masuk kelas Rendah (≤2.60), sedangkan di Raster masuk Sedang (≥2.60). 2) Kanopi pohon rapat di kebun campur terdeteksi sebagai hutan (PL=5 → Sangat Tinggi)."
        ]
    ]
    add_styled_table(s11, rec_headers, rec_rows, rec_widths, font_size=8.3)

    out_file1 = "Analisis_KBA_KVA_PL_dan_Komparasi_JLH_Sumbar_2025.pptx"
    out_file2 = "Matriks_Perbandingan_JLH_Sumbar_2025.pptx"
    prs.save(out_file1)
    prs.save(out_file2)
    print(f"Berhasil membuat presentasi: {out_file1} dan memperbarui {out_file2}")

if __name__ == "__main__":
    create_deep_analysis_pptx()
