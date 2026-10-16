import zipfile
import re
import os

docx_path = r"report/Mẫu ĐATN_2019_version 1_1.docx"
out_dir = r"figures"

with zipfile.ZipFile(docx_path, 'r') as z:
    rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
    doc_xml = z.read('word/document.xml').decode('utf-8')
    
    # find relationships
    rel_dict = {}
    for m in re.finditer(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels_xml):
        rel_dict[m.group(1)] = m.group(2)
        
    embeds = re.findall(r'embed="([^"]+)"', doc_xml)
    print("Found embeds in doc:", embeds[:10])
    for rId in embeds[:5]:
        target = rel_dict.get(rId)
        print(f"  {rId} -> {target}")
        if target:
            target_path = 'word/' + target
            if target_path in z.namelist():
                out_name = os.path.basename(target)
                dest = os.path.join(out_dir, "hust_logo.png")
                with open(dest, "wb") as f_out:
                    f_out.write(z.read(target_path))
                print(f"Extracted first image to {dest}")
                break
