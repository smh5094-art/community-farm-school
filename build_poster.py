"""
Build the donor-facing PDF leave-behind:
  Page 1 = giving-tree poster
  Page 2 = $250k match challenge one-pager

Also outputs a high-res PNG of page 1 (for web display).

Run from the community-farm-school directory:
    python3 build_poster.py
"""
import base64
import re
from pathlib import Path
import cairosvg
from pypdf import PdfWriter, PdfReader
import io

ROOT = Path(__file__).parent
TREE_SVG = ROOT / "images" / "giving-tree-poster.svg"
MATCH_SVG = ROOT / "images" / "match-challenge-page.svg"
TREE_PNG = ROOT / "images" / "giving-tree-v2.png"

OUT_DIR = ROOT / "downloads"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PDF = OUT_DIR / "community-farm-school-giving-tree.pdf"
OUT_PNG = OUT_DIR / "giving-tree-poster.png"

# ---------- Embed the tree image as base64 in the poster SVG ----------
with open(TREE_PNG, "rb") as f:
    tree_b64 = base64.b64encode(f.read()).decode("ascii")
tree_uri = f"data:image/png;base64,{tree_b64}"

with open(TREE_SVG) as f:
    tree_svg = f.read()

tree_svg = re.sub(
    r'<image xlink:href="giving-tree-v2\.png" href="giving-tree-v2\.png"',
    f'<image xlink:href="{tree_uri}" href="{tree_uri}"',
    tree_svg,
)

# ---------- Render page 1 (tree poster) ----------
# Letter-portrait at 200 dpi: 1700 × 2200; PDF page sizes are in points (1pt = 1/72").
# US Letter = 612 × 792 pt. We render the SVG to fill that page proportionally.
tree_pdf_bytes = cairosvg.svg2pdf(bytestring=tree_svg.encode("utf-8"),
                                  output_width=612, output_height=765)
cairosvg.svg2png(bytestring=tree_svg.encode("utf-8"),
                 write_to=str(OUT_PNG), output_width=1600)

# ---------- Render page 2 (match challenge) ----------
with open(MATCH_SVG) as f:
    match_svg = f.read()
match_pdf_bytes = cairosvg.svg2pdf(bytestring=match_svg.encode("utf-8"),
                                   output_width=612, output_height=765)

# ---------- Merge into a single 2-page PDF ----------
writer = PdfWriter()
for pdf_bytes in (tree_pdf_bytes, match_pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    for page in reader.pages:
        writer.add_page(page)

with open(OUT_PDF, "wb") as f:
    writer.write(f)

print(f"PDF: {OUT_PDF} ({OUT_PDF.stat().st_size:,} bytes, 2 pages)")
print(f"PNG: {OUT_PNG} ({OUT_PNG.stat().st_size:,} bytes)")
