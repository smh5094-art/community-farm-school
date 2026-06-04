"""Build the single-page donor PDF from the giving-tree poster image."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
SRC = ROOT / "images" / "giving-tree-v3.png"
OUT_PDF = ROOT / "downloads" / "community-farm-school-giving-tree.pdf"
OUT_PDF.parent.mkdir(exist_ok=True)

# US Letter at 200 DPI: 1700 x 2200 px
PAGE_W, PAGE_H = 1700, 2200
MARGIN = 60

img = Image.open(SRC).convert("RGB")
iw, ih = img.size

# Fit within page minus margins, preserve aspect ratio
max_w = PAGE_W - 2 * MARGIN
max_h = PAGE_H - 2 * MARGIN
scale = min(max_w / iw, max_h / ih)
nw, nh = int(iw * scale), int(ih * scale)
img_resized = img.resize((nw, nh), Image.LANCZOS)

# Compose centered on cream page
page = Image.new("RGB", (PAGE_W, PAGE_H), (252, 248, 235))
x = (PAGE_W - nw) // 2
y = (PAGE_H - nh) // 2
page.paste(img_resized, (x, y))

page.save(OUT_PDF, "PDF", resolution=200.0)
print(f"PDF: {OUT_PDF} ({OUT_PDF.stat().st_size:,} bytes)")
