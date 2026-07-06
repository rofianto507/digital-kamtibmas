"""
embed_screenshots.py
────────────────────
Script untuk menambahkan screenshot ke presentasi HTML Digital Kamtibmas.

CARA PAKAI:
  1. Simpan screenshot ke folder:
       digital_kamtibmas/static/img/screenshots/

  2. Namai file screenshot sesuai konvensi berikut:
       satlantas.jpg    -> Slide Satlantas (Laka / Antrian / Peta)
       satnarkoba.jpg   -> Slide Satnarkoba
       satreskrim.jpg   -> Slide Satreskrim
       sabhara.jpg      -> Slide Sabhara (Patroli / Peta Live)
       tahti.jpg        -> Slide Tahti
       intelkam.jpg     -> Slide Intelkam
       dashboard.jpg    -> Slide Dashboard

     Format diterima: .jpg, .jpeg, .png, .webp
     (Script akan otomatis konversi & compress ke JPEG)

  3. Jalankan script ini:
       python embed_screenshots.py

  4. Buka presentasi_digital_kamtibmas.html di browser — selesai!

CATATAN:
  - Script bisa dijalankan berulang kali (idempotent)
  - Screenshot yang belum ada akan tampil sebagai placeholder
  - Target ukuran setelah compress: ≤ 120 KB per gambar
  - Resolusi output: max 960px lebar (height auto-proportional)
"""

import base64, os, re, sys
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("ERROR: Pillow belum diinstall. Jalankan: pip install Pillow")

# ── PATHS ──────────────────────────────────────────────────────
BASE    = Path(__file__).parent
HTML    = BASE / "presentasi_digital_kamtibmas.html"
SCR_DIR = BASE / "static" / "img" / "screenshots"

# ── SLIDE CONFIG ───────────────────────────────────────────────
# key -> (slide_id, caption)
SLIDES = {
    "satlantas":  ("s4",  "Tampilan Sistem — Satlantas"),
    "satnarkoba": ("s5",  "Tampilan Sistem — Satnarkoba"),
    "satreskrim": ("s6",  "Tampilan Sistem — Satreskrim"),
    "sabhara":    ("s7",  "Tampilan Sistem — Sabhara"),
    "tahti":      ("s8",  "Tampilan Sistem — Tahti"),
    "intelkam":   ("s9",  "Tampilan Sistem — Intelkam"),
    "dashboard":  ("s10", "Dashboard Monitoring Terpadu"),
}

# ── COMPRESS IMAGE ─────────────────────────────────────────────
def compress_to_b64(path: Path, max_w=960, quality=82) -> str:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    if w > max_w:
        img = img.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    kb = len(buf.getvalue()) // 1024
    print(f"  compress: {path.name} -> {kb} KB ({img.size[0]}x{img.size[1]})")
    return base64.b64encode(buf.getvalue()).decode()

# ── FIND SCREENSHOT FILE ────────────────────────────────────────
def find_scr(key: str) -> Path | None:
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = SCR_DIR / (key + ext)
        if p.exists():
            return p
    return None

# ── CSS TO INJECT (only once) ──────────────────────────────────
SCR_CSS = """
    /* ── SCREENSHOT PANEL (inject by embed_screenshots.py) ─── */
    .split--scr {
      grid-template-columns: 230px 1fr 300px;
      max-width: 1080px;
    }
    .scr-panel {
      border-radius: 10px; overflow: hidden;
      background: var(--surf2);
      border: 1px solid rgba(255,255,255,.07);
      position: relative; display: flex;
      flex-direction: column; align-items: stretch;
    }
    .scr-panel .scr-img {
      width: 100%; flex: 1; min-height: 0;
      object-fit: cover; object-position: top;
      display: block;
    }
    .scr-caption {
      background: var(--surf); padding: 7px 11px;
      font-size: 10px; color: var(--muted);
      letter-spacing: .04em;
      border-top: 1px solid rgba(255,255,255,.05);
      flex-shrink: 0;
    }
    .scr-empty {
      flex: 1; display: flex; align-items: center;
      justify-content: center;
      color: rgba(255,255,255,.13); font-size: 11px;
      border: 2px dashed rgba(255,255,255,.07);
      border-radius: 9px; margin: 10px;
      text-align: center; padding: 16px; line-height: 1.7;
    }
    /* ── END SCREENSHOT PANEL ─────────────────────────────── */"""

def ensure_css(html: str) -> str:
    if "scr-panel" in html:
        return html   # already injected
    marker = "    /* ── COVER ─"
    if marker in html:
        return html.replace(marker, SCR_CSS + "\n\n    " + marker.strip() + " ", 1)
    # fallback: insert before </style>
    return html.replace("  </style>", SCR_CSS + "\n  </style>", 1)

# ── BUILD SCR-PANEL HTML ───────────────────────────────────────
def build_scr_panel(key: str, caption: str, b64: str | None) -> str:
    if b64:
        inner = (
            f'<img class="scr-img" '
            f'src="data:image/jpeg;base64,{b64}" alt="{caption}"/>\n'
            f'      <div class="scr-caption">{caption}</div>'
        )
    else:
        inner = (
            f'<div class="scr-empty">'
            f'Screenshot<br><span style="opacity:.6;font-size:9px;">'
            f'{key}.jpg</span></div>'
        )
    return (
        f'\n      <div class="scr-panel" id="scr-{key}">\n'
        f'      {inner}\n'
        f'      </div>'
    )

# ── PATCH FEATURE SLIDES (s4–s9) ──────────────────────────────
def patch_feature_slide(html: str, key: str, caption: str, b64: str | None) -> str:
    slide_id, _ = SLIDES[key]
    new_panel = build_scr_panel(key, caption, b64)

    # If panel already exists -> replace its contents
    panel_pattern = re.compile(
        rf'(<div class="scr-panel" id="scr-{key}">)(.*?)(</div>)',
        re.DOTALL
    )
    if panel_pattern.search(html):
        inner = (
            f'<img class="scr-img" src="data:image/jpeg;base64,{b64}" '
            f'alt="{caption}"/>\n      <div class="scr-caption">{caption}</div>'
            if b64 else
            f'<div class="scr-empty">Screenshot<br>'
            f'<span style="opacity:.6;font-size:9px;">{key}.jpg</span></div>'
        )
        html = panel_pattern.sub(
            rf'\g<1>\n      {inner}\n      \g<3>', html
        )
        return html

    # Panel not yet present — add it and add split--scr class
    # Find the .split div in the correct slide
    # Strategy: find slide section, then find first .split in it
    slide_sec_pat = re.compile(
        rf'(<section class="slide" id="{slide_id}">)(.*?)(</section>)',
        re.DOTALL
    )
    m = slide_sec_pat.search(html)
    if not m:
        print(f"  WARN: slide {slide_id} tidak ditemukan")
        return html

    sec_inner = m.group(2)

    # Add split--scr class to the .split div (only the first one)
    sec_inner = sec_inner.replace(
        '<div class="split"',
        '<div class="split split--scr"',
        1
    )

    # Insert scr-panel before the closing </div> of .split--scr
    # Find last </div></div></div> pattern (split > split-right > last feat)
    # Simpler: find </div>\n    </div> at the end of the split div
    # We insert before the split's closing tag
    close_split = '    </div>\n  </section>'
    if close_split in sec_inner:
        sec_inner = sec_inner.replace(
            close_split,
            new_panel + '\n    </div>\n  </section>',
            1
        )
    else:
        # Fallback: insert before last </div>
        last_close = sec_inner.rfind('</div>')
        sec_inner = sec_inner[:last_close] + new_panel + '\n    ' + sec_inner[last_close:]

    html = html[:m.start()] + m.group(1) + sec_inner + m.group(3) + html[m.end():]
    return html


# ── PATCH DASHBOARD SLIDE (s10) — different layout ────────────
def patch_dashboard_slide(html: str, b64: str | None) -> str:
    key     = "dashboard"
    caption = "Dashboard Monitoring Terpadu"

    new_panel = build_scr_panel(key, caption, b64)

    panel_pattern = re.compile(
        rf'(<div class="scr-panel" id="scr-{key}">)(.*?)(</div>)',
        re.DOTALL
    )
    if panel_pattern.search(html):
        inner = (
            f'<img class="scr-img" src="data:image/jpeg;base64,{b64}" '
            f'alt="{caption}"/>\n      <div class="scr-caption">{caption}</div>'
            if b64 else
            f'<div class="scr-empty">Screenshot<br>'
            f'<span style="opacity:.6;font-size:9px;">{key}.jpg</span></div>'
        )
        return panel_pattern.sub(rf'\g<1>\n      {inner}\n      \g<3>', html)

    # For s10 the layout is .db-mock (not .split), so we append the panel
    # right after the .db-mock closing div, before the .db-legend div
    slide_sec_pat = re.compile(
        r'(<section class="slide" id="s10">)(.*?)(</section>)',
        re.DOTALL
    )
    m = slide_sec_pat.search(html)
    if not m:
        return html

    sec_inner = m.group(2)
    # Find db-legend div and insert scr-panel before it
    if '<div class="db-legend">' in sec_inner:
        sec_inner = sec_inner.replace(
            '\n\n  <div class="db-legend">',
            new_panel + '\n\n  <div class="db-legend">',
            1
        )
    else:
        sec_inner += new_panel

    html = html[:m.start()] + m.group(1) + sec_inner + m.group(3) + html[m.end():]
    return html


# ── MAIN ───────────────────────────────────────────────────────
def main():
    if not HTML.exists():
        sys.exit(f"ERROR: File tidak ditemukan: {HTML}")

    SCR_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nMembaca: {HTML.name}")
    html = HTML.read_text(encoding="utf-8")

    # 1. Inject CSS
    html = ensure_css(html)

    # 2. Process each slide
    found, missing = [], []
    for key, (slide_id, caption) in SLIDES.items():
        scr_path = find_scr(key)
        if scr_path:
            print(f"\n[{slide_id}] {key}: ditemukan -> {scr_path.name}")
            b64 = compress_to_b64(scr_path)
            found.append(key)
        else:
            print(f"[{slide_id}] {key}: belum ada -> placeholder")
            b64 = None
            missing.append(key)

        if key == "dashboard":
            html = patch_dashboard_slide(html, b64)
        else:
            html = patch_feature_slide(html, key, caption, b64)

    # 3. Save
    HTML.write_text(html, encoding="utf-8")
    size_kb = HTML.stat().st_size // 1024

    print(f"\nSelesai! File disimpan: {HTML.name} ({size_kb} KB)")
    print(f"  Screenshot berhasil: {len(found)} slide(s): {', '.join(found) or '-'}")
    if missing:
        print(f"  Placeholder (belum ada screenshot): {', '.join(missing)}")
        print(f"\n  Simpan screenshot ke folder:")
        print(f"  {SCR_DIR}")
        print(f"  dengan nama: {', '.join(k + '.jpg' for k in missing)}")
        print(f"  Lalu jalankan script ini lagi.")

if __name__ == "__main__":
    main()
