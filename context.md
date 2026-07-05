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
│   ├── eform_laka.py
│   ├── jenis_layanan.py
│   ├── loket.py
│   ├── antrian.py
│   ├── display_config.py
│   ├── konseling.py
│   ├── rehab.py
│   ├── barang_bukti.py
│   ├── patroli.py
│   ├── tahti_sel.py                  # Master sel/kamar tahanan
│   ├── tahanan.py                    # Data tahanan Tahti
│   ├── tahti_tamu.py                 # Master data tamu pengunjung
│   └── tahti_kunjungan.py            # Buku tamu / kunjungan
├── controllers/
│   ├── __init__.py
│   ├── display_controller.py         # Controller display antrian
│   └── tahti_public.py               # Kiosk buku tamu (auth=public)
├── views/
│   ├── menu.xml
│   ├── kabupaten_views.xml
│   ├── kecamatan_views.xml
│   ├── desa_views.xml
│   ├── polsek_views.xml
│   ├── eform_laka_views.xml
│   ├── antrian_views.xml
│   ├── loket_views.xml
│   ├── jenis_layanan_views.xml
│   ├── konseling_views.xml
│   ├── rehab_views.xml
│   ├── barang_bukti_views.xml
│   ├── patroli_views.xml
│   ├── dashboard_views.xml
│   ├── display_config_views.xml
│   ├── antrian_display_template.xml
│   ├── tahti_sel_views.xml           # List editable sel/kamar
│   ├── tahanan_views.xml             # Form/list tahanan
│   ├── tahti_tamu_views.xml          # Form/list data tamu
│   ├── tahti_kunjungan_views.xml     # Form/list buku tamu
│   └── tahti_kiosk_template.xml      # HTML template kiosk publik
├── security/
│   ├── security.xml
│   └── ir.model.access.csv
├── data/
│   └── sequence.xml                  # FL, PAT, KSL, RHB, BBK, KUJ, THN
└── static/
    ├── description/icon.png
    ├── img/logo_polda.png
    ├── lib/
    │   ├── leaflet/
    │   ├── leaflet-markercluster/
    │   ├── echart/
    │   └── fontawesome/
    └── src/
        ├── css/
        │   ├── map_widget.css
        │   ├── dashboard.css
        │   └── tahti_kiosk.css       # CSS kiosk publik
        ├── js/
        │   ├── map_widget.js
        │   ├── patroli_map_widget.js
        │   ├── dashboard.js
        │   └── tahti_kiosk.js        # OWL app kiosk publik
        └── xml/
            ├── map_widget.xml
            ├── patroli_map_widget.xml
            └── dashboard.xml
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

### digital_kamtibmas.eform_laka (Satlantas)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto-generated (prefix FL, 5 digit) |
| `kejadian` | Char | Deskripsi kejadian (required) |
| `tanggal_kejadian` | Datetime | Waktu kejadian (default: now) |
| `lat` | Float | Latitude |
| `lng` | Float | Longitude |
| `foto` | Binary | Foto dokumentasi |
| `state` | Selection | BARU / DIPROSES / SELESAI |

### digital_kamtibmas.antrian (Satlantas)

| Field | Tipe | Keterangan |
|---|---|---|
| `nomor_antrian` | Char | Auto-generated (`{CODE}-{NNN}`) |
| `nomor_urut` | Integer | Urutan per layanan per hari |
| `user_id` | Many2one | Pendaftar (res.users) |
| `atas_nama` | Char | Nama penerima layanan |
| `tanggal_booking` | Date | Tanggal booking |
| `loket_id` | Many2one | → loket |
| `state` | Selection | menunggu / konfirmasi / dipanggil / selesai / batal |

### digital_kamtibmas.konseling (Satnarkoba)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto (prefix KSL) |
| `nama` | Char | Nama pemohon |
| `nik` | Char | NIK 16 digit |
| `jenis_masalah` | Selection | penyalahgunaan / ketergantungan / pencegahan / pasca_rehab / konsultasi / lainnya |
| `tanggal_jadwal` | Datetime | Jadwal konseling |
| `state` | Selection | menunggu / konfirmasi / proses / selesai |

### digital_kamtibmas.rehab (Satnarkoba)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto (prefix RHB) |
| `nama` | Char | Nama pemohon |
| `nik` | Char | NIK 16 digit |
| `jenis_narkoba` | Char | Jenis narkoba/zat |
| `tanggal_jadwal` | Datetime | Jadwal rehab |
| `state` | Selection | menunggu / konfirmasi / proses / selesai |

### digital_kamtibmas.barang_bukti (Satreskrim)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto (prefix BBK) |
| `nomor_perkara` | Char | No. Perkara / SP3 |
| `jenis_perkara` | Selection | pencurian / penipuan / penganiayaan / narkoba / korupsi / cybercrime / kesusilaan / pembunuhan / lainnya |
| `nama_pelapor` | Char | Nama pelapor (required) |
| `item_ids` | One2many | → barang_bukti_item |
| `state` | Selection | diterima / disimpan / diproses / dikembalikan / dimusnahkan |

### digital_kamtibmas.patroli (Sabhara)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto (prefix PAT) |
| `tanggal_patroli` | Datetime | Tanggal mulai (required) |
| `tanggal_selesai` | Datetime | Tanggal selesai |
| `kecamatan_id` | Many2one | → kecamatan |
| `desa_id` | Many2one | → desa |
| `personel_ids` | One2many | → patroli_personel |
| `titik_ids` | One2many | → patroli_titik (GPS points) |
| `state` | Selection | menunggu / berjalan / selesai |

---

## Tahti — Model

### digital_kamtibmas.tahti_sel

Master sel/kamar penahanan. View: list editable, tanpa form.

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama sel (required) |
| `jenis` | Selection | pria / wanita / anak |
| `kapasitas` | Integer | Kapasitas maksimal |
| `keterangan` | Text | Catatan tambahan |

> Tidak ada computed field. `jenis` di list **tidak boleh** pakai `widget="badge"` karena display-only — cukup `<field name="jenis"/>` agar tetap editable.

### digital_kamtibmas.tahanan

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto (prefix THN, 5 digit) |
| `nama` | Char | Nama lengkap (required) |
| `nik` | Char | NIK (size 16) |
| `jenis_kelamin` | Selection | laki / perempuan |
| `tanggal_lahir` | Date | Tanggal lahir |
| `alamat` | Text | Alamat |
| `foto` | Image | max 512×512 |
| `nomor_perkara` | Char | No. perkara |
| `jenis_perkara` | Selection | 9 opsi (pencurian..lainnya) |
| `pasal` | Char | Pasal yang disangkakan |
| `penyidik_id` | Many2one | → res.users |
| `tanggal_masuk` | Date | Tanggal masuk (required, default today) |
| `tanggal_keluar` | Date | Tanggal keluar |
| `sel_id` | Many2one | → tahti_sel (ondelete: set null) |
| `state` | Selection | ditahan / bebas |
| `kunjungan_count` | Integer | Computed (count kunjungan) |

**Actions**: `action_bebaskan()`, `action_tahan_kembali()`

### digital_kamtibmas.tahti_tamu

Master data pengunjung. NIK wajib unik (SQL constraint).

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `nama` | Char | Nama lengkap (required) |
| `nik` | Char | NIK 16 digit (required, **unique**) |
| `no_hp` | Char | No. HP/WA |
| `alamat` | Text | Alamat |
| `foto_ktp` | Image | max 800×600 |
| `kunjungan_ids` | One2many | → tahti_kunjungan |
| `kunjungan_count` | Integer | Computed |

**Override**: `name_get()` → `"[NIK] Nama"`, `name_search()` → cari NIK atau nama

### digital_kamtibmas.tahti_kunjungan

Buku tamu (log kunjungan). Tiap record = 1 kunjungan.

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto (prefix KUJ, 5 digit) |
| `tamu_id` | Many2one | → tahti_tamu (required, ondelete: restrict) |
| `tahanan_id` | Many2one | → tahanan (required, ondelete: restrict) |
| `hubungan` | Selection | keluarga / pengacara / teman / lainnya |
| `keperluan` | Text | Tujuan kunjungan |
| `waktu_masuk` | Datetime | Waktu masuk (required, default now) |
| `waktu_keluar` | Datetime | Waktu keluar |
| `petugas_id` | Many2one | → res.users (default current user) |
| `state` | Selection | berlangsung / selesai |
| `tamu_nik` | Char | Related from tamu_id.nik (store=True) |
| `tamu_no_hp` | Char | Related from tamu_id.no_hp |

**Actions**: `action_selesaikan()`, `action_buka_kembali()`

---

## Tahti — Search Filter "Hari Ini" (Timezone WIB)

`waktu_masuk` disimpan UTC. Filter harus menggeser batas ke WIB (-7h):

```xml
<filter string="Hari Ini" name="f_hari_ini"
        domain="[
            ('waktu_masuk','&gt;=',(datetime.datetime.combine(context_today(), datetime.time(0,0,0)) - datetime.timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')),
            ('waktu_masuk','&lt;', (datetime.datetime.combine(context_today() + datetime.timedelta(days=1), datetime.time(0,0,0)) - datetime.timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S'))
        ]"/>
```

> Offset -7h di-hardcode karena sistem khusus Palembang (WIB/UTC+7).

---

## Tahti — Kiosk Web App

Route publik: `/tahti/buku-tamu` — tablet/kiosk di depan pintu Tahti.

### Controller (`controllers/tahti_public.py`)

| Route | Method | Auth | Fungsi |
|---|---|---|---|
| `/tahti/buku-tamu` | HTTP | public | Render halaman kiosk |
| `/tahti/api/cari_tahanan` | jsonrpc | public | Cari tahanan aktif (`state=ditahan`) |
| `/tahti/api/cek_nik` | jsonrpc | public | Cek tamu by NIK, return data jika ada |
| `/tahti/api/daftar_kunjungan` | jsonrpc | public | Buat/update tamu + buat kunjungan baru |

`api_daftar_kunjungan` logic:
1. Validasi tahanan masih `ditahan`
2. Cari tamu by NIK → jika tidak ada, buat baru
3. Jika ada tapi data berubah (nama/hp) → update
4. Buat record `tahti_kunjungan` dengan `waktu_masuk` = UTC now
5. Return `code`, `tamu_nama`, `tahanan_nama`

### OWL App (`static/src/js/tahti_kiosk.js`)

Pattern: IIFE, OWL 2 standalone, single Component.

**Alur fase** (`state.phase`):

| Fase | Layar |
|---|---|
| `idle` | Fullscreen dark (logo, jam real-time, "Sentuh untuk mulai") |
| `cari_tahanan` | Search tahanan + list hasil (langkah 1/3) |
| `data_tamu` | Input NIK (auto-lookup 16 digit), nama, HP, hubungan chips, keperluan (langkah 2/3) |
| `konfirmasi` | Summary ringkasan + tombol submit (langkah 3/3) |
| `sukses` | Fullscreen hijau, nomor kunjungan, countdown 10 detik → idle |

**Penting — OWL XML template di JS**: Tidak boleh pakai HTML named entities (`&nbsp;`, `&mdash;`). Gunakan numeric: `&#160;`, `&#8212;`, atau karakter literal `—`.

**CSS**: `static/src/css/tahti_kiosk.css` — Odoo-style, ungu `#714B67`, Standalone (tidak masuk `web.assets_backend`), dimuat via `<link>` di template HTML.

### Template HTML (`views/tahti_kiosk_template.xml`)

```xml
<template id="tahti_kiosk_template" name="Buku Tamu Tahti — Kiosk">
    <html lang="id">
        <head>...</head>
        <body>
            <div id="tahti-kiosk-app"/>
            <script src="/web/static/lib/owl/owl.js"/>
            <script src="/digital_kamtibmas/static/src/js/tahti_kiosk.js"/>
        </body>
    </html>
</template>
```

> Template ini di-register di `__manifest__.py` → `data: [...]`, bukan di `assets`.
> File JS/CSS kiosk **tidak** masuk `web.assets_backend`.

---

## Menu Struktur

```
Digital Kamtibmas (root, sequence 2)
├── Dashboard                           [admin, operator]
├── Satlantas
│   ├── e-Form Laka                     [admin, operator]
│   └── Antrian Layanan                 [admin, operator]
├── Satnarkoba
│   ├── Konseling Online                [admin, operator]
│   └── Permohonan Rehabilitasi         [admin, operator]
├── Satreskrim
│   └── Barang Bukti                    [admin, operator]
├── Sabhara
│   └── Patroli                         [admin, operator]
├── Tahti (sequence 50)
│   ├── Data Tahanan                    [admin, operator]   (filter default: ditahan)
│   ├── Semua Tahanan                   [admin, operator]
│   ├── Buku Tamu                       [admin, operator]   (filter default: hari ini)
│   └── Data Tamu                       [admin, operator]
└── Configuration                       [admin only]
    ├── Polsek
    ├── Kabupaten
    ├── Kecamatan
    ├── Desa/Kelurahan
    └── Sel/Kamar Tahanan (sequence 20)
```

---

## Security

### Struktur

```
ir.module.category (module_category_dkm)
  └── res.groups.privilege (privilege_dkm_access)
        ├── res.groups: Admin    (group_dkm_admin)
        └── res.groups: Operator (group_dkm_operator)
```

> Di Odoo 19 model privilege adalah `res.groups.privilege` (bukan `res.privilege`).

### Akses Model Tahti

| Model | Admin | Operator |
|---|---|---|
| `tahti_sel` | CRUD | R |
| `tahanan` | CRUD | CRU (no delete) |
| `tahti_tamu` | CRUD | CRU (no delete) |
| `tahti_kunjungan` | CRUD | CRU (no delete) |

---

## Sequences (`data/sequence.xml`)

| ID | Code | Prefix | Padding |
|---|---|---|---|
| `seq_eform_laka` | `digital_kamtibmas.eform_laka.sequence` | FL | 5 |
| `seq_patroli` | `digital_kamtibmas.patroli` | PAT | 5 |
| `seq_konseling` | `digital_kamtibmas.konseling` | KSL | 5 |
| `seq_rehab` | `digital_kamtibmas.rehab` | RHB | 5 |
| `seq_barang_bukti` | `digital_kamtibmas.barang_bukti` | BBK | 5 |
| `seq_tahti_kunjungan` | `digital_kamtibmas.tahti_kunjungan` | KUJ | 5 |
| `seq_tahanan` | `digital_kamtibmas.tahanan` | THN | 5 |

---

## Frontend Assets

### Map Widget (OWL: `DkmMapPicker`)

- Widget name: `dkm_map_picker` (untuk field `float`)
- Library: Leaflet.js
- Center default: Palembang `[-2.9761, 104.7754]`, zoom 13
- Fitur: click-to-pick, drag marker, display lat/lng 6 desimal

### Patroli Route Map Widget (OWL: `PatroliRouteMap`)

Digunakan di form view `digital_kamtibmas.patroli`.

- Marker bernomor urut (1, 2, 3, ...)
- Garis rute putus-putus (`dashArray: '10, 7'`), tanpa panah
- Header: jumlah titik valid (badge `.dkm-rmap-count`)
- Popup: keterangan, waktu rekam, lat/lng

### Dashboard (OWL: `DkmDashboard`)

- Client action tag: `digital_kamtibmas.dashboard`
- Libraries: Leaflet.js + ECharts

---

## Dashboard — Multi-Seksi

Sidebar kiri, `state.activeSection` mengontrol seksi aktif.

| Seksi | Icon | Load Method |
|---|---|---|
| `satlantas` | fa-car | `loadData()` (on mount) |
| `satnarkoba` | fa-medkit | `loadSatnarkoba()` |
| `satreskrim` | fa-search | `loadSatreskrim()` |
| `sabhara` | fa-binoculars | `loadSabhara()` |
| `tahti` | fa-institution | `loadTahti()` |

### Tahti Dashboard

**KPI Cards** (4 cards, `dkm-kpi-card`):

| KPI | Icon | Color | Action |
|---|---|---|---|
| Kunjungan Hari Ini | fa-calendar-check-o | blue | openKunjunganList |
| Total Kunjungan | fa-book | purple | openKunjunganList |
| Total Tamu | fa-users | teal | — |
| Tahanan Aktif | fa-lock | orange | openTahananList(ditahan) |

**Charts** (ECharts):

| Ref | Chart | Data |
|---|---|---|
| `thTrendChart` | Bar | Kunjungan 7 hari terakhir (WIB-aware grouping) |
| `thHubChart` | Donut (`pie` radius 42%-68%) | Distribusi hubungan tamu |
| `thPerkaraChart` | Pie (filled) | Jenis perkara tahanan aktif |
| `thSelChart` | Stacked bar horizontal | Terisi vs sisa kapasitas per sel |

**Tabel**: 5 kunjungan terakhir (dibungkus `dkm-panel` + `dkm-panel-header`)

**WIB-aware aggregation** (7-day trend):

```js
const nowWib       = new Date(Date.now() + 7 * 3600000);
const todayStartMs = Date.UTC(nowWib.getUTCFullYear(), nowWib.getUTCMonth(), nowWib.getUTCDate()) - 7 * 3600000;
// setiap record: _wib(r.waktu_masuk).getUTCFullYear/Month/Date() untuk WIB date key
```

### Sabhara Live Map

- Auto-refresh setiap 30 detik via `setInterval`
- Pulsing marker oranye `#f59e0b` dengan animasi ring `dkm-ring`
- `.dkm-live-marker` **wajib** `position: relative` — tanpa ini ring pulse keluar container

---

## Dashboard — KPI Card Styles

### Standar (`dkm-kpi-card`)

```html
<div class="dkm-kpi-card">
  <div class="dkm-kpi-icon dkm-kpi-icon--purple"><i class="fa fa-..."/></div>
  <div class="dkm-kpi-body">
    <div class="dkm-kpi-value">123</div>
    <div class="dkm-kpi-label">Label</div>
    <div class="dkm-kpi-sub">Sub-label</div>
  </div>
</div>
```

**Warna icon tersedia**: `--purple`, `--blue`, `--orange`, `--green`, `--gray`, `--teal`

### Gradient (`dkm-laka-card`)

Background gradient, ikon dekoratif opacity 0.10 di pojok kanan bawah, progress bar mini.

**Warna**: `--purple`, `--blue`, `--orange`, `--green`, `--slate`, `--amber`

---

## Dashboard — Table Card Pattern

Tabel terbaru selalu dibungkus `dkm-panel` + `dkm-panel-header`:

```xml
<div class="dkm-panel" style="margin-bottom:20px;">
    <div class="dkm-panel-header">
        <span><i class="fa fa-list" style="color:#714B67; margin-right:6px;"/> Judul</span>
        <span class="dkm-count-badge dkm-count-badge--blue" t-esc="data.length"/>
    </div>
    <table class="dkm-table">...</table>
</div>
```

> **Jangan** pakai `dkm-table-card` — class tersebut tidak ada di CSS.

---

## Views — Hal Penting Odoo 19

- `<group>` dalam `<search>` **tidak** support atribut `expand` dan `string`
- `widget="badge"` di list view bersifat **read-only** — tidak bisa dipakai di kolom editable
- `invisible` di button/field menggunakan **Python expression string**: `invisible="state != 'berlangsung'"`

---

## Frontend — Pola Umum

### Timezone (WIB = UTC+7)

```js
_wib(dtStr) {
    const d = new Date(String(dtStr).replace(' ', 'T') + 'Z');
    return isNaN(d.getTime()) ? null : new Date(d.getTime() + 7 * 3600 * 1000);
}
_fmtWib(dtStr) {
    if (!dtStr) return '-';
    const w = this._wib(dtStr);
    if (!w) return '-';
    const p = n => String(n).padStart(2, '0');
    return `${w.getUTCFullYear()}-${p(w.getUTCMonth()+1)}-${p(w.getUTCDate())} ${p(w.getUTCHours())}:${p(w.getUTCMinutes())}`;
}
```

### Inisialisasi Leaflet Setelah OWL Render

```js
this.state.sabhara.loading = false;
setTimeout(() => this._initSabharaLiveMap(), 120);
```

### OWL XML Template — Named Entities

OWL XML parser **tidak** mengenal HTML named entities. Gunakan numeric:

| Salah | Benar |
|---|---|
| `&nbsp;` | `&#160;` |
| `&mdash;` | `—` atau `&#8212;` |
| `&rarr;` | `→` atau `&#8594;` |

### Sidebar Scroll (Flexbox)

```css
.sidebar-list {
    height: 100%;
    min-height: 0;   /* wajib agar flex item bisa shrink */
    overflow-y: auto;
}
```

---

## Color Scheme

| Elemen | Warna |
|---|---|
| Background | `#f8f9fa` |
| Brand/Primary | `#71639e` (dashboard) / `#714B67` (kiosk/tahti) |
| KPI icon purple bg | `#f0eff5` |
| Card shadow | `0 1px 4px rgba(0,0,0,0.07)` |
| Card radius | `4px` |
| Live map header | `#1e1b4b` |
| Pulse marker | `#f59e0b` |
| BERLANGSUNG badge | `#fef3c7` / `#92400e` |
| SELESAI badge | `#d1fae5` / `#065f46` |

---

## Changelog

| Versi | Fitur |
|---|---|
| 1.0.0 | Initial: Satlantas (e-Form Laka, Antrian), Satnarkoba, Satreskrim, Sabhara, Dashboard 4 seksi |
| 1.1.0 | Sabhara Live Patrol Map + Route Visualization |
| 1.2.0 | Tahti: Master Sel, Data Tahanan, Buku Tamu (Tamu + Kunjungan), Menu Tahti |
| 1.3.0 | Kiosk Web App (`/tahti/buku-tamu`) — OWL standalone, auth=public |
| 1.4.0 | Dashboard Tahti — KPI, trend 7 hari, pie perkara, stacked bar kapasitas sel, tabel kunjungan |
