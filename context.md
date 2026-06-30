# Digital Kamtibmas — Project Context

## Identitas Modul

| Properti | Nilai |
|---|---|
| Nama | Digital Kamtibmas |
| Versi | 19.0.1.0.0 |
| Author | CV Sel Studio |
| Website | https://selstudio.id |
| Kategori | Tools |
| License | LGPL-3 |
| Tujuan | Sistem Informasi Digital Kamtibmas Polrestabes Palembang |
| Dependensi | `base`, `web`, `mail` |
| Post-init Hook | Migrasi data dari modul `petadigi` |

---

## Struktur Direktori

```
digital_kamtibmas/
├── __init__.py
├── __manifest__.py
├── hooks.py                          # Migrasi data dari petadigi
├── context.md                        # Dokumentasi proyek ini
├── models/
│   ├── __init__.py
│   ├── kabupaten.py
│   ├── kecamatan.py
│   ├── desa.py
│   ├── polsek.py
│   └── eform_laka.py
├── views/
│   ├── menu.xml
│   ├── kabupaten_views.xml
│   ├── kecamatan_views.xml
│   ├── desa_views.xml
│   ├── polsek_views.xml
│   ├── eform_laka_views.xml
│   └── dashboard_views.xml
├── security/
│   ├── security.xml                  # Grup, privilege & module category
│   └── ir.model.access.csv
├── data/
│   └── sequence.xml                  # Sequence FL00001, FL00002, ...
└── static/
    ├── description/icon.png
    ├── lib/
    │   ├── leaflet/                  # Peta interaktif
    │   └── echart/                   # Chart visualisasi
    └── src/
        ├── css/map_widget.css
        ├── css/dashboard.css
        ├── js/map_widget.js
        ├── js/dashboard.js
        ├── xml/map_widget.xml
        └── xml/dashboard.xml
```

---

## Model & Relasi

### Hierarki Wilayah

```
digital_kamtibmas.kabupaten
  └── One2many → digital_kamtibmas.kecamatan
        ├── One2many → digital_kamtibmas.desa
        └── One2many → digital_kamtibmas.polsek
```

### digital_kamtibmas.kabupaten

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama Kabupaten/Kota (required) |
| `code` | Char | Kode wilayah |
| `type` | Selection | KABUPATEN / KOTA |
| `geometry` | Text | GeoJSON geometry |
| `kecamatan_ids` | One2many | Relasi ke kecamatan |
| `kecamatan_count` | Integer | Computed, stored |

### digital_kamtibmas.kecamatan

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama Kecamatan (required) |
| `code` | Char | Kode wilayah |
| `kabupaten_id` | Many2one | → kabupaten (on_delete: restrict) |
| `geometry` | Text | GeoJSON geometry |
| `desa_ids` | One2many | Relasi ke desa |
| `desa_count` | Integer | Computed, stored |

### digital_kamtibmas.desa

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama Desa/Kelurahan (required) |
| `code` | Char | Kode wilayah |
| `type` | Selection | DESA / KELURAHAN |
| `kecamatan_id` | Many2one | → kecamatan (on_delete: restrict) |
| `kabupaten_id` | Many2one | Related via kecamatan (stored, readonly) |
| `geometry` | Text | GeoJSON geometry |

> **Catatan**: Field nama `code` dan `type` disesuaikan dengan konvensi petadigi (bukan `kode`/`tipe`).

### digital_kamtibmas.polsek

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama Polsek (required) |
| `kecamatan_id` | Many2one | → kecamatan (on_delete: restrict) |
| `kabupaten_id` | Many2one | Related via kecamatan (stored, readonly) |

> **Catatan**: Polsek tidak memiliki field `code` karena `petadigi.polsek` tidak menyediakan field tersebut.

### digital_kamtibmas.eform_laka

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan | Tracking |
|---|---|---|---|
| `code` | Char | Auto-generated (prefix FL, 5 digit) | - |
| `kejadian` | Char | Deskripsi kejadian (required) | Ya |
| `keterangan` | Text | Keterangan detail | - |
| `tanggal_kejadian` | Datetime | Waktu kejadian (required, default: now) | Ya |
| `lat` | Float | Latitude (6 desimal) | - |
| `lng` | Float | Longitude (6 desimal) | - |
| `foto` | Binary | Foto dokumentasi (attachment) | - |
| `foto_filename` | Char | Nama file foto | - |
| `state` | Selection | BARU / DIPROSES / SELESAI (default: BARU) | Ya |

**State workflow**:
```
BARU → DIPROSES → SELESAI
         ↑___________↓  (reset ke BARU)
```

**Methods**:
- `create()` — auto-generate kode dari sequence
- `action_set_diproses()` — transisi ke DIPROSES
- `action_set_selesai()` — transisi ke SELESAI
- `action_set_baru()` — reset ke BARU

---

## Security & Akses

### Struktur Security (Odoo 19)

```
ir.module.category (module_category_dkm)
  └── res.groups.privilege (privilege_dkm_access)   ← bukan res.privilege
        ├── res.groups: Admin  (group_dkm_admin)
        └── res.groups: Operator (group_dkm_operator)
```

> **Penting**: Di Odoo 19, model privilege adalah `res.groups.privilege` (bukan `res.privilege`).
> Privilege wajib memiliki `category_id` yang merujuk ke `ir.module.category`.

### Access Control Matrix

| Model | Admin | Operator |
|---|---|---|
| eform_laka | CRUD + Delete | Create + Read + Write |
| kabupaten | CRUD + Delete | Read only |
| kecamatan | CRUD + Delete | Read only |
| desa | CRUD + Delete | Read only |
| polsek | CRUD + Delete | Read only |

---

## Views — Hal Penting Odoo 19

Tag `<group>` dalam `<search>` view **tidak mendukung** atribut `expand` dan `string`.
Gunakan `<group>` polos tanpa atribut:

```xml
<!-- BENAR (Odoo 19) -->
<group>
    <filter string="..." .../>
</group>

<!-- SALAH — akan ParseError -->
<group expand="0" string="Kelompokkan">
```

---

## Menu Struktur

```
Digital Kamtibmas (root, sequence 2)
├── Dashboard                         [admin, operator]
├── Satlantas
│   └── e-Form Laka                   [admin, operator]
└── Configuration                     [admin only]
    ├── Polsek
    ├── Kabupaten
    ├── Kecamatan
    └── Desa/Kelurahan
```

---

## Frontend Assets

### Map Widget (OWL Component: DkmMapPicker)

- **File**: [static/src/js/map_widget.js](static/src/js/map_widget.js)
- **Template**: [static/src/xml/map_widget.xml](static/src/xml/map_widget.xml)
- **Field widget name**: `dkm_map_picker` (untuk field tipe `float`)
- **Library**: Leaflet.js
- **Center default**: Palembang [-2.9761, 104.7754], zoom 13
- **Fitur**: Click-to-pick koordinat, drag marker, display lat/lng 6 desimal
- **Tile**: OpenStreetMap

### Dashboard (OWL Component: DkmDashboard)

- **File**: [static/src/js/dashboard.js](static/src/js/dashboard.js)
- **Template**: [static/src/xml/dashboard.xml](static/src/xml/dashboard.xml)
- **CSS**: [static/src/css/dashboard.css](static/src/css/dashboard.css)
- **Client action tag**: `digital_kamtibmas.dashboard`
- **Libraries**: Leaflet.js (peta), ECharts (grafik)

**State utama**:

```javascript
state: {
    period: 'this_month',   // this_month | last_month | this_year | all_time
    loading: true,
    kpi: { total, baru, diproses, selesai },
    trendData: [],          // 6 bulan terakhir untuk line chart
    recentData: [],         // 5 e-form laka terbaru
    pendingData: [],        // e-form laka BARU + DIPROSES (max 10)
    lakaPoints: [],         // Points untuk map markers
}

mapState: {
    drillLevel: 'kecamatan',  // 'kecamatan' | 'desa'
    activeKecId: null,
    kecName: '',
}
```

**Komponen dashboard**:
1. KPI Cards (4): Total, Baru, Diproses, Selesai — clickable, filter ke list
2. Trend Chart: Line chart 6 bulan (ECharts)
3. Status Distribution: Pie chart (ECharts)
4. Leaflet Map: Geometry kecamatan/desa + markers e-form laka, drill-down support
5. Tabel e-Form Terbaru: 5 record terbaru
6. Tabel Membutuhkan Tindakan: BARU + DIPROSES, max 10

**Drill-down Map**:
- Level 1 (`drillLevel: 'kecamatan'`): Geometry semua kecamatan, klik → drill down
- Level 2 (`drillLevel: 'desa'`): Geometry desa dalam kecamatan aktif
- Field yang di-fetch dari `digital_kamtibmas.desa`: `['id', 'name', 'type', 'geometry']`

**Responsive breakpoints**:
- Desktop > 1200px: 4 KPI, chart 3fr+2fr, 2-col panel
- Tablet 640–1200px: 2 KPI, 1-col chart, 2-col panel
- Mobile < 640px: 1 KPI, 1-col chart, 1-col panel

---

## Color Scheme (Dashboard CSS)

Mengadopsi gaya **omni_referral_base** — clean, minimal, elegan.

| Elemen | Warna | Keterangan |
|---|---|---|
| Background | `#f8f9fa` | Netral (bukan purple tint) |
| Brand/Primary | `#71639e` | Purple elegan (dari omni style) |
| KPI icon purple bg | `#f0eff5` | Light purple |
| Card shadow | `0 1px 4px rgba(0,0,0,0.07)` | Subtle |
| Card radius | `0.25rem` (4px) | Minimal |
| Header radius | `10px` | Sedikit rounded |
| Text heading | `#1f2937` | Charcoal |
| Text secondary | `#6b7280` | Gray |
| BARU | `#dbeafe` / `#1d4ed8` | Biru |
| DIPROSES | `#fef3c7` / `#92400e` | Orange |
| SELESAI | `#d1fae5` / `#065f46` | Hijau |

---

## Sequence

| Sequence | Prefix | Padding | Contoh |
|---|---|---|---|
| `digital_kamtibmas.eform_laka.sequence` | `FL` | 5 | FL00001 |

---

## hooks.py (Post-init Migration)

Dijalankan sekali saat install modul. Memigrasi data wilayah dari modul `petadigi` jika tersedia.

**Mapping field petadigi → digital_kamtibmas**:

| petadigi field | dkm field | Model |
|---|---|---|
| `src.name` | `name` | semua |
| `src.code` | `code` | kabupaten, kecamatan, desa |
| `src.type` | `type` | kabupaten, desa |
| `src.geometry` | `geometry` | kabupaten, kecamatan, desa |
| — | — | polsek tidak ada field code |

> **Catatan**: `petadigi.polsek` hanya memiliki `name`, `address`, `polres_id` — tidak ada `code`.

**Alur**:
1. Cek ketersediaan model `petadigi.kabupaten` → jika tidak ada, skip
2. Copy Kabupaten (filter: `polres_id.name ilike 'Palembang'`)
3. Copy Kecamatan (filter: `kabupaten_id in kab_map`)
4. Copy Desa (filter: `kecamatan_id in kec_map`)
5. Copy Polsek (filter: `polres_id.name ilike 'Palembang'`, ambil kecamatan dari `kecamatan_ids[0]`)

---

## File Kunci

| File | Peran |
|---|---|
| [models/eform_laka.py](models/eform_laka.py) | Model utama bisnis + workflow state |
| [models/kabupaten.py](models/kabupaten.py) | Master wilayah (field: `code`, `type`) |
| [models/desa.py](models/desa.py) | Master desa (field: `code`, `type`) |
| [static/src/js/dashboard.js](static/src/js/dashboard.js) | Dashboard OWL + peta + chart |
| [static/src/css/dashboard.css](static/src/css/dashboard.css) | Styling dashboard (gaya omni_referral_base) |
| [static/src/js/map_widget.js](static/src/js/map_widget.js) | Custom field widget peta |
| [views/eform_laka_views.xml](views/eform_laka_views.xml) | UI form + list e-form laka |
| [views/menu.xml](views/menu.xml) | Struktur menu aplikasi |
| [security/security.xml](security/security.xml) | Privilege (`res.groups.privilege`) + kategori modul |
| [security/ir.model.access.csv](security/ir.model.access.csv) | Hak akses per model per grup |
| [hooks.py](hooks.py) | Migrasi data dari petadigi |

---

## Changelog Perbaikan

| # | File | Perubahan |
|---|---|---|
| 1 | `security/security.xml` | Model privilege `res.privilege` → `res.groups.privilege`; tambah `ir.module.category` dan field `category_id` |
| 2 | `views/polsek_views.xml` | `<group expand="0" string="...">` → `<group>` |
| 3 | `views/desa_views.xml` | `<group expand="0" string="...">` → `<group>` |
| 4 | `views/kecamatan_views.xml` | `<group expand="0" string="...">` → `<group>` |
| 5 | `models/kabupaten.py` | Field `kode` → `code`, `tipe` → `type` |
| 6 | `models/kecamatan.py` | Field `kode` → `code` |
| 7 | `models/desa.py` | Field `kode` → `code`, `tipe` → `type` |
| 8 | `models/polsek.py` | Hapus field `code` (tidak ada di petadigi.polsek) |
| 9 | `hooks.py` | Gunakan `src.code`/`src.type` (sesuai petadigi); hapus `code` dari create polsek |
| 10 | `views/*_views.xml` | Semua referensi `kode`→`code`, `tipe`→`type` di 4 file views |
| 11 | `static/src/js/dashboard.js` | Field desa `'tipe'` → `'type'` pada `searchRead` |
| 12 | `static/src/css/dashboard.css` | Redesign: gaya omni_referral_base (bg `#f8f9fa`, radius `0.25rem`, shadow halus, brand `#71639e`) |
