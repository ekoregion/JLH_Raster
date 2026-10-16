import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    for shd in tcPr.findall(qn('w:shd')):
        tcPr.remove(shd)
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shading)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout(doc, text, title="CATATAN TEKNIS & METODOLOGI:"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"{title}\n")
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(9.5)
    run_b.font.italic = True
    run_b.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, caption=None):
    if caption:
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(8)
        cp.paragraph_format.space_after = Pt(2)
        r_cap = cp.add_run(f"Skrip Program: {caption}")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="E1E4E8"/>'
        f'  <w:left w:val="single" w:sz="20" w:space="0" w:color="3B6998"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="E1E4E8"/>'
        f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="E1E4E8"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x24, 0x29, 0x2E)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_detailed_jlh_doc():
    doc = docx.Document()
    
    # Page Margins (1 inch = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # HEADER / COVER TITLE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(4)
    r_inst = p_inst.add_run(
        "KEMENTERIAN LINGKUNGAN HIDUP / BADAN PENGENDALIAN LINGKUNGAN HIDUP (BPLH)\n"
        "DIREKTORAT PENYELENGGARAAN SUMBER DAYA ALAM BERKELANJUTAN"
    )
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("PEDOMAN TEKNIS & DOKUMENTASI METODOLOGI\nPENYUSUNAN JASA LINGKUNGAN HIDUP (JLH)")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run(
        "Provinsi Sumatera Barat (Tahun Analisis: 2025–2026)\n"
        "Transformasi Spasial Karakteristik Bentang Alam (KBA), Karakteristik Vegetasi Alami (KVA), "
        "dan Penutupan Lahan (PL) Multiskala Berbasis Cloud Computing Resolusi Ultra-Tinggi (0.5 Meter Seamless)"
    )
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x69, 0x84)

    # Metadata Table
    meta_tbl = doc.add_table(rows=1, cols=1)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = meta_tbl.cell(0, 0)
    set_cell_background(c, "F4F6F9")
    set_cell_margins(c, top=120, bottom=120, left=160, right=160)
    set_table_borders(meta_tbl, color="CBD5E1", sz="6")
    p_m = c.paragraphs[0]
    p_m.paragraph_format.line_spacing = 1.15
    p_m.paragraph_format.space_after = Pt(0)
    p_m.add_run("IDENTITAS DOKUMEN & SPESIFIKASI DATA:\n").bold = True
    p_m.add_run("• Ruang Lingkup Wilayah: ").bold = True
    p_m.add_run("Provinsi Sumatera Barat (19 Kabupaten/Kota)\n")
    p_m.add_run("• Resolusi Spasial Grid: ").bold = True
    p_m.add_run("0.5 Meter x 0.5 Meter (Ultra-High Resolution Seamless)\n")
    p_m.add_run("• Sistem Proyeksi Koordinat: ").bold = True
    p_m.add_run("EPSG:3857 (WGS 84 / Pseudo-Mercator)\n")
    p_m.add_run("• Enkoding & Format Data: ").bold = True
    p_m.add_run("Cloud Optimized GeoTIFF (COG), Kompresi LERC_ZSTD (Lossless-Floating Max Error 0.005)\n")
    p_m.add_run("• Enkoding KBA & KVA: ").bold = True
    p_m.add_run("UInt8 (Skala 1 - 255) Kompresi Zstandard (Level 9)\n")
    p_m.add_run("• Jumlah Tile Tutupan Lahan: ").bold = True
    p_m.add_run("~2.300+ Grid Tile Citra Satelit Multiskala Tahun 2025\n")
    p_m.add_run("• Tahun Penyusunan: ").bold = True
    p_m.add_run("Oktober 2026")
    for r in p_m.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # DAFTAR ISI
    # =========================================================================
    h_toc = doc.add_heading("DAFTAR ISI", level=1)
    h_toc.paragraph_format.space_before = Pt(14)
    h_toc.paragraph_format.space_after = Pt(4)
    h_toc.style.font.name = "Arial"
    h_toc.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    toc_items = [
        "1. Landasan Hukum, Kebijakan, dan Kerangka Konseptual JLH",
        "2. Definisi & Karakteristik Fisis 6 Indikator Layanan Ekosistem Prioritas",
        "3. Tiga Pilar Komponen Input JLH (KBA, KVA, dan PL 2025)",
        "   3.1 Karakteristik Bentang Alam (KBA) - Faktor Abiotik Geomorfologi",
        "   3.2 Karakteristik Vegetasi Alami (KVA) - Faktor Integritas Ekologis",
        "   3.3 Penutupan Lahan (PL) Multiskala 2025 - Faktor Pemanfaatan Antropogenik",
        "4. Formulasi Matematis & Pembobotan Regional Sumatera",
        "   4.1 Model Kombinasi Linear Terbobot",
        "   4.2 Rasionalisasi Saintifik Proporsi Bobot Tiap Indikator",
        "5. Matriks Penilaian & Tabel Lookup Penutupan Lahan (15 Kelas)",
        "6. Pipeline Arsitektur Komputasi Python Grid 0.5 Meter",
        "   6.1 Skrip Tahap 1: Ekstraksi & Rasterisasi Grid KBA dan KVA (generate_kba_kva_grids.py)",
        "   6.2 Skrip Tahap 2: Penggabungan Master KBA & KVA Menjadi Seamless UInt8 ZSTD (create_seamless_kba_kva.py)",
        "   6.3 Skrip Tahap 3: Kalkulasi Paralel Multi-Core 6 Indikator JLH (calculate_jlh_sumbar_2025.py)",
        "   6.4 Skrip Tahap 4: Mozaik Virtual Raster (VRT) & Ekspor LERC_ZSTD Chunking (create_seamless_jlh_lerc.py)",
        "   6.5 Skrip Tahap 5: Penyesuaian Legal Kriteria Khusus pada Layer PHK (apply_kk_phk.py)",
        "   6.6 Skrip Tahap 6: Pembentukan Piramida Resolusi Spasial (Internal Overviews)",
        "7. Spesifikasi Teknis Produk Akhir Raster Seamless Se-Sumatera Barat",
        "8. Panduan Standard Operating Procedure (SOP) Analisis & Visualisasi di QGIS / ArcGIS",
        "9. Ringkasan & Rekomendasi Pemeliharaan Data Geospasial"
    ]
    for item in toc_items:
        p_ti = doc.add_paragraph()
        p_ti.paragraph_format.space_before = Pt(1)
        p_ti.paragraph_format.space_after = Pt(1)
        r = p_ti.add_run(item)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        if item.startswith("   "):
            r.font.color.rgb = RGBColor(0x4A, 0x69, 0x84)
            p_ti.paragraph_format.left_indent = Inches(0.2)
        else:
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # BAB 1
    # =========================================================================
    h1 = doc.add_heading("1. Landasan Hukum, Kebijakan, dan Kerangka Konseptual JLH", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(4)
    h1.style.font.name = "Arial"
    h1.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Jasa Lingkungan Hidup (JLH) atau Ecosystem Services didefinisikan sebagai kontribusi langsung maupun tidak langsung "
        "dari ekosistem alami dan bentang alam terhadap kesejahteraan hidup manusia, keberlanjutan ekonomi, dan ketahanan hayati. "
        "Penyusunan peta spasial JLH di Provinsi Sumatera Barat memiliki landasan hukum yang kuat dalam tatanan regulasi nasional Republik Indonesia:"
    )

    regulations = [
        ("Undang-Undang Nomor 32 Tahun 2009 tentang Perlindungan dan Pengelolaan Lingkungan Hidup: ", 
         "Pasal 15 dan 19 mengamanatkan bahwa penyusunan Rencana Perlindungan dan Pengelolaan Lingkungan Hidup (RPPLH) "
         "serta Kajian Lingkungan Hidup Strategis (KLHS) wajib mendasarkan pada inventarisasi daya dukung dan daya tampung lingkungan hidup (D3TLH) yang salah satu pilar intinya adalah valuasi dan pemodelan spasial jasa ekosistem."),
        ("Peraturan Pemerintah Nomor 46 Tahun 2017 tentang Instrumen Ekonomi Lingkungan Hidup: ", 
         "Mewajibkan pemetaan fungsi penyedia, pengatur, dan pendukung lingkungan hidup sebagai basis penentuan kompensasi jasa lingkungan (Payment for Ecosystem Services / PES) dan neraca sumber daya alam."),
        ("Permen LHK Terkait Pedoman Penyusunan RPPLH & D3TLH: ", 
         "Menetapkan standardisasi metodologi analisis ekoregion berbasis keterpaduan bentang alam (geofisik), tutupan vegetasi alami, dan pemanfaatan lahan aktual."),
        ("Konteks Kebutuhan Daerah Provinsi Sumatera Barat: ", 
         "Sebagai provinsi yang berada di zona Busur Vulkanik Bukit Barisan dan Patahan Semangko (The Great Sumatran Fault), "
         "Sumatera Barat menghadapi tantangan tinggi degradasi ekosistem hulu dan kerentanan bencana. Data spasial JLH ultra-detail (0.5 meter) "
         "sangat mendesak untuk memandu pemulihan lingkungan, perizinan berusaha, tata ruang kehutanan, dan penetapan zona perlindungan mutlak.")
    ]
    for r_title, r_desc in regulations:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(2)
        pb.paragraph_format.space_after = Pt(2)
        r_rt = pb.add_run(r_title)
        r_rt.bold = True
        r_rt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(r_desc)

    add_callout(
        doc,
        "Prinsip Dasar Pemodelan JLH:\n"
        "JLH bukanlah sekadar peta tematik penutupan lahan, melainkan sintesis kuantitatif antara fondasi fisik permanen (KBA), "
        "kapasitas ekologis klimaks (KVA), dan wujud pemanfaatan lahan antropogenik saat ini (PL). "
        "Dengan resolusi 0.5 meter, batas-batas koridor sempadan sungai, kebun masyarakat, kantong habitat hutan, dan formasi lereng terpetakan secara presisi setingkat skala tapak (1:1.000).",
        title="PENDEKATAN SAINTIFIK EKOREGION BERESOLUSI ULTRA-TINGGI:"
    )

    # =========================================================================
    # BAB 2
    # =========================================================================
    h2 = doc.add_heading("2. Definisi & Karakteristik Fisis 6 Indikator Layanan Ekosistem Prioritas", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(4)
    h2.style.font.name = "Arial"
    h2.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Berdasarkan klasifikasi Millennium Ecosystem Assessment (MEA) dan standardisasi Direktorat Penyelenggaraan Sumber Daya Alam "
        "Berkelanjutan KLH/BPLH, pemodelan JLH Sumatera Barat mencakup 6 Indikator Prioritas dengan rentang nilai skala 1.0 (Sangat Rendah) hingga 5.0 (Sangat Tinggi):"
    )

    ind_details = [
        ("1. PGA - Pengaturan Air (Water Regulation):",
         "Kapasitas lanskap dalam meregulasi dinamika hidrologis permukaan dan bawah permukaan, mencakup kapasitas infiltrasi tanah, "
         "retensi air limpasan hujan, pemeliharaan debit aliran dasar (baseflow), dan pengurangan puncak banjir. "
         "Kawasan berhutan lebat di dataran tinggi vulkanik dan perbukitan karst memiliki nilai PGA tertinggi (skor 4–5), "
         "sedangkan lahan terbangun rapat dan tanah terbuka memiliki nilai PGA terendah (skor 1–2)."),
        ("2. PHK - Pendukung Habitat & Keanekaragaman Hayati (Biodiversity & Habitat Support):",
         "Kemampuan ekosistem untuk menyediakan ruang hidup, habitat berkembang biak, sumber pakan, dan koridor migrasi bagi flora dan fauna liar asli Sumatera. "
         "Indikator ini menjadi instrumen utama dalam perlindungan spesies kunci (seperti Harimau Sumatera, Tapir, Rangkong, dan flora endemik Rafflesia). "
         "Hutan primer dan kawasan konservasi memiliki nilai mutlak tertinggi."),
        ("3. PPK - Penyerap & Penyimpan Karbon (Carbon Sequestration & Storage):",
         "Potensi biomassa vegetasi di atas dan di bawah tanah (Aboveground & Belowground Biomass), nekromasa, serta bahan organik tanah "
         "dalam menyerap dan mengunci emisi karbon dioksida (CO2) atmosfer. Sangat krusial dalam mendukung komitmen Indonesia Folu Net Sink 2030 "
         "dan penurunan emisi gas rumah kaca daerah."),
        ("4. PYA - Penyedia Air Bersih (Water Provisioning):",
         "Ketersediaan debit dan volume air bersih alami yang dapat dimanfaatkan secara langsung oleh masyarakat untuk konsumsi domestik, "
         "sanitasi, irigasi pertanian, dan kelangsungan hidup. Menggabungkan keberadaan badan air, mata air, dan cekungan air tanah alami."),
        ("5. PGN - Penyedia Pangan (Food Provisioning):",
         "Kapasitas lanskap dalam memproduksi bahan pangan nabati maupun hewani lokal secara berkelanjutan, meliputi sawah irigasi, "
         "pertanian lahan kering, perikanan darat, agroforestri, dan kebun pangan masyarakat."),
        ("6. PKU - Pengatur Kualitas Udara (Air Quality Regulation):",
         "Peran kanopi vegetasi dalam menyaring partikulat polutan (PM2.5, PM10), menyerap gas beracun (NOx, SOx, CO), memproduksi oksigen, "
         "serta menjaga kelembaban dan kesejukan iklim mikro setempat.")
    ]

    for title, desc in ind_details:
        doc.add_heading(title, level=2)
        doc.add_paragraph(desc)

    # =========================================================================
    # BAB 3
    # =========================================================================
    h3 = doc.add_heading("3. Tiga Pilar Komponen Input JLH (KBA, KVA, dan PL 2025)", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(4)
    h3.style.font.name = "Arial"
    h3.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Kekuatan utama pemodelan JLH Sumatera Barat terletak pada integrasi multi-layer yang memadukan faktor abiotik, biotik, dan antropogenik:"
    )

    doc.add_heading("3.1 Karakteristik Bentang Alam (KBA)", level=2)
    doc.add_paragraph(
        "KBA mencerminkan kondisi geomorfologi abiotik yang terbentuk secara evolusioner dalam skala geologis. "
        "Peta KBA diklasifikasikan dari analisis bentuk lahan (landform unit), elevasi topografi DEMNAS, kelerengan lereng, dan litologi batuan induk. "
        "Di Sumatera Barat, satuan KBA mencakup:\n"
        "• Satuan Vulkanik (Kerucut Gunung Api Marapi, Singgalang, Talang, Tandikat) dengan tanah andosol subur dan daya serap air sangat tinggi.\n"
        "• Satuan Perbukitan Karst Struktural (Payakumbuh, Ngalau Indah) yang berfungsi sebagai reservoir akuifer air tanah dalam.\n"
        "• Satuan Dataran Aluvial & Dataran Pantai (Pesisir Padang, Pariaman, Pesisir Selatan) yang menampung aliran permukaan dan sedimen.\n"
        "• Satuan Perbukitan Tektonik Terlipat (Pegunungan Bukit Barisan) yang memiliki kemiringan terjal dan rentan terhadap erosi fisik.\n"
        "Setiap unit KBA diberi nilai skor integer 1 sampai 5 untuk tiap indikator JLH, di mana angka 5 mewakili fungsi bentang alam paling optimal."
    )

    doc.add_heading("3.2 Karakteristik Vegetasi Alami (KVA)", level=2)
    doc.add_paragraph(
        "KVA merepresentasikan kondisi tipe ekosistem klimaks vegetasi alami yang ada sebelum terjadinya modifikasi masif oleh manusia. "
        "KVA diekstraksi dari rekonstruksi tipe formasi hutan tropika Sumatera Barat, meliputi:\n"
        "• Hutan Hujan Pegunungan Tinggi (Subalpin & Montane Forest): Kanopi padat lumut, vegetasi kerdil, fungsi retensi kabut dan air sangat tinggi.\n"
        "• Hutan Hujan Tropika Dataran Rendah (Lowland Dipterocarp Forest): Keanekaragaman pohon famili Dipterocarpaceae tertinggi di dunia, cadangan karbon raksasa.\n"
        "• Hutan Rawa Gambut & Rawa Air Tawar (Freshwater Peat Swamp): Cadangan karbon organik tanah dan penyeimbang tata air pesisir barat.\n"
        "• Formasi Vegetasi Mangrove Pesisir: Pelindung garis pantai dari abrasi gelombang dan habitat pembibitan biota laut.\n"
        "Nilai KVA mencerminkan nilai intrinsik ekologis yang menjadi penyeimbang penting terhadap intervensi manusia."
    )

    doc.add_heading("3.3 Penutupan Lahan (PL) Multiskala 2025", level=2)
    doc.add_paragraph(
        "Penutupan Lahan (PL) 2025 merupakan komponen paling dinamis yang mencerminkan wujud fisik tutupan permukaan bumi terkini. "
        "Data PL diproduksi melalui klasifikasi berbasis citra satelit resolusi sangat tinggi tahun 2025 menggunakan model Machine Learning/Deep Learning, "
        "yang menghasilkan 15 kelas tutupan lahan pada resolusi spasial 0.5 meter. Data PL terbagi ke dalam ~2.300+ grid tile se-Sumatera Barat, "
        "mampu membedakan dengan sangat tajam antara tajuk pohon alami, kebun campuran, lahan sawah, jalan beraspal, dan bangunan fisik."
    )

    # =========================================================================
    # BAB 4
    # =========================================================================
    h4 = doc.add_heading("4. Formulasi Matematis & Pembobotan Regional Sumatera", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(4)
    h4.style.font.name = "Arial"
    h4.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_heading("4.1 Model Kombinasi Linear Terbobot", level=2)
    doc.add_paragraph(
        "Perhitungan skor indeks JLH pada setiap sel piksel (resolusi 0.5m x 0.5m) menggunakan fungsi linear multivariat:"
    )
    add_callout(
        doc,
        "JLH_k = (Skor_KBA_k × W_KBA_k) + (Skor_KVA_k × W_KVA_k) + (Skor_PL_k × W_PL_k)\n\n"
        "Keterangan:\n"
        "• k : Indeks indikator jasa lingkungan hidup (PGA, PHK, PPK, PYA, PGN, PKU).\n"
        "• Skor_KBA, Skor_KVA, Skor_PL : Skor bernilai 1.0 s.d. 5.0.\n"
        "• W_KBA, W_KVA, W_PL : Bobot proporsional regional (W_KBA + W_KVA + W_PL = 1.00).\n"
        "• JLH_k : Skor akhir kontinu (Float32) bernilai 1.00 s.d. 5.00 pada daratan valid, dan 0.00 pada area NoData/Laut.",
        title="FORMULA MATEMATIS MULTIVARIAT JLH:"
    )

    doc.add_heading("4.2 Rasionalisasi Saintifik Proporsi Bobot Tiap Indikator", level=2)
    doc.add_paragraph(
        "Berdasarkan karakteristik biogeofisik Regional Pulau Sumatera, tutupan lahan aktual (PL) ditetapkan memegang peranan dominan "
        "sebesar 60% (W_PL = 0.60) karena aktivitas manusia pada tutupan lahan secara langsung mengubah siklus biogeokimia dan hidrologi. "
        "Sisa bobot 40% dialokasikan secara bervariasi antara Bentang Alam (KBA) dan Vegetasi Alami (KVA) berdasarkan sifat fisis indikator:"
    )

    # Weight Table
    tbl_w = doc.add_table(rows=7, cols=6)
    tbl_w.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_w = ["Indikator JLH", "W_KBA", "W_KVA", "W_PL", "Total", "Rasionalisasi Saintifik Pembobotan Regional"]
    for j, h_text in enumerate(headers_w):
        cell = tbl_w.cell(0, j)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [1, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h_text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_w = [
        ("PGA (Pengaturan Air)", "0.28", "0.12", "0.60", "1.00", 
         "Morfologi bentang alam (kemiringan lereng & litologi batuan KBA) sangat mendominasi kapasitas infiltrasi dan pencegahan banjir bandang dibanding tipe vegetasi alami."),
        ("PHK (Habitat & Kehati)", "0.24", "0.16", "0.60", "1.00", 
         "Tipe vegetasi klimaks (KVA) dan keragaman topografi (KBA) menyediakan relung ekologis spesifik yang mendukung keanekaragaman hayati endemik."),
        ("PPK (Penyimpan Karbon)", "0.20", "0.20", "0.60", "1.00", 
         "Biomassa vegetasi alami (KVA) dan tutupan lahan aktual (PL) memiliki kontribusi seimbang terhadap stok karbon di atas dan di bawah permukaan tanah."),
        ("PYA (Penyedia Air)", "0.32", "0.08", "0.60", "1.00", 
         "Cekungan air tanah, geomorfologi karst/vulkanik, dan struktur geologi KBA paling menentukan ketersediaan debit air permukaan dan mata air alami."),
        ("PGN (Penyedia Pangan)", "0.28", "0.12", "0.60", "1.00", 
         "Tingkat kesuburan tanah vulkanik dan dataran aluvium KBA sangat menentukan potensi produktivitas pangan nabati maupun hewani."),
        ("PKU (Kualitas Udara)", "0.15", "0.25", "0.60", "1.00", 
         "Kerapatan tajuk kanopi vegetasi alami (KVA) sangat dominan dalam menyerap partikulat debu, memproduksi oksigen, dan mereduksi suhu panas perkotaan.")
    ]

    for row_idx, row_vals in enumerate(data_w, start=1):
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text_val in enumerate(row_vals):
            cell = tbl_w.cell(row_idx, col_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [1, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text_val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True

    set_table_borders(tbl_w, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # BAB 5
    # =========================================================================
    h5 = doc.add_heading("5. Matriks Penilaian & Tabel Lookup Penutupan Lahan (15 Kelas)", level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)
    h5.style.font.name = "Arial"
    h5.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Tabel berikut menyajikan matriks konversi resmi dari kelas piksel Penutupan Lahan 2025 (kategori integer 1 s.d. 15) "
        "menjadi nilai skor layanan ekosistem skala 1 (Sangat Rendah) hingga 5 (Sangat Tinggi):"
    )

    tbl_pl = doc.add_table(rows=12, cols=8)
    tbl_pl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_pl = ["Kode", "Kategori Penutupan Lahan (PL 2025)", "PGA", "PHK", "PPK", "PYA", "PGN", "PKU"]
    for j, h_text in enumerate(headers_pl):
        cell = tbl_pl.cell(0, j)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h_text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_pl = [
        ("1", "Water (Badan Air / Danau / Sungai)", "5", "1", "1", "5", "4", "5"),
        ("2", "Natural Forest (Hutan Hujan Alami)", "5", "5", "5", "3", "4", "5"),
        ("4", "Flooded Vegetation (Rawa / Mangrove)", "4", "3", "3", "3", "4", "5"),
        ("5", "Crops (Pertanian Tanaman Pangan / Sawah)", "3", "1", "1", "3", "4", "3"),
        ("7", "Development Space (Lahan Terbuka Binaan)", "2", "1", "1", "2", "1", "2"),
        ("8", "Bare Ground (Tanah Terbuka / Bekas Tambang)", "1", "1", "1", "1", "1", "1"),
        ("11", "Rangeland (Padang Rumput / Semak Belukar)", "3", "2", "2", "1", "2", "3"),
        ("12", "Plantation (Perkebunan Sawit / Karet / dsb)", "3", "2", "2", "2", "3", "4"),
        ("13", "Uncertain Trees (Pohon Campuran / Agroforestri)", "3", "3", "2", "2", "3", "3"),
        ("14", "Road (Jaringan Jalan & Infrastruktur Transportasi)", "1", "1", "1", "1", "1", "1"),
        ("15", "Building (Kawasan Terbangun / Permukiman / Gedung)", "1", "1", "1", "2", "1", "1")
    ]

    for row_idx, row_vals in enumerate(data_pl, start=1):
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text_val in enumerate(row_vals):
            cell = tbl_pl.cell(row_idx, col_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text_val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True

    set_table_borders(tbl_pl, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # BAB 6
    # =========================================================================
    h6 = doc.add_heading("6. Pipeline Arsitektur Komputasi Python Grid 0.5 Meter", level=1)
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(4)
    h6.style.font.name = "Arial"
    h6.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Pemrosesan spasial se-Provinsi Sumatera Barat pada resolusi ultra-tinggi 0.5 meter mencakup wilayah seluas "
        "sekitar 42.000 km² dengan total dimensi matriks piksel mencapai 739.298 kolom × 1.001.630 baris (~740 Miliar Piksel). "
        "Pendekatan pengolahan konvensional (in-memory processing) dipastikan akan gagal karena membutuhkan RAM lebih dari 1.5 Terabyte. "
        "Oleh karena itu, dirancang arsitektur pipeline komputasi terdistribusi dalam 6 tahapan terstruktur:"
    )

    # 6.1
    doc.add_heading("6.1 Skrip Tahap 1: Ekstraksi & Rasterisasi Grid KBA dan KVA (generate_kba_kva_grids.py)", level=2)
    doc.add_paragraph(
        "Skrip ini bertugas memotong data poligon vektor KBA dan KVA ke dalam kisi-kisi grid ubin (tile) yang presisi "
        "selaras dengan kisi grid tutupan lahan (Origin X: 11110809.99, Origin Y: 101049.75, Step Size: 3974.72m, Dimensi: 7949 x 7949 piksel). "
        "Setiap fitur poligon di-rasterisasi menggunakan rasterio.features.rasterize dengan kompresi LZW dan block size 512x512:"
    )

    code_kba_kva = """# ==============================================================================
# EKSTRAKSI & RASTERISASI KBA & KVA PER TILE GRID (0.5 METER)
# File: generate_kba_kva_grids.py
# ==============================================================================
import os, glob, time, openpyxl
import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
from shapely.geometry import box
import geopandas as gpd

# Parameter Grid Acuan Selaras Tutupan Lahan 2025
REF_X = 11110809.99449189      # Koordinat X Kiri Atas
REF_Y = 101049.75140393605     # Koordinat Y Kiri Atas
STEP_M = 3974.7246             # Ukuran grid per tile (meter)
TILE_W = 7949                  # Lebar piksel (7949 * 0.5m = 3974.5m)
TILE_H = 7949                  # Tinggi piksel
RES = 0.5                      # Resolusi 0.5 meter

def rasterize_tile_vector(gdf_layer, col_val, bounds, out_tif_path):
    \"\"\"Memotong poligon dengan bounding box dan merasterisasi secara cepat\"\"\"
    minx, miny, maxx, maxy = bounds
    tile_geom = box(minx, miny, maxx, maxy)
    
    # Spatial filter subset
    sub_gdf = gdf_layer[gdf_layer.intersects(tile_geom)]
    if sub_gdf.empty:
        arr = np.zeros((TILE_H, TILE_W), dtype=np.uint8)
    else:
        shapes = ((geom, int(val)) for geom, val in zip(sub_gdf.geometry, sub_gdf[col_val]))
        trans = from_origin(minx, maxy, RES, RES)
        arr = rasterize(shapes=shapes, out_shape=(TILE_H, TILE_W), transform=trans, fill=0, dtype=np.uint8)
        
    profile = {
        'driver': 'GTiff', 'dtype': 'uint8', 'nodata': 0,
        'width': TILE_W, 'height': TILE_H, 'count': 1,
        'crs': 'EPSG:3857', 'transform': from_origin(minx, maxy, RES, RES),
        'tiled': True, 'blockxsize': 512, 'blockysize': 512, 'compress': 'lzw'
    }
    with rasterio.open(out_tif_path, 'w', **profile) as dst:
        dst.write(arr, 1)"""
    add_code_block(doc, code_kba_kva, caption="generate_kba_kva_grids.py (Rasterisasi Tile KBA/KVA)")

    # 6.2
    doc.add_heading("6.2 Skrip Tahap 2: Penggabungan Master KBA & KVA Menjadi Seamless UInt8 ZSTD (create_seamless_kba_kva.py)", level=2)
    doc.add_paragraph(
        "Setelah ribuan tile KBA dan KVA selesai dirasterisasi, seluruh tile digabungkan menjadi file Virtual Raster (.vrt), "
        "kemudian diekspor menjadi GeoTIFF utuh satu file (seamless) se-Sumatera Barat menggunakan tipe data UInt8 (1 byte per piksel) "
        "dan kompresi Zstandard level 9. Hasilnya menghasilkan file master KBA sebesar 178 MB dan KVA sebesar 169 MB yang sangat ringan dibuka di SIG:"
    )

    code_kba_seamless = """# ==============================================================================
# PENGGABUNGAN VRT KBA & KVA KE GEOTIFF SEAMLESS UINT8 ZSTD
# File: create_seamless_kba_kva.py
# ==============================================================================
import rasterio
from rasterio.windows import Window
import numpy as np

def convert_vrt_to_seamless_uint8(vrt_path, output_path, chunk_size=8192):
    with rasterio.open(vrt_path) as src:
        meta = src.meta.copy()
        width, height = src.width, src.height

        meta.update({
            "driver": "GTiff",
            "dtype": "uint8",
            "count": 1,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "compress": "zstd",
            "zstd_level": 9,
            "nodata": 0,
            "bigtiff": "YES",
            "num_threads": "ALL_CPUS"
        })

        with rasterio.open(output_path, "w", **meta) as dst:
            total_chunks = (height + chunk_size - 1) // chunk_size
            for chunk_idx, y_start in enumerate(range(0, height, chunk_size)):
                actual_chunk_height = min(chunk_size, height - y_start)
                window = Window(0, y_start, width, actual_chunk_height)
                chunk_data = src.read(1, window=window)
                dst.write(chunk_data, 1, window=window)"""
    add_code_block(doc, code_kba_seamless, caption="create_seamless_kba_kva.py (Mozaik Zstandard UInt8)")

    # 6.3
    doc.add_heading("6.3 Skrip Tahap 3: Kalkulasi Paralel Multi-Core 6 Indikator JLH (calculate_jlh_sumbar_2025.py)", level=2)
    doc.add_paragraph(
        "Tahap ketiga adalah komputasi inti integrasi matematis KBA, KVA, dan PL. Komputasi dijalankan secara paralel "
        "memanfaatkan 16 CPU Core menggunakan Python multiprocessing.Pool. Dua inovasi kunci yang diterapkan:\n"
        "1. NumPy 1D Remap Table: Skor PL, KBA, dan KVA disimpan dalam array 1D berukuran 256 elemen. Operasi klasifikasi ulang "
        "dieksekusi instan melalui indeks array NumPy (pl_remap[k][pl_data]), memproses 63 juta piksel per tile hanya dalam hitungan milidetik.\n"
        "2. Predictor Floating Point 3 & Deflate: Hasil 6 band disimpan dalam 1 file multi-band Float32 dengan kompresi Deflate Predictor 3:"
    )

    code_calc_jlh = """# ==============================================================================
# KOMPUTASI MULTI-CORE PARALEL 6 INDIKATOR JLH PER TILE GRID
# File: calculate_jlh_sumbar_2025.py
# ==============================================================================
import os, multiprocessing as mp
import numpy as np
import rasterio
from rasterio.windows import from_bounds
import openpyxl

JLH_CONFIG = {
    'pga': {'name': 'Pengaturan Air',             'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'phk': {'name': 'Pendukung Habitat & Kehati', 'w_kba': 0.24, 'w_kva': 0.16, 'w_pl': 0.60},
    'ppk': {'name': 'Penyerap & Simpan Karbon',   'w_kba': 0.20, 'w_kva': 0.20, 'w_pl': 0.60},
    'pya': {'name': 'Penyedia Air',               'w_kba': 0.32, 'w_kva': 0.08, 'w_pl': 0.60},
    'pgn': {'name': 'Penyedia Pangan (Sumatera)', 'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'pku': {'name': 'Pengatur Kualitas Udara',    'w_kba': 0.15, 'w_kva': 0.25, 'w_pl': 0.60}
}
JLH_KEYS = list(JLH_CONFIG.keys())

def process_tile_task(task_args):
    kba_path, kva_path, out_path = task_args
    if os.path.exists(out_path):
        return 'skip'

    global worker_src_pl, shared_remap
    pl_remap = shared_remap['pl']
    kba_remap = shared_remap['kba']
    kva_remap = shared_remap['kva']

    with rasterio.open(kba_path) as src_kba, rasterio.open(kva_path) as src_kva:
        kba_data = src_kba.read(1)
        kva_data = src_kva.read(1)
        bounds = src_kba.bounds
        h, w = src_kba.height, src_kba.width
        prof = src_kba.profile.copy()

    # Windowed read dari Master Raster LULC 2025
    win_pl = from_bounds(*bounds, transform=worker_src_pl.transform)
    pl_data = worker_src_pl.read(1, window=win_pl, out_shape=(h, w), boundless=True, fill_value=0)

    nodata_mask = (pl_data == 0) | (pl_data == 255)

    # Lewati jika tile seluruhnya berada di laut lepas
    if np.all(nodata_mask) and np.all(kba_data == 0) and np.all(kva_data == 0):
        return 'empty'

    # Kalkulasi 6 Band JLH Secara Vektorisasi
    jlh_result = np.zeros((6, h, w), dtype=np.float32)
    for idx, k in enumerate(JLH_KEYS):
        cfg = JLH_CONFIG[k]
        sk_kba = kba_remap[k][kba_data]
        sk_kva = kva_remap[k][kva_data]
        sk_pl = pl_remap[k][pl_data]

        band = (sk_kba * cfg['w_kba']) + (sk_kva * cfg['w_kva']) + (sk_pl * cfg['w_pl'])
        band[nodata_mask] = 0.0
        jlh_result[idx] = band

    prof.update({
        'count': 6, 'dtype': 'float32', 'nodata': 0.0,
        'compress': 'deflate', 'predictor': 3,
        'tiled': True, 'blockxsize': 512, 'blockysize': 512
    })

    with rasterio.open(out_path, 'w', **prof) as dst:
        dst.write(jlh_result)
        for b_idx, k in enumerate(JLH_KEYS, 1):
            dst.set_band_description(b_idx, f"JLH_{k.upper()}_{JLH_CONFIG[k]['name']}")

    return 'processed'"""
    add_code_block(doc, code_calc_jlh, caption="calculate_jlh_sumbar_2025.py (Kalkulasi 6 Band Paralel)")

    # 6.4
    doc.add_heading("6.4 Skrip Tahap 4: Mozaik Virtual Raster (VRT) & Ekspor LERC_ZSTD Chunking (create_seamless_jlh_lerc.py)", level=2)
    doc.add_paragraph(
        "Ribuan tile multi-band kemudian dipecah ke dalam VRT per indikator tunggal, lalu digabungkan menjadi file seamless utuh "
        "berformat GeoTIFF LERC_ZSTD. Algoritma Limited Error Raster Compression (LERC) dikombinasikan dengan Zstandard "
        "mempertahankan presisi floating-point dengan batas toleransi eror max_z_error=0.005, mereduksi ukuran file hingga 97%:"
    )

    code_lerc_export = """# ==============================================================================
# EKSPOR MOZAIK SEAMLESS 1-LAYER PER INDIKATOR DENGAN LERC_ZSTD
# File: create_seamless_jlh_lerc.py
# ==============================================================================
import rasterio
from rasterio.windows import Window
import numpy as np

def export_seamless_lerc_zstd(input_vrt_path, output_tif_path, chunk_rows=4096):
    with rasterio.open(input_vrt_path) as src:
        profile = src.profile.copy()
        width, height = src.width, src.height
        
        profile.update({
            'driver': 'GTiff',
            'dtype': 'float32',
            'nodata': 0.0,
            'compress': 'lerc_zstd',
            'max_z_error': 0.005,
            'tiled': True,
            'blockxsize': 512,
            'blockysize': 512,
            'bigtiff': 'YES',
            'num_threads': 'all_cpus'
        })

        num_chunks = (height + chunk_rows - 1) // chunk_rows
        with rasterio.open(output_tif_path, 'w', **profile) as dst:
            for c in range(num_chunks):
                r_start = c * chunk_rows
                curr_h = min(chunk_rows, height - r_start)
                win = Window(0, r_start, width, curr_h)

                chunk_data = src.read(1, window=win)
                dst.write(chunk_data, 1, window=win)"""
    add_code_block(doc, code_lerc_export, caption="create_seamless_jlh_lerc.py (Ekspor LERC_ZSTD Chunking)")

    # 6.5
    doc.add_heading("6.5 Skrip Tahap 5: Penyesuaian Legal Kriteria Khusus pada Layer PHK (apply_kk_phk.py)", level=2)
    doc.add_paragraph(
        "Pada indikator Pendukung Habitat & Keanekaragaman Hayati (PHK), dilakukan penyesuaian berbasis mandat kawasan konservasi "
        "dan koridor ekologis bernilai konservasi tinggi (KK.gpkg):\n"
        "• Kriteria Khusus 1 (KK 1): Kawasan konservasi inti (Cagar Alam, Suaka Margasatwa, Taman Nasional) dipaksa bernilai mutlak 5.0.\n"
        "• Kriteria Khusus 2 & 3 (KK 2/3): Zona penyangga ekologis dipaksa bernilai minimal 4.0 jika nilai aslinya di bawah 4.0.\n"
        "• Area di luar poligon KK mempertahankan nilai asli hasil perpaduan KBA, KVA, dan PL:"
    )

    code_kk = """# ==============================================================================
# PENYESUAIAN KRITERIA KHUSUS PADA LAYER PHK
# File: apply_kk_phk.py
# ==============================================================================
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np

def apply_kriteria_khusus(input_phk_tif, kk_gpkg_path, output_phk_kk_tif):
    gdf = gpd.read_file(kk_gpkg_path)
    gdf_kk1 = gdf[gdf['KK_PHK25'] == 'Kriteria Khusus 1']
    gdf_kk23 = gdf[gdf['KK_PHK25'].isin(['Kriteria Khusus 2', 'Kriteria Khusus 3'])]

    with rasterio.open(input_phk_tif) as src:
        meta = src.meta.copy()
        phk_data = src.read(1)
        transform = src.transform
        shape = phk_data.shape

        mask_kk1 = rasterize([(geom, 1) for geom in gdf_kk1.geometry], out_shape=shape, transform=transform, default_value=0, dtype=np.uint8)
        mask_kk23 = rasterize([(geom, 1) for geom in gdf_kk23.geometry], out_shape=shape, transform=transform, default_value=0, dtype=np.uint8)

        phk_adjusted = np.where(mask_kk1 == 1, 5.0, phk_data)
        phk_adjusted = np.where((mask_kk23 == 1) & (phk_adjusted < 4.0), 4.0, phk_adjusted)

        with rasterio.open(output_phk_kk_tif, 'w', **meta) as dst:
            dst.write(phk_adjusted, 1)"""
    add_code_block(doc, code_kk, caption="apply_kk_phk.py (Integrasi Kriteria Khusus Konservasi)")

    # 6.6
    doc.add_heading("6.6 Skrip Tahap 6: Pembentukan Piramida Resolusi Spasial (Internal Overviews)", level=2)
    doc.add_paragraph(
        "Untuk menjamin file raster berukuran raksasa dapat dibuka dan di-zoom secara instan di QGIS maupun aplikasi WebGIS "
        "tanpa rendering lag, dibuat piramida resolusi internal bertingkat (overviews) faktor 2, 4, 8, 16, 32, 64, dan 128:"
    )

    code_ovr = """# ==============================================================================
# PEMBUATAN INTERNAL OVERVIEWS PADA GEOTIFF SEAMLESS
# ==============================================================================
import rasterio
from rasterio.enums import Resampling

def build_pyramid_overviews(tif_path):
    with rasterio.open(tif_path, 'r+') as dst:
        factors = [2, 4, 8, 16, 32, 64, 128]
        dst.build_overviews(factors, Resampling.nearest)
        dst.update_tags(ns='rio_overview', resampling='nearest')
    print(f"Piramida overviews berhasil dibangun untuk: {tif_path}")"""
    add_code_block(doc, code_ovr, caption="Membangun Piramida Resolusi (Overviews)")

    # =========================================================================
    # BAB 7: METODE PEMETAAN & PENGGABUNGAN JASA LINGKUNGAN HIDUP TINGGI (JLHT)
    # =========================================================================
    h7_jlht = doc.add_heading("7. Metode Pemetaan dan Penggabungan Jasa Lingkungan Hidup Tinggi (JLH Tinggi: Kategori A, B, dan C)", level=1)
    h7_jlht.paragraph_format.space_before = Pt(14)
    h7_jlht.paragraph_format.space_after = Pt(4)
    h7_jlht.style.font.name = "Arial"
    h7_jlht.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_heading("7.1 Konsep Dasar dan Pemilihan 3 Indikator Kunci JLH Tinggi", level=2)
    doc.add_paragraph(
        "Dalam pedoman KLH/BPLH mengenai Pemetaan Jasa Lingkungan Hidup Tinggi (JLH Tinggi), evaluasi difokuskan pada "
        "tiga fungsi ekosistem penyangga kehidupan paling krusial yang merepresentasikan keseimbangan hidrologis, "
        "keanekaragaman hayati, dan mitigasi perubahan iklim:\n"
        "1. JLH Pengatur Air (PGA): Kemampuan ekosistem mengatur tata air, infiltrasi, dan pengendalian limpasan.\n"
        "2. JLH Pendukung Habitat & Keanekaragaman Hayati (PHK): Kemampuan bentang alam mendukung kelangsungan hidup biota dan genetik.\n"
        "3. JLH Penyerap & Penyimpan Karbon (PPK): Kapasitas biomassa dan tanah dalam menyerap serta menyimpan cadangan karbon.\n\n"
        "Suatu piksel (berukuran 0.5m x 0.5m) dinyatakan memiliki Jasa Lingkungan Hidup Tinggi pada masing-masing indikator apabila "
        "memiliki skor indeks >= 4.20 (masuk dalam rentang kelas Sangat Tinggi: 4.20 - 5.00)."
    )

    doc.add_heading("7.2 Tantangan Penggabungan Konvensional vs Solusi Pengkodean Bitwise Hierarkis", level=2)
    doc.add_paragraph(
        "Secara konseptual, klasifikasi JLH Tinggi dibagi menjadi tiga kategori utama:\n"
        "• Kategori A: Piksel yang memiliki nilai tinggi (>= 4.2) pada ketiga JLH sekaligus (PGA, PHK, dan PPK).\n"
        "• Kategori B: Piksel yang memiliki nilai tinggi (>= 4.2) pada salah dua dari ketiga JLH tersebut.\n"
        "• Kategori C: Piksel yang memiliki nilai tinggi (>= 4.2) pada salah satu dari ketiga JLH tersebut.\n\n"
        "Apabila penggabungan dilakukan secara naif hanya dengan menjumlahkan jumlah indikator yang lolos ambang batas "
        "(Count = 3 -> A, Count = 2 -> B, Count = 1 -> C), maka terjadi kehilangan informasi (information loss) pada Kategori B dan C: "
        "pengguna peta tidak dapat lagi mengetahui JLH mana yang menyusun nilai B atau C pada suatu lokasi.\n\n"
        "Untuk mengatasi hal tersebut, diterapkan algoritma Kombinatorika Aljabar Bitwise 3-Bit (Bitmask Encoding) yang dipetakan ke "
        "Skema Kode Hierarkis 2-Digit (UInt8). Pendekatan ini bekerja dalam 3 tahap matematis:"
    )

    steps_jlht = [
        ("Tahap 1 — Binarisasi Ambang Batas (Thresholding >= 4.2): ",
         "Setiap layer diubah menjadi matriks biner (1 jika nilai >= 4.2, dan 0 jika nilai < 4.2):\n"
         "  b_PGA = (PGA >= 4.2)  |  b_PHK = (PHK >= 4.2)  |  b_PPK = (PPK >= 4.2)"),
        ("Tahap 2 — Penyusunan Indeks Bitwise 3-Bit (Bitmask 0 s.d. 7): ",
         "Ketiga matriks biner digabungkan menggunakan bobot posisi biner 2^2 (4), 2^1 (2), dan 2^0 (1):\n"
         "  Bitmask = (4 x b_PGA) + (2 x b_PHK) + (1 x b_PPK)\n"
         "Setiap kombinasi irisan pada Diagram Venn menghasilkan angka unik 0 s.d. 7 tanpa ada tumpang tindih."),
        ("Tahap 3 — Pemetaan ke Kode Hierarkis 2-Digit (Dual-Level Readability): ",
         "Nilai Bitmask (0..7) dipetakan ke kode integer 2-digit di mana:\n"
         "  • Digit Puluhan menunjukkan Kategori Utama: 1 = Kategori A, 2 = Kategori B, 3 = Kategori C.\n"
         "  • Digit Satuan menunjukkan Sub-Kombinasi Penyusun Spesifik: B1 (21), B2 (22), B3 (23) serta C1 (31), C2 (32), C3 (33).")
    ]
    for st_title, st_desc in steps_jlht:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(2)
        pb.paragraph_format.space_after = Pt(3)
        r_st = pb.add_run(st_title)
        r_st.bold = True
        r_st.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(st_desc)

    doc.add_heading("7.3 Tabel Matriks Kebenaran (Truth Table) dan Standar Simbologi Diagram Venn", level=2)
    doc.add_paragraph(
        "Tabel berikut menyajikan matriks kebenaran lengkap penggabungan PGA, PHK, dan PPK beserta kode piksel, sub-kelas, "
        "komponen penyusun, dan kode warna standar sesuai pedoman KLH/BPLH:"
    )

    jlht_rows = [
        ("1", "1", "1", "7 (111)", "10", "A", "Kategori A (3 JLH)", "JLH Tinggi Pengatur Air, Kehati & Karbon", "Coklat (#9A7029)"),
        ("1", "1", "0", "6 (110)", "21", "B1", "Kategori B (2 JLH)", "JLH Tinggi Pengatur Air & Kehati", "Biru Muda (#63C5DA)"),
        ("0", "1", "1", "3 (011)", "22", "B2", "Kategori B (2 JLH)", "JLH Tinggi Kehati & Karbon", "Kuning (#F2EA3B)"),
        ("1", "0", "1", "5 (101)", "23", "B3", "Kategori B (2 JLH)", "JLH Tinggi Pengatur Air & Karbon", "Ungu (#AE529A)"),
        ("1", "0", "0", "4 (100)", "31", "C1", "Kategori C (1 JLH)", "JLH Tinggi Pengatur Air", "Biru Tua (#305496)"),
        ("0", "1", "0", "2 (010)", "32", "C2", "Kategori C (1 JLH)", "JLH Tinggi Pendukung Habitat & Kehati", "Hijau (#54B948)"),
        ("0", "0", "1", "1 (001)", "33", "C3", "Kategori C (1 JLH)", "JLH Tinggi Penyerap & Penyimpan Karbon", "Merah (#ED1C24)"),
        ("0", "0", "0", "0 (000)", "0", "Non-JLHT", "Bukan JLH Tinggi", "Ketiga JLH bernilai < 4.2", "Abu-abu (#E2E8F0)")
    ]

    tbl_jlht = doc.add_table(rows=len(jlht_rows)+1, cols=9)
    tbl_jlht.alignment = WD_TABLE_ALIGNMENT.CENTER
    jlht_headers = ["PGA >=4.2", "PHK >=4.2", "PPK >=4.2", "Bitmask", "Kode Piksel", "Sub-Kelas", "Kategori Utama", "Komponen Penyusun JLH Tinggi", "Warna Standar"]
    for j, h in enumerate(jlht_headers):
        cell = tbl_jlht.cell(0, j)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=70, right=70)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row in enumerate(jlht_rows, start=1):
        bg_col = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = tbl_jlht.cell(i, j)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=55, bottom=55, left=70, right=70)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if j in (4, 5):
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    set_table_borders(tbl_jlht, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_heading("7.4 Cara Membaca Penyusun Spesifik (B1–B3, C1–C3) dan Kategori Utama (A, B, C)", level=2)
    doc.add_paragraph(
        "Dengan desain kode hierarkis 2-digit dan penyematan metadata GDAL Raster Attribute Table (.tif.aux.xml) serta QGIS Style (.qml), "
        "file raster JLH Tinggi memberikan fleksibilitas pembacaan ganda:\n"
        "1. Membaca Komponen Penyusun secara Langsung di QGIS/ArcGIS: Saat file sumbar_2025_jlh_tinggi_seamless.tif dimuat ke QGIS, "
        "tabel atribut dan legenda otomatis menampilkan 7 kelas (A, B1, B2, B3, C1, C2, C3) lengkap dengan deskripsi penyusunnya "
        "(misalnya B1 = Pengatur Air & Kehati, B2 = Kehati & Karbon, B3 = Pengatur Air & Karbon).\n"
        "2. Membaca Ringkasan Kategori A, B, dan C dengan Operasi Pembagian Bulat: Jika analis ingin mengekstrak hanya Kategori A, B, atau C "
        "di Raster Calculator, cukup gunakan rumus pembagian bulat (integer division) dengan angka 10:\n"
        "   • Kategori_Utama = Int(JLH_Tinggi / 10)\n"
        "   Hasilnya: nilai 1 = Kategori A (semua 3 JLH), nilai 2 = Kategori B (salah 2 JLH), dan nilai 3 = Kategori C (salah 1 JLH)."
    )

    doc.add_heading("7.5 Skrip Implementasi Penggabungan JLH Tinggi (calculate_jlh_tinggi_sumbar.py)", level=2)
    code_jlht_script = """# ==============================================================================
# PENGGABUNGAN JLH TINGGI (PGA, PHK, PPK >= 4.2) DENGAN BITMASK & KODE 2-DIGIT
# File: calculate_jlh_tinggi_sumbar.py
# ==============================================================================
import numpy as np
import rasterio
from rasterio.windows import Window

THRESHOLD_TINGGI = 4.2

# Pemetaan indeks Bitmask (4*PGA + 2*PHK + 1*PPK) ke Kode Hierarkis 2-Digit:
# 0(000)->0, 1(001)->33(C3), 2(010)->32(C2), 3(011)->22(B2),
# 4(100)->31(C1), 5(101)->23(B3), 6(110)->21(B1), 7(111)->10(A)
BITMASK_TO_CODE = np.array([0, 33, 32, 22, 31, 23, 21, 10], dtype=np.uint8)

def compute_jlh_tinggi_chunk(pga_arr, phk_arr, ppk_arr, threshold=4.2):
    valid_mask = (pga_arr > 0) & (~np.isnan(pga_arr))

    b_pga = (pga_arr >= threshold).astype(np.uint8)
    b_phk = (phk_arr >= threshold).astype(np.uint8)
    b_ppk = (ppk_arr >= threshold).astype(np.uint8)

    # Bitwise combination: 4*PGA + 2*PHK + 1*PPK (menghasilkan 0..7)
    bitmask = (b_pga << 2) | (b_phk << 1) | b_ppk

    # Reklasifikasi cepat via NumPy fancy indexing ke kode 10, 21..23, 31..33, 0
    out_code = BITMASK_TO_CODE[bitmask]
    out_code[~valid_mask] = 255  # NoData untuk laut / luar area
    return out_code"""
    add_code_block(doc, code_jlht_script, caption="calculate_jlh_tinggi_sumbar.py (Kombinasi Bitwise JLH Tinggi)")

    doc.add_heading("7.6 Hasil Rekapitulasi Luasan JLH Tinggi Provinsi Sumatera Barat (Resolusi 0.5 Meter)", level=2)
    doc.add_paragraph(
        "Berdasarkan hasil pemrosesan penuh atas layer PGA (sumbar_2025_jlh_pga_seamless.tif), PHK terintegrasi Kawasan Konservasi "
        "(sumbar_2025_jlh_phk_kk_seamless.tif), dan PPK (sumbar_2025_jlh_ppk_seamless.tif) dengan ambang batas >= 4.20, "
        "diperoleh distribusi luasan masing-masing sub-kelas dan kategori utama sebagai berikut:"
    )

    jlht_stat_rows = [
        ("10", "A", "Kategori A (3 JLH Tinggi)", "PGA + PHK_KK + PPK", "1.653.253,12", "38,56%"),
        ("21", "B1", "Kategori B (2 JLH Tinggi)", "PGA + PHK_KK", "98.330,58", "2,29%"),
        ("22", "B2", "Kategori B (2 JLH Tinggi)", "PHK_KK + PPK", "423.286,91", "9,87%"),
        ("23", "B3", "Kategori B (2 JLH Tinggi)", "PGA + PPK", "258.136,40", "6,02%"),
        ("—", "Subtotal B", "Total Kategori B (B1 + B2 + B3)", "Salah 2 JLH Tinggi", "779.753,89", "18,19%"),
        ("31", "C1", "Kategori C (1 JLH Tinggi)", "PGA saja", "53.556,14", "1,25%"),
        ("32", "C2", "Kategori C (1 JLH Tinggi)", "PHK_KK saja", "60.715,18", "1,42%"),
        ("33", "C3", "Kategori C (1 JLH Tinggi)", "PPK saja", "93.559,83", "2,18%"),
        ("—", "Subtotal C", "Total Kategori C (C1 + C2 + C3)", "Salah 1 JLH Tinggi", "207.831,15", "4,85%"),
        ("10–33", "TOTAL JLHT", "Total JLH Tinggi (A + B + C)", "Minimal 1 JLH >= 4.2", "2.640.838,16", "61,59%"),
        ("1", "Non-JLHT", "Di Luar JLH Tinggi", "Ketiga JLH < 4.2", "1.646.875,67", "38,41%"),
        ("—", "TOTAL DARATAN", "Total Daratan Valid", "Seluruh Daratan", "4.287.713,83", "100,00%")
    ]

    tbl_stat = doc.add_table(rows=len(jlht_stat_rows)+1, cols=6)
    tbl_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    stat_headers = ["Kode Piksel", "Sub-Kelas", "Kategori Utama", "Penyusun JLH (>= 4.2)", "Luas (Hektar)", "Proporsi (%)"]
    for j, h in enumerate(stat_headers):
        cell = tbl_stat.cell(0, j)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row in enumerate(jlht_stat_rows, start=1):
        is_summary = row[1] in ("Subtotal B", "Subtotal C", "TOTAL JLHT", "TOTAL DARATAN")
        bg_col = "E2E8F0" if is_summary else ("F8FAFC" if i % 2 == 1 else "FFFFFF")
        for j, val in enumerate(row):
            cell = tbl_stat.cell(i, j)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=55, bottom=55, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if is_summary or j in (1, 4, 5):
                r.font.bold = True
                if is_summary:
                    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    set_table_borders(tbl_stat, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # BAB 8
    # =========================================================================
    h7 = doc.add_heading("8. Spesifikasi Teknis Produk Akhir Raster Seamless Se-Sumatera Barat", level=1)
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(4)
    h7.style.font.name = "Arial"
    h7.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Seluruh rangkaian pipeline komputasi menghasilkan 10 file master raster seamless se-Provinsi Sumatera Barat "
        "yang tersimpan di direktori kerja dan server Kementerian Lingkungan Hidup / BPLH:"
    )

    prod_files = [
        ("sumbar_2025_jlh_pga_seamless.tif", "403 MB", "Float32 (1.0–5.0)", "LERC_ZSTD", "JLH Pengaturan Air (Water Regulation)"),
        ("sumbar_2025_jlh_phk_seamless.tif", "362 MB", "Float32 (1.0–5.0)", "LERC_ZSTD", "JLH Pendukung Habitat & Kehati (Alami)"),
        ("sumbar_2025_jlh_phk_kk_seamless.tif", "375 MB", "Float32 (1.0–5.0)", "LERC_ZSTD", "JLH Habitat & Kehati dengan Penyesuaian Kriteria Khusus"),
        ("sumbar_2025_jlh_ppk_seamless.tif", "307 MB", "Float32 (1.0–5.0)", "LERC_ZSTD", "JLH Penyerap & Penyimpan Karbon (Carbon Storage)"),
        ("sumbar_2025_jlh_pya_seamless.tif", "360 MB", "Float32 (1.0–5.0)", "LERC_ZSTD", "JLH Penyedia Air Bersih (Water Provisioning)"),
        ("sumbar_2025_jlh_pgn_seamless.tif", "342 MB", "Float32 (1.0–5.0)", "LERC_ZSTD", "JLH Penyedia Pangan (Food Provisioning)"),
        ("sumbar_2025_jlh_pku_seamless.tif", "427 MB", "Float32 (1.0–5.0)", "LERC_ZSTD", "JLH Pengatur Kualitas Udara (Air Quality)"),
        ("sumbar_2025_jlh_tinggi_seamless.tif", "1,6 GB", "UInt8 (Kode 10, 21–33)", "DEFLATE + RAT", "JLH Tinggi Gabungan (PGA, PHK+KK, PPK >= 4.2)"),
        ("sumbar_2025_kba_seamless.tif", "178 MB", "UInt8 (1–255)", "Zstandard L9", "Master Karakteristik Bentang Alam Se-Sumbar"),
        ("sumbar_2025_kva_seamless.tif", "169 MB", "UInt8 (1–255)", "Zstandard L9", "Master Karakteristik Vegetasi Alami Se-Sumbar")
    ]
    tbl_p = doc.add_table(rows=len(prod_files)+1, cols=5)
    tbl_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Nama File Master", "Ukuran File", "Tipe Data", "Kompresi", "Deskripsi Lapisan"]):
        cell = tbl_p.cell(0, j)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, row in enumerate(prod_files, start=1):
        bg_col = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = tbl_p.cell(i, j)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    set_table_borders(tbl_p, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # BAB 9
    # =========================================================================
    h8 = doc.add_heading("9. Panduan Standard Operating Procedure (SOP) Analisis & Visualisasi di QGIS / ArcGIS", level=1)
    h8.paragraph_format.space_before = Pt(14)
    h8.paragraph_format.space_after = Pt(4)
    h8.style.font.name = "Arial"
    h8.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Untuk memastikan pengguna data (analis SIG, perencana tata ruang, dan akademisi) dapat membuka dan memvisualisasikan "
        "lapisan data JLH secara konsisten dan terstandardisasi, berikut adalah prosedur operasional standar di perangkat lunak SIG:"
    )

    sops = [
        ("Langkah 1: Menambahkan Layer Raster ke Kanvas Peta: ", 
         "Seret (drag-and-drop) file sumbar_2025_jlh_*_seamless.tif langsung ke panel Layers QGIS atau Add Data pada ArcGIS Pro."),
        ("Langkah 2: Konfigurasi Nilai NoData (Transparansi Laut): ", 
         "Klik kanan layer > Properties > tab Transparency. Pastikan nilai 'Additional no data value' diisi '0' (untuk JLH individu) "
         "atau '255' (untuk JLH Tinggi gabungan). Ini membuat area laut menjadi transparan sempurna."),
        ("Langkah 3: Pengaturan Simbologi Warna (Pseudocolor / Paletted): ", 
         "Untuk JLH individu, gunakan 'Singleband pseudocolor' (Min=1.0, Max=5.0). Untuk JLH Tinggi gabungan, cukup muat file style "
         "sumbar_2025_jlh_tinggi_seamless.qml agar warna Diagram Venn (A, B1, B2, B3, C1, C2, C3) otomatis diterapkan."),
        ("Langkah 4: Penetapan Batas Rentang Nilai (Min / Max): ", 
         "Atur Min = 1.0 (Layanan Sangat Rendah) dan Max = 5.0 (Layanan Sangat Tinggi)."),
        ("Langkah 5: Klasifikasi 5 Kelas Daya Dukung Lingkungan: ", 
         "Gunakan mode 'Equal Interval' dengan 5 kelas standar kementerian:\n"
         "  • 1.00 - 1.80 : Sangat Rendah (Merah / Coklat Terang)\n"
         "  • 1.81 - 2.60 : Rendah (Oranye)\n"
         "  • 2.61 - 3.40 : Sedang (Kuning)\n"
         "  • 3.41 - 4.20 : Tinggi (Hijau Muda)\n"
         "  • 4.21 - 5.00 : Sangat Tinggi (Hijau Tua Konservasi)")
    ]
    for stitle, sdesc in sops:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(2)
        pb.paragraph_format.space_after = Pt(2)
        r_st = pb.add_run(stitle)
        r_st.bold = True
        r_st.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(sdesc)

    # =========================================================================
    # BAB 10
    # =========================================================================
    h9 = doc.add_heading("10. Ringkasan & Rekomendasi Pemeliharaan Data Geospasial", level=1)
    h9.paragraph_format.space_before = Pt(14)
    h9.paragraph_format.space_after = Pt(4)
    h9.style.font.name = "Arial"
    h9.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Penyusunan basis data Jasa Lingkungan Hidup (JLH) Provinsi Sumatera Barat resolusi 0.5 meter seamless ini "
        "menjadi tonggak penting transformasi tata kelola lingkungan hidup berbasis bukti saintifik (evidence-based policy). "
        "Beberapa rekomendasi pemeliharaan dan pemanfaatan data ke depan:"
    )

    recs = [
        ("Pembaruan Berkala Komponen Penutupan Lahan (PL): ", 
         "Karena KBA dan KVA bersifat permanen dalam jangka panjang, pembaruan JLH di masa mendatang cukup memperbarui lapisan Penutupan Lahan (PL) "
         "tahunan atau lima tahunan, kemudian menjalankan ulang skrip kalkulasi otomatis."),
        ("Integrasi ke Sistem Informasi Geospasial Daerah (Simtaru / WebGIS BPLH): ", 
         "File raster LERC_ZSTD yang telah dilengkapi overviews siap dipublikasikan via Map Server (GeoServer / Cloud Optimized GeoTIFF TiTiler) "
         "sehingga dapat diakses secara publik dan lintas sektor oleh seluruh OPD di Sumatera Barat."),
        ("Pemanfaatan Multisektoral: ", 
         "Data ini sangat direkomendasikan menjadi rujukan wajib dalam revisi RTRW Provinsi/Kabupaten/Kota, penetapan Nilai Ekonomi Karbon (NEK), "
         "analisis dampak lingkungan (AMDAL), serta perizinan pemanfaatan kawasan hutan.")
    ]
    for rtitle, rdesc in recs:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(2)
        pb.paragraph_format.space_after = Pt(2)
        r_rt = pb.add_run(rtitle)
        r_rt.bold = True
        r_rt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(rdesc)

    # Signature / Closing
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(16)
    p_close.paragraph_format.space_after = Pt(4)
    r_c = p_close.add_run(
        "Dokumen ini disusun sebagai pedoman resmi dan repositori kode sumber komputasi pemodelan "
        "Jasa Lingkungan Hidup (JLH) Provinsi Sumatera Barat tahun 2025–2026."
    )
    r_c.font.italic = True
    r_c.font.size = Pt(9.5)
    r_c.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    output_filename = "Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.docx"
    doc.save(output_filename)
    print(f"File dokumen Word JLH berhasil diperbarui dan disimpan: {output_filename}")

if __name__ == "__main__":
    build_detailed_jlh_doc()
