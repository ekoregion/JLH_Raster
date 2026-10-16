import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    # Remove existing shading if any
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

def add_callout(doc, text, title="CATATAN PENTING / METODOLOGI:"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    # Left thick border
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
        cp.paragraph_format.space_before = Pt(6)
        cp.paragraph_format.space_after = Pt(2)
        r_cap = cp.add_run(f"Skrip: {caption}")
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
        f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="4A6984"/>'
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
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def create_document():
    doc = docx.Document()
    
    # Page Setup - Margins 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # COVER / HEADER TITLE
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("KEMENTERIAN LINGKUNGAN HIDUP / BADAN PENGENDALIAN LINGKUNGAN HIDUP (BPLH)\nDIREKTORAT PENYELENGGARAAN SUMBER DAYA ALAM BERKELANJUTAN")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("DOKUMENTASI LENGKAP METODOLOGI & SKRIP PEMODELAN JASA LINGKUNGAN HIDUP (JLH)")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Provinsi Sumatera Barat (Tahun Analisis: 2025–2026)\nTransformasi Spasial KBA, KVA, dan PL Multiskala Berbasis Cloud Computing Resolusi Ultra-Tinggi (0.5 Meter Seamless) Serta Hilirisasi MCE Ruang Hidup Pasca-Bencana")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x69, 0x84)

    # Metadata Box
    meta_tbl = doc.add_table(rows=1, cols=1)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = meta_tbl.cell(0, 0)
    set_cell_background(c, "F4F6F9")
    set_cell_margins(c, top=100, bottom=100, left=150, right=150)
    set_table_borders(meta_tbl, color="CBD5E1", sz="6")
    p_m = c.paragraphs[0]
    p_m.paragraph_format.line_spacing = 1.15
    p_m.paragraph_format.space_after = Pt(0)
    p_m.add_run("• Resolusi Spasial Grid: ").bold = True
    p_m.add_run("0.5 Meter (Ultra-High Resolution Seamless) & 10 Meter (Quick View)\n")
    p_m.add_run("• Sistem Proyeksi (CRS): ").bold = True
    p_m.add_run("EPSG:3857 (WGS 84 / Pseudo-Mercator)\n")
    p_m.add_run("• Kompresi Raster: ").bold = True
    p_m.add_run("LERC_ZSTD (Lossless-Floating Max Error 0.005, Menghemat Disk hingga 97%)\n")
    p_m.add_run("• Jumlah Tile Tutupan Lahan: ").bold = True
    p_m.add_run("~2.300+ Grid Tile Citra Satelit Resolusi Tinggi Tahun 2025\n")
    p_m.add_run("• Tanggal Efektif: ").bold = True
    p_m.add_run("Oktober 2026")
    for r in p_m.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # DAFTAR ISI
    # -------------------------------------------------------------
    h_toc = doc.add_heading("DAFTAR ISI", level=1)
    h_toc.paragraph_format.space_before = Pt(14)
    h_toc.paragraph_format.space_after = Pt(4)
    h_toc.style.font.name = "Arial"
    h_toc.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    toc_items = [
        "1. Latar Belakang & Kerangka Konseptual JLH",
        "2. Tiga Pilar Komponen Input JLH (KBA, KVA, dan PL 2025)",
        "3. Formulasi Matematis & Bobot 6 Indikator JLH Regional Sumatera",
        "4. Tabel Matriks Skor Penutupan Lahan (PL Lookup Table 15 Kelas)",
        "5. Skrip Python: Transformasi & Kalkulasi JLH Grid 0.5m (Anti-OOM)",
        "6. Skrip Python: Mozaik Seamless Se-Sumatera Barat & Kompresi LERC_ZSTD",
        "7. Penyesuaian Kriteria Khusus (KK.gpkg) pada Layer PHK",
        "8. Hilirisasi Analisis: Pemodelan Spasial JLH Ruang Hidup (Relokasi Huntap/Huntara)",
        "9. Petunjuk Operasional & Visualisasi Data di QGIS",
        "10. Spesifikasi Teknis Server & Ringkasan File Produk"
    ]
    for item in toc_items:
        p_ti = doc.add_paragraph()
        p_ti.paragraph_format.space_before = Pt(1)
        p_ti.paragraph_format.space_after = Pt(1)
        r = p_ti.add_run(item)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # BAB 1
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Latar Belakang & Kerangka Konseptual JLH", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(4)
    h1.style.font.name = "Arial"
    h1.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p1 = doc.add_paragraph(
        "Jasa Lingkungan Hidup (JLH) atau Ecosystem Services merupakan seluruh manfaat langsung maupun tidak langsung "
        "yang diperoleh manusia dari berfungsinya ekosistem alami dan bentang alam secara lestari. Pemodelan spasial JLH "
        "Provinsi Sumatera Barat disusun untuk menyediakan basis data geospasial beresolusi sangat detail (0.5 meter seamless) "
        "guna mendukung kebijakan strategis pemerintah, di antaranya:"
    )
    
    b_items1 = [
        ("Rencana Perlindungan dan Pengelolaan Lingkungan Hidup (RPPLH): ", "Sebagai dasar ilmiah penetapan zona perlindungan dan pemanfaatan sumber daya alam."),
        ("Daya Dukung & Daya Tampung Lingkungan Hidup (D3TLH): ", "Menghitung kapasitas maksimum lanskap dalam menyerap dampak aktivitas pembangunan dan permukiman."),
        ("Mitigasi Bencana & Lokasi Relokasi (Huntap/Huntara): ", "Menyediakan arahan spasial yang aman dari ancaman bencana hidrometeorologi (longsor, banjir bandang/galodo, banjir genangan) sekaligus menjamin ketersediaan air bersih dan ketahanan pangan.")
    ]
    for b_title, b_desc in b_items1:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_bt = pb.add_run(b_title)
        r_bt.bold = True
        r_bt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(b_desc)

    doc.add_paragraph(
        "Pemodelan ini mengevaluasi 6 Indikator Layanan Ekosistem Prioritas:"
    )
    indicators = [
        ("PGA (Pengaturan Air): ", "Kapasitas lanskap dalam mengatur siklus hidrologi, infiltrasi air tanah, dan pengendalian limpasan permukaan."),
        ("PHK (Pendukung Habitat & Keanekaragaman Hayati): ", "Kemampuan ekosistem dalam menyediakan relung hidup, keanekaragaman flora/fauna liar, dan koridor ekologis."),
        ("PPK (Penyerap & Penyimpan Karbon): ", "Potensi biomassa vegetasi dan bahan organik tanah dalam menyerap emisi CO2 atmosfer."),
        ("PYA (Penyedia Air Bersih): ", "Ketersediaan debit air bersih dari sumber alami (sungai, mata air, dan cekungan air tanah) untuk konsumsi manusia."),
        ("PGN (Penyedia Pangan): ", "Kapasitas produktivitas lanskap dalam menyediakan komoditas pertanian pangan, perkebunan, dan peternakan lokal."),
        ("PKU (Pengatur Kualitas Udara): ", "Peran vegetasi dalam menyaring partikulat polusi, memproduksi oksigen, dan meregulasi iklim mikro.")
    ]
    for in_title, in_desc in indicators:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_it = pb.add_run(in_title)
        r_it.bold = True
        r_it.font.color.rgb = RGBColor(0x2C, 0x5E, 0x8A)
        pb.add_run(in_desc)

    # -------------------------------------------------------------
    # BAB 2
    # -------------------------------------------------------------
    h2 = doc.add_heading("2. Tiga Pilar Komponen Input JLH", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(4)
    h2.style.font.name = "Arial"
    h2.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p2 = doc.add_paragraph(
        "Setiap piksel indikator JLH dihitung secara kuantitatif melalui integrasi linear tiga komponen spasial:"
    )
    add_callout(
        doc,
        "JLH = (Skor KBA × W_KBA) + (Skor KVA × W_KVA) + (Skor PL × W_PL)\n"
        "Di mana W_KBA + W_KVA + W_PL = 1.00 (Total Bobot 100%). Seluruh nilai skor dinormalisasi pada skala 1.0 (Sangat Rendah) hingga 5.0 (Sangat Tinggi).",
        title="FORMULA DASAR PERHITUNGAN JASA LINGKUNGAN HIDUP:"
    )

    doc.add_heading("2.1 Karakteristik Bentang Alam (KBA)", level=2)
    doc.add_paragraph(
        "KBA merepresentasikan faktor fisik abiotik permanen yang meliputi bentuk lahan (landform), elevasi topografi, "
        "kelerengan, geomorfologi, dan jenis batuan/tanah induk. KBA bersifat statis dalam skala dekade dan menjadi "
        "fondasi stabilitas fisik lingkungan. Misalnya pada indikator Pengaturan Air (PGA) dan Penyedia Air (PYA), "
        "pegunungan karst atau vulkanik muda dengan batuan permeabel memiliki skor KBA tinggi sebagai resapan air utama."
    )

    doc.add_heading("2.2 Karakteristik Vegetasi Alami (KVA)", level=2)
    doc.add_paragraph(
        "KVA merepresentasikan tutupan vegetasi klimaks alami (seperti formasi hutan hujan tropika pegunungan, hutan dataran "
        "rendah, hutan rawa gambut, dan mangrove) yang belum mengalami konversi masif. KVA mencerminkan integritas ekologis "
        "asli dan daya lenting ekosistem dalam menjaga keseimbangan iklim mikro serta habitat kehati."
    )

    doc.add_heading("2.3 Penutupan Lahan Multiskala 2025 (PL)", level=2)
    doc.add_paragraph(
        "Penutupan Lahan (PL) merupakan komponen antropogenik yang paling dinamis dan memiliki bobot dominan (60%). "
        "Data PL 2025 diklasifikasikan dari citra satelit resolusi sangat tinggi yang terbagi dalam ~2.300+ grid tile "
        "se-Sumatera Barat, mencakup 15 kelas tutupan lahan mulai dari hutan alami, badan air, pertanian, perkebunan, hingga permukiman."
    )

    # -------------------------------------------------------------
    # BAB 3
    # -------------------------------------------------------------
    h3 = doc.add_heading("3. Formulasi Matematis & Bobot 6 Indikator JLH Regional Sumatera", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(4)
    h3.style.font.name = "Arial"
    h3.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Penetapan pembobotan (Weighting) pada masing-masing indikator mengacu pada kaidah biogeofisik Regional Sumatera, "
        "di mana tutupan lahan aktual (PL) berkontribusi 60%, sedangkan 40% sisanya dibagi secara rasional antara Bentang Alam (KBA) "
        "dan Vegetasi Alami (KVA) sesuai karakteristik spesifik tiap fungsi ekosistem:"
    )

    # Table of weights
    tbl_w = doc.add_table(rows=7, cols=6)
    tbl_w.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_w = ["Indikator JLH", "W_KBA", "W_KVA", "W_PL", "Total", "Rasionalisasi Ilmiah Pembobotan"]
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
        ("PGA (Pengaturan Air)", "0.28", "0.12", "0.60", "1.00", "Bentuk bentang alam & permeabilitas batuan KBA dominan dalam laju resapan air."),
        ("PHK (Habitat & Kehati)", "0.24", "0.16", "0.60", "1.00", "Vegetasi alami klimaks KVA menyediakan koridor ekologis dan relung habitat fauna liar."),
        ("PPK (Penyimpan Karbon)", "0.20", "0.20", "0.60", "1.00", "KVA dan tutupan biomassa aktual PL memiliki kontribusi seimbang terhadap stok karbon."),
        ("PYA (Penyedia Air)", "0.32", "0.08", "0.60", "1.00", "Cekungan air tanah dan geomorfologi KBA paling krusial menentukan debit mata air alami."),
        ("PGN (Penyedia Pangan)", "0.28", "0.12", "0.60", "1.00", "Morfologi lereng dan kesuburan tanah vulkanik KBA menentukan produktivitas pangan."),
        ("PKU (Kualitas Udara)", "0.15", "0.25", "0.60", "1.00", "Kerapatan kanopi vegetasi alami KVA sangat krusial dalam menyerap gas polutan & panas.")
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

    # -------------------------------------------------------------
    # BAB 4
    # -------------------------------------------------------------
    h4 = doc.add_heading("4. Tabel Matriks Skor Penutupan Lahan (PL Lookup Table)", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(4)
    h4.style.font.name = "Arial"
    h4.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Setiap nilai raster kelas penutupan lahan (kategori integer 1 s.d. 15) ditransformasikan menjadi nilai "
        "skor layanan ekosistem berskala 1 (Sangat Rendah) hingga 5 (Sangat Tinggi) berdasarkan matriks rujukan KLH/BPLH:"
    )

    tbl_pl = doc.add_table(rows=12, cols=8)
    tbl_pl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_pl = ["Kode", "Kategori Penutupan Lahan", "PL PGA", "PL PHK", "PL PPK", "PL PYA", "PL PGN", "PL PKU"]
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
        ("8", "Bare Ground (Tanah Terbuka / Lahan Kosong)", "1", "1", "1", "1", "1", "1"),
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

    # -------------------------------------------------------------
    # BAB 5
    # -------------------------------------------------------------
    h5 = doc.add_heading("5. Skrip Python: Transformasi & Kalkulasi JLH Grid 0.5m", level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)
    h5.style.font.name = "Arial"
    h5.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Karena wilayah Provinsi Sumatera Barat pada resolusi 0.5 meter memiliki dimensi lebih dari 700.000 × 1.000.000 piksel "
        "(puluhan gigapiksel), pemrosesan langsung satu provinsi akan menyebabkan lonjakan memori (Out-Of-Memory / OOM Crash). "
        "Oleh karena itu, arsitektur komputasi dirancang berbasis Tile-Grid (~2.300+ tile) dengan dua inovasi optimasi:"
    )

    b_opt = [
        ("O(1) NumPy 1D Remap Table: ", "Alih-alih menggunakan operasi reclassify bercabang yang lambat, skor PL di-remap menggunakan array NumPy 1D berindeks 0–255 (Direct Array Indexing), mengeksekusi konversi 16 juta piksel per tile hanya dalam ~0.08 detik."),
        ("Windowed Reading Rasterio: ", "Data KBA dan KVA dibaca langsung hanya pada koordinat batas (bounding box) tile yang sedang diproses menggunakan rasterio.windows.from_bounds, sehingga RAM yang digunakan sangat minimal (< 1.5 GB).")
    ]
    for ot, od in b_opt:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_ot = pb.add_run(ot)
        r_ot.bold = True
        r_ot.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(od)

    code_step5 = """# ==============================================================================
# SKRIP TRANSFORMASI & PERHITUNGAN 6 INDIKATOR JLH PER TILE GRID (0.5 METER)
# File: calculate_jlh_sumbar_2025.py
# ==============================================================================
import os, glob
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from tqdm import tqdm

# 1. Konfigurasi Pembobotan Regional Sumatera
JLH_CONFIG = {
    'pga': {'name': 'Pengaturan Air',             'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'phk': {'name': 'Pendukung Habitat & Kehati', 'w_kba': 0.24, 'w_kva': 0.16, 'w_pl': 0.60},
    'ppk': {'name': 'Penyerap & Simpan Karbon',   'w_kba': 0.20, 'w_kva': 0.20, 'w_pl': 0.60},
    'pya': {'name': 'Penyedia Air',               'w_kba': 0.32, 'w_kva': 0.08, 'w_pl': 0.60},
    'pgn': {'name': 'Penyedia Pangan (Sumatera)', 'w_kba': 0.28, 'w_kva': 0.12, 'w_pl': 0.60},
    'pku': {'name': 'Pengatur Kualitas Udara',    'w_kba': 0.15, 'w_kva': 0.25, 'w_pl': 0.60}
}

# 2. Matriks Lookup Skor PL (1 s.d. 15)
PL_LOOKUP = {
    1:  {'pga': 5, 'phk': 1, 'ppk': 1, 'pya': 5, 'pgn': 4, 'pku': 5},
    2:  {'pga': 5, 'phk': 5, 'ppk': 5, 'pya': 3, 'pgn': 4, 'pku': 5},
    4:  {'pga': 4, 'phk': 3, 'ppk': 3, 'pya': 3, 'pgn': 4, 'pku': 5},
    5:  {'pga': 3, 'phk': 1, 'ppk': 1, 'pya': 3, 'pgn': 4, 'pku': 3},
    7:  {'pga': 2, 'phk': 1, 'ppk': 1, 'pya': 2, 'pgn': 1, 'pku': 2},
    8:  {'pga': 1, 'phk': 1, 'ppk': 1, 'pya': 1, 'pgn': 1, 'pku': 1},
    11: {'pga': 3, 'phk': 2, 'ppk': 2, 'pya': 1, 'pgn': 2, 'pku': 3},
    12: {'pga': 3, 'phk': 2, 'ppk': 2, 'pya': 2, 'pgn': 3, 'pku': 4},
    13: {'pga': 3, 'phk': 3, 'ppk': 2, 'pya': 2, 'pgn': 3, 'pku': 3},
    14: {'pga': 1, 'phk': 1, 'ppk': 1, 'pya': 1, 'pgn': 1, 'pku': 1},
    15: {'pga': 1, 'phk': 1, 'ppk': 1, 'pya': 2, 'pgn': 1, 'pku': 1}
}

# Inisialisasi Tabel Remap Cepat NumPy (Index 0 s.d. 255)
PL_REMAP = {}
for key in JLH_CONFIG.keys():
    arr = np.zeros(256, dtype=np.float32)
    for c_val, scores in PL_LOOKUP.items():
        arr[c_val] = scores[key]
    PL_REMAP[key] = arr

def process_single_grid(pl_tile_path, kba_datasets, kva_datasets, output_path):
    with rasterio.open(pl_tile_path) as src_pl:
        pl_data = src_pl.read(1)
        bounds = src_pl.bounds
        shape = pl_data.shape
        meta = src_pl.meta.copy()

        # Deteksi piksel valid daratan
        valid_mask = pl_data > 0
        if not np.any(valid_mask):
            return False

        meta.update({
            'count': 6,
            'dtype': 'float32',
            'nodata': 0.0,
            'compress': 'deflate',
            'predictor': 3
        })

        jlh_stack = np.zeros((6, shape[0], shape[1]), dtype=np.float32)

        for band_idx, (key, cfg) in enumerate(JLH_CONFIG.items()):
            # A. Skor PL via Array Indexing Instan
            score_pl = PL_REMAP[key][pl_data]

            # B. Windowed Reading KBA & KVA sesuai bounds tile
            win_kba = from_bounds(*bounds, transform=kba_datasets[key].transform)
            score_kba = kba_datasets[key].read(1, window=win_kba, out_shape=shape).astype(np.float32)

            win_kva = from_bounds(*bounds, transform=kva_datasets[key].transform)
            score_kva = kva_datasets[key].read(1, window=win_kva, out_shape=shape).astype(np.float32)

            # C. Integrasi Kombinasi Linear
            jlh_val = (score_kba * cfg['w_kba']) + (score_kva * cfg['w_kva']) + (score_pl * cfg['w_pl'])
            jlh_val = np.where(valid_mask, jlh_val, 0.0)
            jlh_stack[band_idx] = jlh_val

        with rasterio.open(output_path, 'w', **meta) as dst:
            dst.write(jlh_stack)
            for idx, key in enumerate(JLH_CONFIG.keys(), start=1):
                dst.set_band_description(idx, f"JLH_{key.upper()}")
        return True"""
    add_code_block(doc, code_step5, caption="calculate_jlh_sumbar_2025.py (Komputasi Paralel Grid 0.5m)")

    # -------------------------------------------------------------
    # BAB 6
    # -------------------------------------------------------------
    h6 = doc.add_heading("6. Skrip Python: Mozaik Seamless Se-Sumatera Barat & Kompresi LERC_ZSTD", level=1)
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(4)
    h6.style.font.name = "Arial"
    h6.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Setelah seluruh grid tile selesai dikalkulasi, ribuan file pecahan digabungkan menjadi 1 file GeoTIFF utuh "
        "(seamless 1-file per layer) se-Provinsi Sumatera Barat. Jika disimpan dengan format GeoTIFF standar tanpa kompresi, "
        "ukuran 1 layer raster 0.5m se-provinsi mencapai lebih dari 120 GigaBytes (GB). "
        "Solusi modern yang diterapkan adalah algoritma kompresi mutakhir LERC_ZSTD (Limited Error Raster Compression + Zstandard):"
    )

    b_lerc = [
        ("max_z_error = 0.005: ", "Toleransi galat maksimum dibatasi hanya 0.005 (setengah persen dari skala 1 s.d. 5), menjamin akurasi saintifik 99.9% utuh."),
        ("Pengurangan Ukuran Drastis: ", "Ukuran file berkurang dari ~120 GB menjadi hanya ~350 MB per layer (~97% disk saving)."),
        ("Internal Tiling & BigTIFF: ", "Raster dibagi ke blok internal 512×512 piksel sehingga sangat cepat diakses di QGIS, ArcGIS, maupun WebGIS.")
    ]
    for lt, ld in b_lerc:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_lt = pb.add_run(lt)
        r_lt.bold = True
        r_lt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(ld)

    code_step6 = """# ==============================================================================
# SKRIP MOZAIK SEAMLESS & EKSPOR KOMPRESI LERC_ZSTD CHUNKING
# File: create_seamless_jlh_lerc.py
# ==============================================================================
import rasterio
from rasterio.windows import Window
import numpy as np

def export_seamless_lerc_zstd(input_vrt_path, output_tif_path, width, height, num_chunks=245):
    with rasterio.open(input_vrt_path) as src:
        profile = src.profile.copy()
        profile.update({
            'driver': 'GTiff',
            'dtype': 'float32',
            'nodata': 0.0,
            'compress': 'lerc_zstd',
            'max_z_error': 0.005,
            'tiled': True,
            'blockxsize': 512,
            'blockysize': 512,
            'bigtiff': 'YES'
        })

        chunk_size = 4096
        with rasterio.open(output_tif_path, 'w', **profile) as dst:
            for c in range(num_chunks):
                r_start = c * chunk_size
                curr_h = min(chunk_size, height - r_start)
                win = Window(0, r_start, width, curr_h)

                chunk_data = src.read(1, window=win)
                dst.write(chunk_data, 1, window=win)
                print(f"Chunk {c+1}/{num_chunks} tersimpan!")"""
    add_code_block(doc, code_step6, caption="create_seamless_jlh_lerc.py (Chunking LERC_ZSTD Mozaik)")

    doc.add_paragraph(
        "Hasil Produk Layer Seamless Se-Sumatera Barat Berbasis LERC_ZSTD:"
    )
    prod_files = [
        ("sumbar_2025_jlh_pga_seamless.tif", "403 MB", "JLH Pengaturan Air"),
        ("sumbar_2025_jlh_phk_seamless.tif", "362 MB", "JLH Pendukung Habitat & Kehati (Alami)"),
        ("sumbar_2025_jlh_phk_kk_seamless.tif", "375 MB", "JLH Habitat & Kehati dengan Penyesuaian Kriteria Khusus"),
        ("sumbar_2025_jlh_ppk_seamless.tif", "307 MB", "JLH Penyerap & Penyimpan Karbon"),
        ("sumbar_2025_jlh_pya_seamless.tif", "360 MB", "JLH Penyedia Air"),
        ("sumbar_2025_jlh_pgn_seamless.tif", "342 MB", "JLH Penyedia Pangan"),
        ("sumbar_2025_jlh_pku_seamless.tif", "427 MB", "JLH Pengatur Kualitas Udara"),
        ("sumbar_2025_kba_seamless.tif", "178 MB", "Master Karakteristik Bentang Alam"),
        ("sumbar_2025_kva_seamless.tif", "169 MB", "Master Karakteristik Vegetasi Alami")
    ]
    tbl_p = doc.add_table(rows=len(prod_files)+1, cols=3)
    tbl_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Nama File Seamless (0.5m)", "Ukuran File", "Deskripsi Lapisan Tematik"]):
        cell = tbl_p.cell(0, j)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=90, bottom=90, left=110, right=110)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, (fname, fsize, fdesc) in enumerate(prod_files, start=1):
        bg_col = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate([fname, fsize, fdesc]):
            cell = tbl_p.cell(i, j)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=60, bottom=60, left=110, right=110)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    set_table_borders(tbl_p, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # BAB 7
    # -------------------------------------------------------------
    h7 = doc.add_heading("7. Penyesuaian Kriteria Khusus (KK.gpkg) pada Layer PHK", level=1)
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(4)
    h7.style.font.name = "Arial"
    h7.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Pada indikator Pendukung Habitat & Keanekaragaman Hayati (PHK), dilakukan penyesuaian berbasis kebijakan "
        "dan kawasan konservasi bernilai konservasi tinggi (High Conservation Value / HCV) melalui penumpangsusunan "
        "layer vektor poligon Kriteria Khusus (KK.gpkg):"
    )

    b_kk = [
        ("Kriteria Khusus 1 (KK 1): ", "Zona Inti Konservasi Mutlak (Cagar Alam, Taman Nasional, Suaka Margasatwa, Koridor Satwa Kunci). Seluruh piksel di dalam poligon ini dipaksa bernilai mutlak 5.0 (Sangat Tinggi)."),
        ("Kriteria Khusus 2 & 3 (KK 2 & KK 3): ", "Zona Penyangga Ekologis & Restorasi Ekosistem. Seluruh piksel di dalam poligon ini dipaksa bernilai minimal 4.0 (Tinggi)."),
        ("Area Di Luar Poligon KK: ", "Tetap mempertahankan nilai asli hasil perhitungan KBA, KVA, dan PL.")
    ]
    for kt, kd in b_kk:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_kt = pb.add_run(kt)
        r_kt.bold = True
        r_kt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(kd)

    code_step7 = """# ==============================================================================
# PENYESUAIAN KRITERIA KHUSUS PADA LAYER PHK
# File: apply_kk_phk.py
# ==============================================================================
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np

def apply_kriteria_khusus(input_phk_tif, kk_gpkg_path, output_phk_kk_tif):
    gdf = gpd.read_file(kk_gpkg_path)
    
    with rasterio.open(input_phk_tif) as src:
        meta = src.meta.copy()
        phk_data = src.read(1)
        transform = src.transform
        shape = phk_data.shape
        
        # Pisahkan KK1 dan KK2/3
        gdf_kk1 = gdf[gdf['KK_PHK25'] == 'Kriteria Khusus 1']
        gdf_kk23 = gdf[gdf['KK_PHK25'].isin(['Kriteria Khusus 2', 'Kriteria Khusus 3'])]
        
        # Rasterize poligon ke grid raster
        mask_kk1 = rasterize([(geom, 1) for geom in gdf_kk1.geometry], out_shape=shape, transform=transform, default_value=0, dtype=np.uint8)
        mask_kk23 = rasterize([(geom, 1) for geom in gdf_kk23.geometry], out_shape=shape, transform=transform, default_value=0, dtype=np.uint8)
        
        # Override nilai PHK
        phk_adjusted = np.where(mask_kk1 == 1, 5.0, phk_data)
        phk_adjusted = np.where((mask_kk23 == 1) & (phk_adjusted < 4.0), 4.0, phk_adjusted)
        
        with rasterio.open(output_phk_kk_tif, 'w', **meta) as dst:
            dst.write(phk_adjusted, 1)"""
    add_code_block(doc, code_step7, caption="apply_kk_phk.py (Rasterizing Vektor Kriteria Khusus)")

    # -------------------------------------------------------------
    # BAB 8
    # -------------------------------------------------------------
    h8 = doc.add_heading("8. Hilirisasi Analisis: Pemodelan Spasial JLH Ruang Hidup (Relokasi Huntap/Huntara)", level=1)
    h8.paragraph_format.space_before = Pt(14)
    h8.paragraph_format.space_after = Pt(4)
    h8.style.font.name = "Arial"
    h8.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Puncak pemanfaatan data JLH adalah hilirisasi analitik untuk perencanaan relokasi permukiman masyarakat pasca-bencana "
        "banjir bandang (galodo) dan tanah longsor di Sumatera Barat. Analisis Kesesuaian Lahan Relokasi (JLH Ruang Hidup) "
        "ini menggunakan pendekatan Multi-Criteria Evaluation (MCE) Realistis:"
    )

    doc.add_heading("8.1 Rasionalisasi Formula Bobot Realistis (50% Bahaya : 50% JLH)", level=2)
    doc.add_paragraph(
        "Pada pendekatan awal, layer PHK (Habitat & Kehati) dan PPK (Karbon) sempat disertakan sebagai eliminator, "
        "yang menyebabkan hampir seluruh wilayah daratan berlubang (tereliminasi) karena kawasan hutan konservasi dan "
        "tutupan pohon lebat dinilai bernilai 5.0. Pada formulasi realistis yang disepakati, PHK dan PPK dikeluarkan dari "
        "formula matematis awal dan dipindahkan ke tahap Screening Hukum (Kawasan Hutan 2026). "
        "Struktur pembobotan realistis dibagi secara berimbang menjadi dua pilar utama:"
    )

    b_mce = [
        ("50% PILAR KESELAMATAN (Bahaya Bencana Hidrometeorologi): ", "Bahaya Tanah Longsor (20%), Bahaya Banjir Genangan (15%), dan Bahaya Banjir Bandang / Galodo (15%)."),
        ("50% PILAR MUTU HIDUP & DAYA DUKUNG (4 JLH Utama): ", "Penyedia Air / PYA (17.5%), Penyedia Pangan / PGN (17.5%), Pengaturan Air / PGA (10%), dan Pengatur Kualitas Udara / PKU (5%)."),
        ("GATEKEEPER CONSTRAINT (Eliminasi Mutlak): ", "Piksel dengan indeks bahaya tinggi (Nilai Bahaya > 0.66) pada salah satu bencana langsung dieliminasi secara mutlak (Skor Kesesuaian = 0.0).")
    ]
    for mt, md in b_mce:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_mt = pb.add_run(mt)
        r_mt.bold = True
        r_mt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(md)

    add_callout(
        doc,
        "Skor Kesesuaian Lahan Relokasi =\n"
        "Gatekeeper × [(0.20 × Skor_LS) + (0.15 × Skor_BJ) + (0.15 × Skor_GD) + (0.175 × Skor_PYA) + (0.175 × Skor_PGN) + (0.10 × Skor_PGA) + (0.05 × Skor_PKU)]\n"
        "Di mana Gatekeeper = 0 jika Bahaya > 0.66, dan Gatekeeper = 1 jika Bahaya ≤ 0.66.",
        title="FORMULA MATEMATIS MCE REALISTIS RUANG HIDUP:"
    )

    doc.add_heading("8.2 Skrip Python Eksekusi MCE (Versi 10m Quick View & 0.5m Full)", level=2)
    code_step8 = """# ==============================================================================
# PEMODELAN MCE KESESUAIAN RELOKASI REALISTIS SUMATERA BARAT
# File: run_mce_realistic_05m.py
# ==============================================================================
import rasterio
from rasterio.windows import Window
import numpy as np

# Lookup Table Normalisasi JLH (Skala 0 s.d. 1.0)
lut_pya = np.array([0.0, 0.0, 0.25, 0.50, 0.75, 1.00], dtype=np.float32) # Monotonik Naik
lut_pgn = np.array([0.0, 0.0, 0.25, 0.50, 0.75, 1.00], dtype=np.float32) # Monotonik Naik
lut_pga = np.array([0.0, 0.0, 0.20, 1.00, 0.50, 0.00], dtype=np.float32) # Optimal pada Skor 3
lut_pku = np.array([0.0, 0.0, 0.20, 1.00, 0.50, 0.00], dtype=np.float32) # Optimal pada Skor 3

def compute_chunk_mce(pga, pya, pgn, pku, ls, bj, gd):
    # 1. Normalisasi Faktor Bahaya (Aman = 1.0, Sedang = 0.5, Tinggi = 0.0)
    s_ls = np.where(ls <= 0.33, 1.0, np.where(ls <= 0.66, 0.5, 0.0)).astype(np.float32)
    s_bj = np.where(bj <= 0.33, 1.0, np.where(bj <= 0.66, 0.5, 0.0)).astype(np.float32)
    s_gd = np.where(gd <= 0.33, 1.0, np.where(gd <= 0.66, 0.5, 0.0)).astype(np.float32)
    
    # Gatekeeper Constraint: Jika ada bahaya tinggi (>0.66) -> Mutlak Gugur
    gatekeeper = (ls <= 0.66) & (bj <= 0.66) & (gd <= 0.66)
    
    # 2. Normalisasi 4 JLH
    s_pya = lut_pya[np.clip(np.round(pya).astype(int), 0, 5)]
    s_pgn = lut_pgn[np.clip(np.round(pgn).astype(int), 0, 5)]
    s_pga = lut_pga[np.clip(np.round(pga).astype(int), 0, 5)]
    s_pku = lut_pku[np.clip(np.round(pku).astype(int), 0, 5)]
    
    # 3. Penjumlahan Berbobot
    score = (
        (0.20 * s_ls) + (0.15 * s_bj) + (0.15 * s_gd) +
        (0.175 * s_pya) + (0.175 * s_pgn) + (0.10 * s_pga) + (0.05 * s_pku)
    )
    
    # Terapkan Gatekeeper & Validitas
    score = np.where(gatekeeper & (pga > 0), score, 0.0)
    return score"""
    add_code_block(doc, code_step8, caption="run_mce_realistic_05m.py (Fungsi Komputasi MCE Ruang Hidup)")

    doc.add_heading("8.3 Screening Kebijakan: Kawasan Hutan 2026 & RTRW", level=2)
    doc.add_paragraph(
        "Hasil pemodelan MCE yang telah menghasilkan skor 0.0 hingga 1.0 selanjutnya di-overlay dengan status hukum "
        "dan tata ruang aktual untuk menerbitkan arahan operasional pembangunan hunian tetap/sementara:"
    )

    tbl_pol = doc.add_table(rows=5, cols=4)
    tbl_pol.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Status Kawasan Hutan", "Pola Ruang RTRW", "Kategori Kesesuaian MCE", "Rekomendasi Kebijakan Operasional"]):
        cell = tbl_pol.cell(0, j)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_pol = [
        ("Area Penggunaan Lain (APL)", "Kawasan Permukiman / Perdesaan", "Sangat Sesuai (0.75 - 1.00)", "PRIORITAS 1: Siap bangun fisik Huntap secara langsung tanpa hambatan kehutanan."),
        ("Hutan Produksi Konversi (HPK)", "Bukan Kawasan Lindung", "Sesuai (0.50 - 0.74)", "PRIORITAS 2: Layak teknis; diproses melalui mekanisme Pelepasan Kawasan Hutan ke Kementerian LHK."),
        ("Hutan Produksi Tetap (HPT)", "Kawasan Budidaya", "Sesuai (0.50 - 0.74)", "ALTERNATIF BERSYARAT: Memerlukan mekanisme Persetujuan Penggunaan Kawasan Hutan (PPKH)."),
        ("Hutan Lindung (HL) / Konservasi", "Kawasan Lindung", "Semua Nilai", "DILARANG MUTLAK: Tidak boleh dibangun hunian guna mencegah degradasi hidrologis dan bencana susulan.")
    ]
    for i, row in enumerate(data_pol, start=1):
        bg_col = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = tbl_pol.cell(i, j)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if j == 0:
                r.font.bold = True
            elif j == 3 and "DILARANG" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
            elif j == 3 and "PRIORITAS 1" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x00, 0x70, 0xC0)

    set_table_borders(tbl_pol, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # BAB 9
    # -------------------------------------------------------------
    h9 = doc.add_heading("9. Petunjuk Operasional & Visualisasi Data di QGIS", level=1)
    h9.paragraph_format.space_before = Pt(14)
    h9.paragraph_format.space_after = Pt(4)
    h9.style.font.name = "Arial"
    h9.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Untuk membuka dan menganalisis file raster JLH maupun hasil MCE di aplikasi QGIS:"
    )
    b_qgis = [
        ("Membuka File Raster: ", "Drag-and-drop file sumbar_2025_kesesuaian_relokasi_realistic_10m.tif atau sumbar_2025_jlh_*_seamless.tif langsung ke panel Layers QGIS."),
        ("Pewarnaan Simbologi: ", "Buka Layer Properties > Symbology > Render type ubah ke 'Singleband pseudocolor'. Gunakan Color Ramp 'RdYlGn' (Merah - Kuning - Hijau) atau 'Spectral' (Inverted) dengan Min = 0.0 dan Max = 1.0."),
        ("Klasifikasi Diskret: ", "Ubah Mode ke 'Equal Interval' atau 'Discrete' dengan 3 kelas: [0.0 - 0.50: Kurang Sesuai (Merah)], [0.50 - 0.74: Sesuai Bersyarat (Kuning)], [0.75 - 1.00: Sangat Sesuai (Hijau)]."),
        ("Penanganan NoData: ", "Buka tab Transparency, pastikan Additional no data value diisi 0.0 jika ingin menghilangkan area laut/luar provinsi agar transparan.")
    ]
    for qt, qd in b_qgis:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_qt = pb.add_run(qt)
        r_qt.bold = True
        r_qt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(qd)

    # -------------------------------------------------------------
    # BAB 10
    # -------------------------------------------------------------
    h10 = doc.add_heading("10. Spesifikasi Teknis Server & Ringkasan File Produk", level=1)
    h10.paragraph_format.space_before = Pt(14)
    h10.paragraph_format.space_after = Pt(4)
    h10.style.font.name = "Arial"
    h10.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    doc.add_paragraph(
        "Pemrosesan skala gigapiksel 0.5 meter didukung oleh infrastruktur cloud computing berkinerja tinggi:"
    )
    b_srv = [
        ("Server VPS Dedicated: ", "Host IP 182.23.160.75 (Kementerian Lingkungan Hidup / BPLH)."),
        ("Spesifikasi Komputasi: ", "16 vCPU, 64 GB RAM, Solid State Drive (SSD) Enterprise."),
        ("Lingkungan Perangkat Lunak: ", "Ubuntu Linux 24.04 LTS, Python 3.12, GDAL 3.8.4, Rasterio 1.3.10, NumPy 1.26.4."),
        ("Lokasi File Output Server: ", "/home/kemenlh/jlh/output/ (Seamless JLH) dan /home/kemenlh/jlh/output/kesesuaian_relokasi/ (MCE Relokasi)."),
        ("Lokasi File Lokal (Mac): ", "data/jlh_seamless/ pada direktori kerja proyek JLH.")
    ]
    for st, sd in b_srv:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.space_before = Pt(1)
        pb.paragraph_format.space_after = Pt(2)
        r_st = pb.add_run(st)
        r_st.bold = True
        r_st.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        pb.add_run(sd)

    # Closing paragraph
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(14)
    p_close.paragraph_format.space_after = Pt(4)
    r_c = p_close.add_run("Dokumen ini disahkan sebagai laporan teknis metodologi dan repositori skrip pemodelan spasial Jasa Lingkungan Hidup (JLH) Provinsi Sumatera Barat tahun 2025–2026.")
    r_c.font.italic = True
    r_c.font.size = Pt(9.5)
    r_c.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    output_filename = "Dokumentasi_Metodologi_dan_Skrip_JLH_Sumbar.docx"
    doc.save(output_filename)
    print(f"File dokumen Word berhasil dibuat: {output_filename}")

if __name__ == "__main__":
    create_document()
