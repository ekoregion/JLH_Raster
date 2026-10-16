import zipfile
import os
import shutil

def create_pptx(output_pptx_path, image_paths):
    # Buat direktori sementara
    temp_dir = "/tmp/pptx_build"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(f"{temp_dir}/_rels", exist_ok=True)
    os.makedirs(f"{temp_dir}/ppt/_rels", exist_ok=True)
    os.makedirs(f"{temp_dir}/ppt/slides/_rels", exist_ok=True)
    os.makedirs(f"{temp_dir}/ppt/media", exist_ok=True)

    # 1. [Content_Types].xml
    slide_overrides = ""
    for i in range(1, len(image_paths) + 1):
        slide_overrides += f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'

    content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Default Extension="jpg" ContentType="image/jpeg"/>
    <Default Extension="png" ContentType="image/png"/>
    <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
    {slide_overrides}
</Types>'''
    with open(f"{temp_dir}/[Content_Types].xml", "w") as f:
        f.write(content_types)

    # 2. _rels/.rels
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>'''
    with open(f"{temp_dir}/_rels/.rels", "w") as f:
        f.write(root_rels)

    # 3. ppt/presentation.xml
    sld_id_lst = ""
    pres_rels = ""
    for i in range(1, len(image_paths) + 1):
        sld_id_lst += f'<p:sldId id="{255 + i}" r:id="rId{i}"/>\n'
        pres_rels += f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'

    # Ukuran 16:9 widescreen: 12192000 x 6858000 EMU (13.333 x 7.5 inches)
    presentation_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" 
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" 
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
    <p:sldMasterIdLst/>
    <p:sldIdLst>
        {sld_id_lst}
    </p:sldIdLst>
    <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
    <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>'''
    with open(f"{temp_dir}/ppt/presentation.xml", "w") as f:
        f.write(presentation_xml)

    with open(f"{temp_dir}/ppt/_rels/presentation.xml.rels", "w") as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    {pres_rels}
</Relationships>''')

    # Copy images and create slide XMLs
    for i, img_path in enumerate(image_paths, 1):
        ext = os.path.splitext(img_path)[1].lower()
        target_img_name = f"image{i}{ext}"
        shutil.copyfile(img_path, f"{temp_dir}/ppt/media/{target_img_name}")

        slide_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" 
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" 
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
    <p:cSld>
        <p:spTree>
            <p:nvGrpSpPr>
                <p:cNvPr id="1" name=""/>
                <p:cNvGrpSpPr/>
                <p:nvPr/>
            </p:nvGrpSpPr>
            <p:grpSpPr/>
            <p:pic>
                <p:nvPicPr>
                    <p:cNvPr id="{i + 1}" name="SlideImage{i}"/>
                    <p:cNvPicPr>
                        <a:picLocks noChangeAspect="1"/>
                    </p:cNvPicPr>
                    <p:nvPr/>
                </p:nvPicPr>
                <p:blipFill>
                    <a:blip r:embed="rId1"/>
                    <a:stretch>
                        <a:fillRect/>
                    </a:stretch>
                </p:blipFill>
                <p:spPr>
                    <a:xfrm>
                        <a:off x="0" y="0"/>
                        <a:ext cx="12192000" cy="6858000"/>
                    </a:xfrm>
                    <a:prstGeom prst="rect">
                        <a:avLst/>
                    </a:prstGeom>
                </p:spPr>
            </p:pic>
        </p:spTree>
    </p:cSld>
</p:sld>'''
        with open(f"{temp_dir}/ppt/slides/slide{i}.xml", "w") as f:
            f.write(slide_xml)

        slide_rel = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{target_img_name}"/>
</Relationships>'''
        with open(f"{temp_dir}/ppt/slides/_rels/slide{i}.xml.rels", "w") as f:
            f.write(slide_rel)

    # Pack into .pptx (zip)
    with zipfile.ZipFile(output_pptx_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                zipf.write(full_path, rel_path)

    shutil.rmtree(temp_dir)
    print(f"Successfully generated: {output_pptx_path}")

if __name__ == "__main__":
    imgs = [
        "/Users/danangwijaya/.gemini/antigravity/brain/cddee218-adc1-4a5a-846c-be7258a8414e/jlh_cover_slide_1791563375091.jpg",
        "/Users/danangwijaya/.gemini/antigravity/brain/cddee218-adc1-4a5a-846c-be7258a8414e/jlh_outline_slide_1791563422741.jpg",
        "/Users/danangwijaya/.gemini/antigravity/brain/cddee218-adc1-4a5a-846c-be7258a8414e/jlh_calculation_slide_1791563402482.jpg"
    ]
    out = "/Users/danangwijaya/Documents/Danang/PROJECT/CODE/JLH/Presentasi_Perhitungan_JLH.pptx"
    create_pptx(out, imgs)
