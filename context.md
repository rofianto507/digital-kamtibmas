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
│   ├── eform_laka.py
│   ├── jenis_layanan.py
│   ├── loket.py
│   ├── antrian.py
│   ├── display_config.py
│   ├── konseling.py
│   ├── rehab.py
│   ├── barang_bukti.py
│   └── patroli.py
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
│   └── sequence.xml                  # Sequences FL, PAT, KON, REH, BB, dsb.
└── static/
    ├── description/icon.png
    ├── img/logo_polda.png
    ├── lib/
    │   ├── leaflet/                  # Peta interaktif
    │   └── echart/                   # Chart visualisasi
    └── src/
        ├── css/map_widget.css
        ├── css/dashboard.css
        ├── js/map_widget.js
        ├── js/patroli_map_widget.js
        ├── js/dashboard.js
        ├── xml/map_widget.xml
        ├── xml/patroli_map_widget.xml
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

### digital_kamtibmas.polsek

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama Polsek (required) |
| `kecamatan_id` | Many2one | → kecamatan (on_delete: restrict) |
| `kabupaten_id` | Many2one | Related via kecamatan (stored, readonly) |

> Polsek tidak memiliki field `code` karena `petadigi.polsek` tidak menyediakan field tersebut.

### digital_kamtibmas.eform_laka (Satlantas)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto-generated (prefix FL, 5 digit) |
| `kejadian` | Char | Deskripsi kejadian (required) |
| `keterangan` | Text | Keterangan detail |
| `tanggal_kejadian` | Datetime | Waktu kejadian (required, default: now) |
| `lat` | Float | Latitude (6 desimal) |
| `lng` | Float | Longitude (6 desimal) |
| `foto` | Binary | Foto dokumentasi (attachment) |
| `state` | Selection | BARU / DIPROSES / SELESAI |

**State workflow**: `BARU → DIPROSES → SELESAI → BARU`

### digital_kamtibmas.jenis_layanan

Master jenis layanan antrian Satlantas (SIM, STNK, BPKB, dsb.)

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama layanan (required) |
| `code` | Char | Kode singkat (untuk nomor antrian) |

### digital_kamtibmas.loket

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama loket |
| `layanan_id` | Many2one | → jenis_layanan |
| `kuota` | Integer | Kuota antrian per hari |
| `state` | Selection | aktif / nonaktif |

### digital_kamtibmas.antrian (Satlantas)

| Field | Tipe | Keterangan |
|---|---|---|
| `nomor_antrian` | Char | Auto-generated (format: `{CODE}-{NNN}`) |
| `nomor_urut` | Integer | Urutan per layanan per hari |
| `user_id` | Many2one | Pendaftar (res.users) |
| `atas_nama` | Char | Nama penerima layanan |
| `tanggal_booking` | Date | Tanggal booking |
| `loket_id` | Many2one | → loket |
| `layanan_id` | Many2one | Related from loket (stored) |
| `state` | Selection | menunggu / konfirmasi / dipanggil / selesai / batal |
| `catatan` | Text | Catatan |

**State workflow**: `menunggu → konfirmasi → dipanggil → selesai`
**Validasi**: Kuota loket dicek saat konfirmasi; loket nonaktif tidak bisa dipilih.

### digital_kamtibmas.konseling (Satnarkoba)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto-generated |
| `nama` | Char | Nama lengkap pemohon |
| `nik` | Char | NIK (16 digit) |
| `no_hp` | Char | No. HP/WA |
| `jenis_kelamin` | Selection | laki-laki / perempuan |
| `jenis_masalah` | Selection | penyalahgunaan / ketergantungan / pencegahan / pasca_rehab / konsultasi / lainnya |
| `sumber_rujukan` | Selection | mandiri / keluarga / sekolah / instansi / lainnya |
| `tanggal_jadwal` | Datetime | Jadwal konseling |
| `state` | Selection | menunggu / konfirmasi / proses / selesai |

### digital_kamtibmas.rehab (Satnarkoba)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto-generated |
| `nama` | Char | Nama lengkap pemohon |
| `nik` | Char | NIK (16 digit) |
| `jenis_narkoba` | Char | Jenis narkoba/zat |
| `lama_penggunaan` | Char | Durasi penggunaan |
| `tanggal_jadwal` | Datetime | Jadwal rehab |
| `state` | Selection | menunggu / konfirmasi / proses / selesai |

### digital_kamtibmas.barang_bukti (Satreskrim)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto-generated |
| `nomor_perkara` | Char | No. Perkara / SP3 |
| `jenis_perkara` | Selection | pencurian / penipuan / penganiayaan / narkoba / korupsi / cybercrime / pemerkosaan / pembunuhan / lainnya |
| `nama_pelapor` | Char | Nama pelapor / pemilik (required) |
| `item_ids` | One2many | → barang_bukti_item |
| `lokasi_penyimpanan` | Char | Nomor rak / ruangan |
| `state` | Selection | diterima / disimpan / diproses / dikembalikan / dimusnahkan |

### digital_kamtibmas.patroli (Sabhara)

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto-generated (prefix PAT) |
| `tanggal_patroli` | Datetime | Tanggal mulai patroli (required) |
| `tanggal_selesai` | Datetime | Tanggal selesai |
| `kecamatan_id` | Many2one | → kecamatan |
| `desa_id` | Many2one | → desa (domain: kecamatan) |
| `keterangan` | Text | Keterangan / rute |
| `personel_ids` | One2many | → patroli_personel |
| `titik_ids` | One2many | → patroli_titik |
| `state` | Selection | menunggu / berjalan / selesai |

**State workflow**: `menunggu → berjalan → selesai`

### digital_kamtibmas.patroli_personel

| Field | Tipe | Keterangan |
|---|---|---|
| `patroli_id` | Many2one | → patroli (cascade) |
| `nama` | Char | Nama personel |
| `pangkat` | Char | Pangkat |
| `sequence` | Integer | Urutan |

### digital_kamtibmas.patroli_titik

| Field | Tipe | Keterangan |
|---|---|---|
| `patroli_id` | Many2one | → patroli (cascade) |
| `waktu_rekam` | Datetime | Waktu rekam GPS |
| `latitude` | Float | Latitude (10,6) |
| `longitude` | Float | Longitude (10,6) |

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
│   ├── e-Form Laka                   [admin, operator]
│   └── Antrian Layanan               [admin, operator]
├── Satnarkoba
│   ├── Konseling Online              [admin, operator]
│   └── Permohonan Rehabilitasi       [admin, operator]
├── Satreskrim
│   └── Barang Bukti                  [admin, operator]
├── Sabhara
│   └── Patroli                       [admin, operator]
└── Configuration                     [admin only]
    ├── Polsek
    ├── Kabupaten
    ├── Kecamatan
    └── Desa/Kelurahan
```

---

## Frontend Assets

### Map Widget — Koordinat (OWL Component: DkmMapPicker)

- **File**: [static/src/js/map_widget.js](static/src/js/map_widget.js)
- **Template**: [static/src/xml/map_widget.xml](static/src/xml/map_widget.xml)
- **CSS**: [static/src/css/map_widget.css](static/src/css/map_widget.css)
- **Field widget name**: `dkm_map_picker` (untuk field tipe `float`)
- **Library**: Leaflet.js
- **Center default**: Palembang [-2.9761, 104.7754], zoom 13
- **Fitur**: Click-to-pick koordinat, drag marker, display lat/lng 6 desimal
- **Tile**: OpenStreetMap

### Patroli Route Map Widget (OWL Component: PatroliRouteMap)

- **File**: [static/src/js/patroli_map_widget.js](static/src/js/patroli_map_widget.js)
- **Template**: [static/src/xml/patroli_map_widget.xml](static/src/xml/patroli_map_widget.xml)
- **CSS**: [static/src/css/map_widget.css](static/src/css/map_widget.css) (class `.dkm-rmap-*`)
- **Digunakan di**: Form view `digital_kamtibmas.patroli`
- **Fitur**:
  - Marker bernomor urut (1, 2, 3, ...) untuk setiap titik — **bukan** teks "Mulai"/"Akhir"
  - Garis rute **putus-putus** (`dashArray: '10, 7'`)
  - **Tanpa** tanda panah arah
  - Header menampilkan jumlah titik valid di pojok kanan (badge `.dkm-rmap-count`)
  - Popup per marker: keterangan, waktu rekam, lat/lng
  - `popupAnchor: [0, -11]` — tail popup tepat di tengah dot marker

**Getter `titikCount`**:
```js
get titikCount() {
    return (this.props.record.data.titik_ids?.records ?? [])
        .filter(r => r.data.latitude && r.data.longitude).length;
}
```

### Dashboard (OWL Component: DkmDashboard)

- **File**: [static/src/js/dashboard.js](static/src/js/dashboard.js)
- **Template**: [static/src/xml/dashboard.xml](static/src/xml/dashboard.xml)
- **CSS**: [static/src/css/dashboard.css](static/src/css/dashboard.css)
- **Client action tag**: `digital_kamtibmas.dashboard`
- **Libraries**: Leaflet.js (peta), ECharts (grafik)

---

## Dashboard — Struktur Multi-Seksi

Dashboard memiliki sidebar kiri dengan 4 seksi. Seksi aktif dikontrol oleh `state.activeSection`.

| Seksi | Icon | Konten Utama |
|---|---|---|
| `satlantas` | fa-car | KPI Antrian (standar) + KPI e-Form Laka (gradient) + Chart + Peta laka |
| `satnarkoba` | fa-medkit | KPI Konseling (standar) + KPI Rehab (gradient) + Chart + Jadwal |
| `satreskrim` | fa-search | KPI Barang Bukti (standar) + Chart jenis perkara + Tabel terbaru |
| `sabhara` | fa-binoculars | KPI Patroli (standar) + Live Map Patroli + Chart trend |

---

## Dashboard — State

```javascript
state = {
    activeSection: 'satlantas',
    sidebarCollapsed: false,
    period: 'this_month',     // filter periode untuk Satlantas
    loading: true,

    // ── Satlantas ──────────────────────────────────────────────────────────
    kpi: {
        antrTotal, antrMenunggu, antrAktif, antrSelesai,
        lakaTotal, lakaBaru, lakaDisproses, lakaSelesai,
    },
    trendData: [],       // 6 bulan terakhir line chart laka
    layanData: [],       // distribusi jenis layanan antrian
    calendarData: [],    // heat-map kalender
    activeAntrian: [],   // antrian aktif hari ini
    lakaPending: [],     // e-form laka BARU+DIPROSES

    // ── Satnarkoba ─────────────────────────────────────────────────────────
    satkoba: {
        loading: false,
        kpi: { konTotal, konMenunggu, konProses, konSelesai,
               rehTotal, rehMenunggu, rehProses, rehSelesai },
        trendData: [], konJenis: [], jadwalKon: [], jadwalReh: [],
    },

    // ── Satreskrim ─────────────────────────────────────────────────────────
    satreskrim: {
        loading: false,
        kpi: { total, diterima, aktif, selesai },
        trendData: [], jenisPerkara: [], terbaru: [],
    },

    // ── Sabhara ────────────────────────────────────────────────────────────
    sabhara: {
        loading: false,
        kpi: { total, menunggu, berjalan, selesai },
        trendData: [], terbaru: [],
        livePatroli: [],      // array patroli aktif dengan posisi terakhir
        liveLastUpdate: null, // ISO string waktu update terakhir
    },
}
```

---

## Dashboard — Live Patrol Map (Sabhara)

Card di bawah KPI row Sabhara. Memantau pergerakan patroli aktif secara realtime.

### Fitur

- **Auto-refresh** setiap 30 detik via `setInterval` tanpa page reload
- **Pulsing marker** orange (`#f59e0b`) dengan animasi ring `dkm-ring` untuk patroli aktif
- **Sidebar list** kanan: daftar patroli berjalan, klik → fokus + buka popup di peta
- **LIVE badge** berkedip (animasi `dkm-blink`) di header card
- **Waktu update** terakhir di header (format HH:MM:SS WIB)

### Refs & Private Vars

```js
this.sbLiveMapRef = useRef("sbLiveMap");
this._sbLiveMap = null;            // instance Leaflet map
this._sbLiveMarkers = {};          // { patroli_id: L.marker }
this._sbLivePollTimer = null;      // setInterval handle
this._sbLiveBoundsFitted = false;  // flag pertama kali fitBounds
```

### Lifecycle

```
setSection('sabhara')
  → loadSabhara()   [fetch KPI, set loading=false]
  → setTimeout 120ms
  → _initSabharaLiveMap()
      → L.map(sbLiveMapRef.el) + OSM tiles
      → _loadLivePatroli()  [fetch + update markers]
      → _startLivePoll()    [setInterval 30s]

setSection(other) OR onWillDestroy
  → _stopLivePoll()         [clearInterval]
  → _sbLiveMap.remove()
  → reset _sbLiveMarkers, _sbLiveBoundsFitted
```

### Centering Logic

- **Pertama kali**: `fitBounds(bounds, {padding:[80,80]})` — instant
- **Update berikutnya, 1 patroli**: `panTo(latlng, {animate:true})` — smooth
- **Update berikutnya, >1 patroli**: `fitBounds(bounds, {padding:[80,80], animate:true})`

### Marker Diff-Update (`_updateLiveMarkers`)

Diff `_sbLiveMarkers` (existing) vs data baru:
- Patroli hilang → `marker.remove()` + hapus dari dict
- Patroli ada → `setLatLng` + update icon + rebind popup
- Patroli baru → buat `L.divIcon` dengan HTML pulse + `L.marker`

### CSS Classes Live Map

| Class | Keterangan |
|---|---|
| `.dkm-sb-live-header` | Header card (dark navy `#1e1b4b`, `z-index:10`, `flex-shrink:0`) |
| `.dkm-sb-live-body` | Flex container peta+sidebar (`height:430px`, `overflow:hidden`, `z-index:1`) |
| `.dkm-sb-live-map` | Div Leaflet (`flex:1`, `min-width:0`) |
| `.dkm-sb-live-list` | Sidebar kanan (`width:230px`, `overflow-y:auto`, `height:100%`, `min-height:0`) |
| `.dkm-sb-live-legend` | Legend bar bawah (`flex-shrink:0`, `z-index:10`) |
| `.dkm-live-marker` | Wrapper marker (**`position:relative`**, `display:inline-flex`) |
| `.dkm-live-marker-dot` | Lingkaran oranye (`22×22`, `border:3px solid #fff`) |
| `.dkm-live-marker-pulse` | Ring animasi (`position:absolute`, `animation:dkm-ring 2s infinite`) |

**Penting**: `.dkm-live-marker` harus `position:relative` — tanpa ini pulse ring keluar dari map container dan menutupi header/elemen lain.

---

## Dashboard — KPI Card Styles

### Style Standar (`dkm-kpi-card`)

Digunakan di: KPI Antrian (Satlantas), KPI Patroli (Sabhara), KPI Barang Bukti (Satreskrim), KPI Konseling (Satnarkoba).

```html
<div class="dkm-kpi-row">
  <div class="dkm-kpi-card" t-on-click="...">
    <div class="dkm-kpi-icon"><i class="fa fa-..."/></div>
    <div class="dkm-kpi-value">123</div>
    <div class="dkm-kpi-label">Label</div>
  </div>
</div>
```

### Style Gradient (`dkm-laka-card`)

Digunakan di: KPI e-Form Laka (Satlantas), KPI Permohonan Rehabilitasi (Satnarkoba).

Setiap card: background gradient, ikon dekoratif besar (opacity 0.10) di pojok kanan bawah, chip label, angka besar, progress bar mini (kecuali card Total).

**Warna tersedia**:

| Modifier | Gradient |
|---|---|
| `dkm-laka-card--purple` | `#7c3aed → #4c1d95` |
| `dkm-laka-card--blue` | `#3b82f6 → #1e40af` |
| `dkm-laka-card--orange` | `#f59e0b → #b45309` |
| `dkm-laka-card--green` | `#10b981 → #065f46` |
| `dkm-laka-card--slate` | `#64748b → #334155` |
| `dkm-laka-card--amber` | `#f59e0b → #92400e` |

**Penugasan warna**:

| Seksi | KPI | Warna |
|---|---|---|
| Satlantas | Laka Total | `--purple` |
| Satlantas | Laka Baru | `--blue` |
| Satlantas | Laka Diproses | `--orange` |
| Satlantas | Laka Selesai | `--green` |
| Satnarkoba | Rehab Total | `--blue` |
| Satnarkoba | Rehab Menunggu | `--slate` |
| Satnarkoba | Rehab Diproses | `--amber` |
| Satnarkoba | Rehab Selesai | `--green` |

---

## Frontend — Pola Umum

### Timezone Conversion (WIB = UTC+7)

```js
_wib(iso) {
    if (!iso) return null;
    return new Date(new Date(iso).getTime() + 7 * 3600 * 1000);
}
_fmtWib(iso) {
    const d = this._wib(iso);
    if (!d) return '-';
    return d.toISOString().slice(0, 16).replace('T', ' ') + ' WIB';
}
```

### Sidebar Scroll Pattern (Flexbox)

Untuk list di dalam flex container agar `overflow-y: auto` bekerja:
```css
.sidebar-list {
    height: 100%;
    min-height: 0;       /* wajib: flex item tidak bisa shrink tanpa ini */
    overflow-y: auto;
    overflow-x: hidden;
    box-sizing: border-box;
}
```

### Inisialisasi Leaflet setelah OWL Render

Gunakan `setTimeout` setelah set `loading = false` agar OWL sempat render DOM:
```js
this.state.sabhara.loading = false;
setTimeout(() => this._initSabharaLiveMap(), 120);
```

---

## Color Scheme (Dashboard CSS)

Mengadopsi gaya **omni_referral_base** — clean, minimal, elegan.

| Elemen | Warna | Keterangan |
|---|---|---|
| Background | `#f8f9fa` | Netral |
| Brand/Primary | `#71639e` | Purple elegan |
| KPI icon purple bg | `#f0eff5` | Light purple |
| Card shadow | `0 1px 4px rgba(0,0,0,0.07)` | Subtle |
| Card radius | `0.25rem` (4px) | Minimal |
| Text heading | `#1f2937` | Charcoal |
| Text secondary | `#6b7280` | Gray |
| Live map header | `#1e1b4b` | Dark navy |
| Pulse marker | `#f59e0b` | Amber/oranye |
| Active indicator | `#22c55e` | Hijau |
| BARU/Menunggu | `#dbeafe` / `#1d4ed8` | Biru |
| DIPROSES | `#fef3c7` / `#92400e` | Orange |
| SELESAI | `#d1fae5` / `#065f46` | Hijau |

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

---

## File Kunci

| File | Peran |
|---|---|
| [models/eform_laka.py](models/eform_laka.py) | Model e-Form Laka Satlantas |
| [models/antrian.py](models/antrian.py) | Antrian layanan Satlantas |
| [models/konseling.py](models/konseling.py) | Konseling online Satnarkoba |
| [models/rehab.py](models/rehab.py) | Permohonan rehabilitasi Satnarkoba |
| [models/barang_bukti.py](models/barang_bukti.py) | Barang bukti Satreskrim |
| [models/patroli.py](models/patroli.py) | Patroli Sabhara + titik GPS |
| [static/src/js/dashboard.js](static/src/js/dashboard.js) | Dashboard OWL (4 seksi) + live map |
| [static/src/css/dashboard.css](static/src/css/dashboard.css) | Styling dashboard + gradient card + live map |
| [static/src/js/patroli_map_widget.js](static/src/js/patroli_map_widget.js) | Widget peta rute patroli |
| [static/src/js/map_widget.js](static/src/js/map_widget.js) | Widget koordinat (field picker) |
| [views/dashboard_views.xml](views/dashboard_views.xml) | Client action dashboard |
| [views/menu.xml](views/menu.xml) | Struktur menu aplikasi |
| [security/security.xml](security/security.xml) | Privilege + kategori modul |
| [security/ir.model.access.csv](security/ir.model.access.csv) | Hak akses per model per grup |
| [hooks.py](hooks.py) | Migrasi data dari petadigi |

---

## Changelog Perbaikan

| # | File | Perubahan |
|---|---|---|
| 1 | `security/security.xml` | Model privilege `res.privilege` → `res.groups.privilege`; tambah `ir.module.category` |
| 2 | `views/*_views.xml` | `<group expand="0" string="...">` → `<group>` di 4 file views |
| 3 | `models/kabupaten.py` | Field `kode` → `code`, `tipe` → `type` |
| 4 | `models/kecamatan.py` | Field `kode` → `code` |
| 5 | `models/desa.py` | Field `kode` → `code`, `tipe` → `type` |
| 6 | `models/polsek.py` | Hapus field `code` |
| 7 | `hooks.py` | Gunakan `src.code`/`src.type`; hapus `code` dari create polsek |
| 8 | `static/src/css/dashboard.css` | Redesign: gaya omni_referral_base |
| 9 | `static/src/js/patroli_map_widget.js` | Garis putus-putus; marker bernomor; tanpa panah; header badge titikCount; `popupAnchor:[0,-11]` |
| 10 | `static/src/xml/patroli_map_widget.xml` | Tambah `<span class="dkm-rmap-count">` di header |
| 11 | `static/src/css/map_widget.css` | Tambah `.dkm-rmap-count` badge style |
| 12 | `static/src/js/dashboard.js` | Live patrol map Sabhara: `_initSabharaLiveMap`, `_loadLivePatroli`, `_updateLiveMarkers`, `_startLivePoll`, `_stopLivePoll` |
| 13 | `static/src/xml/dashboard.xml` | Live map card Sabhara; gradient KPI e-Form Laka (`dkm-laka-card`); gradient KPI Rehab |
| 14 | `static/src/css/dashboard.css` | `.dkm-laka-card` gradient styles; `.dkm-sb-live-*` live map CSS; animasi `dkm-ring`, `dkm-blink` |
| 15 | `static/src/css/dashboard.css` | Fix header live map hilang: `z-index:10` header/legend; `overflow:hidden` body; `position:relative` `.dkm-live-marker` |
| 16 | `static/src/css/dashboard.css` | Fix sidebar scroll live map: `height:100%; min-height:0` pada `.dkm-sb-live-list` |
| 17 | `static/src/js/dashboard.js` | Fix map tidak mengikuti marker: hapus `isFirst` guard, selalu pan/fitBounds setelah update |
