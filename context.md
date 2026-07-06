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
│   ├── tahti_kunjungan.py            # Buku tamu / kunjungan
│   ├── intelkam_wa_config.py         # Konfigurasi Wablas API
│   ├── intelkam_wa_group.py          # Master Group WhatsApp
│   ├── intelkam_distribusi.py        # Distribusi Informasi + Log
│   └── intelkam_respon.py            # Respon WA Masuk
├── controllers/
│   ├── __init__.py
│   ├── display_controller.py         # Controller display antrian
│   ├── tahti_public.py               # Kiosk buku tamu (auth=public)
│   └── intelkam_webhook.py           # Webhook Wablas (incoming + tracking)
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
│   ├── tahti_kiosk_template.xml      # HTML template kiosk publik
│   └── intelkam_views.xml            # Semua view Intelkam
├── security/
│   ├── security.xml
│   └── ir.model.access.csv
├── data/
│   └── sequence.xml                  # FL, PAT, KSL, RHB, BBK, KUJ, THN, DIST
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

## Intelkam — Model

### intelkam.wa.config

Konfigurasi koneksi ke Wablas API. Hanya boleh ada 1 record aktif.

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Label konfigurasi |
| `api_url` | Char | Base URL Wablas (misal `https://xxx.wablas.com`) |
| `token` | Char | API Token Wablas |
| `device_id` | Char | Device ID (opsional) |
| `active` | Boolean | Aktif/nonaktif |

**Methods**: `get_config()` (classmethod, return config aktif), `send_message()`, `check_message_status()`, `action_test_connection()`

**Send message** endpoint: `POST {api_url}/api/send-message`, body `{"phone": ..., "message": ...}`.
Untuk group: `phone = group_id` (tanpa `@g.us`).

### intelkam.wa.group

Master grup WhatsApp tujuan distribusi.

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Nama grup (required) |
| `group_id` | Char | ID grup Wablas — **tanpa** suffix `@g.us` |
| `deskripsi` | Text | Keterangan |
| `active` | Boolean | Aktif/nonaktif (default True) |

> **Penting**: `group_id` disimpan **tanpa** `@g.us`. Webhook Wablas kadang kirim ID dengan suffix `@g.us` → harus di-strip sebelum lookup.

### intelkam.distribusi.info

Distribusi informasi ke grup WhatsApp.

Inherits: `mail.thread`, `mail.activity.mixin`

| Field | Tipe | Keterangan |
|---|---|---|
| `code` | Char | Auto (prefix DIST, sequence `intelkam.distribusi.info`) |
| `perihal` | Char | Perihal/judul (required) |
| `isi_instruksi` | Text | Isi pesan/instruksi (required) |
| `group_ids` | Many2many | → intelkam.wa.group (required) |
| `pengirim_id` | Many2one | → res.users (default current user) |
| `tanggal_kirim` | Datetime | Diisi saat `action_kirim()` |
| `state` | Selection | draft / mengirim / terkirim / gagal |
| `log_ids` | One2many | → intelkam.distribusi.log |
| `jumlah_terkirim` | Integer | Computed dari log |
| `jumlah_gagal` | Integer | Computed dari log |
| `jumlah_pending` | Integer | Computed dari log |

**Actions**: `action_kirim()`, `action_refresh_status()`, `action_reset_draft()`

`action_kirim()` return dict harus menyertakan `'views': [[False, 'form']]` di bagian `next` → wajib di Odoo 19 agar `_preprocessAction` tidak error.

**Auto-refresh** status pending saat form dibuka via override `web_read()`.

### intelkam.distribusi.log

Log per-group pengiriman distribusi.

| Field | Tipe | Keterangan |
|---|---|---|
| `distribusi_id` | Many2one | → distribusi.info (ondelete: cascade) |
| `group_id` | Many2one | → wa.group |
| `wablas_message_id` | Char | ID pesan dari Wablas |
| `status` | Selection | pending / delivered / read / failed |
| `error_message` | Text | Pesan error jika gagal |
| `tanggal` | Datetime | Waktu log |

### intelkam.respon.wa

Pesan masuk dari grup WhatsApp (via webhook Wablas).

| Field | Tipe | Keterangan |
|---|---|---|
| `group_id_wa` | Char | Group ID raw dari Wablas (mungkin ada `@g.us`) |
| `wa_group_id` | Many2one | → wa.group, computed dari `group_id_wa` (store=True) |
| `pengirim` | Char | Nomor HP pengirim (dari `group.sender`) |
| `nama_pengirim` | Char | Nama pengirim (`pushName`, sering kosong untuk group) |
| `pesan` | Text | Isi pesan |
| `file_url` | Char | URL file/gambar (jika ada media) |
| `mime_type` | Char | Tipe MIME media |
| `has_media` | Boolean | Computed, True jika ada `file_url` |
| `media_preview` | Html | Computed HTML preview (`sanitize=False`) |
| `tanggal` | Datetime | Waktu pesan masuk |
| `wablas_message_id` | Char | ID pesan Wablas |
| `distribusi_id` | Many2one | → distribusi.info, computed (distribusi terakhir ke group ini) |
| `raw_payload` | Text | JSON payload mentah dari Wablas |

`_rec_name = 'pengirim'`

**Computed `_compute_wa_group`**: Strip `@g.us` dari `group_id_wa` sebelum lookup ke `intelkam.wa.group`.

**Computed `_compute_distribusi`**: Cari distribusi terakhir ke group yang sama (exclude draft), domain `('group_ids', 'in', [rec.wa_group_id.id])`.

**`media_preview`** menggunakan `fields.Html(sanitize=False)` karena Odoo 19 melarang OWL directive (`t-if`, `t-att-*`) langsung di form view arch. Render via `widget="html"`.

---

## Intelkam — Webhook Wablas

### Controller (`controllers/intelkam_webhook.py`)

| Route | Method | Auth | Fungsi |
|---|---|---|---|
| `/intelkam/webhook/wablas` | POST | public | Pesan masuk dari grup WA |
| `/intelkam/webhook/wablas/tracking` | POST | public | Status update pengiriman |

### Logika Filtering Pesan Masuk

```python
# Skip jika tidak ada konten (read receipt, notifikasi grup)
has_text = bool((msg.get('message') or '').strip())
has_file = bool((msg.get('file') or msg.get('url') or '').strip())
if not has_text and not has_file:
    continue
```

### Struktur Payload Wablas (Group Message)

```python
# Pengirim asli ada di group.sender, bukan sender (sender = nomor bot)
group_info = msg.get('group') or {}
pengirim_no = group_info.get('sender') or msg.get('sender') or msg.get('phone', '')

# pushName sering kosong untuk pesan grup
nama = (msg.get('pushName') or msg.get('pushname') or
        msg.get('senderName') or group_info.get('pushName') or '')

# Timestamp bisa ISO string "2026-07-04T23:57:12Z" atau Unix int
ts = msg.get('timestamp')
try:
    tanggal = datetime.utcfromtimestamp(int(ts))
except (ValueError, TypeError):
    ts_str = str(ts).rstrip('Z').replace('T', ' ')
    tanggal = datetime.strptime(ts_str[:19], '%Y-%m-%d %H:%M:%S')
```

---

## Intelkam — Views (`views/intelkam_views.xml`)

Semua view Intelkam dalam satu file. Views yang ada:

| View | Model | Tipe |
|---|---|---|
| `view_intelkam_wa_config_form` | wa.config | form |
| `view_intelkam_wa_config_list` | wa.config | list |
| `view_intelkam_wa_group_form` | wa.group | form |
| `view_intelkam_wa_group_list` | wa.group | list |
| `view_intelkam_wa_group_search` | wa.group | search (default filter: aktif) |
| `view_intelkam_distribusi_form` | distribusi.info | form |
| `view_intelkam_distribusi_list` | distribusi.info | list |
| `view_intelkam_distribusi_search` | distribusi.info | search |
| `view_intelkam_distribusi_calendar` | distribusi.info | calendar (color=state, quick_create="False") |
| `view_intelkam_respon_form` | respon.wa | form |
| `view_intelkam_respon_list` | respon.wa | list (default groupby: wa_group_id) |
| `view_intelkam_respon_search` | respon.wa | search (default filter: has_group) |
| `view_intelkam_respon_calendar` | respon.wa | calendar (color=wa_group_id, filters="1") |

**Actions**:
- `action_intelkam_distribusi`: view_mode `list,calendar,form`
- `action_intelkam_respon_wa`: view_mode `list,calendar,form`
- `action_intelkam_wa_group`: view_mode `list,form`
- `action_intelkam_wa_config`: view_mode `list,form`

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
├── Intelkam (sequence 60)
│   ├── Distribusi Informasi            [admin, operator]
│   ├── Respon WhatsApp Masuk           [admin, operator]
│   └── Master Group WhatsApp           [admin, operator]
└── Configuration                       [admin only]
    ├── Polsek
    ├── Kabupaten
    ├── Kecamatan
    ├── Desa/Kelurahan
    ├── Sel/Kamar Tahanan (sequence 20)
    └── Konfigurasi Wablas              [admin only]
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

### Akses Model Intelkam

| Model | Admin | Operator |
|---|---|---|
| `intelkam.wa.config` | CRUD | R |
| `intelkam.wa.group` | CRUD | CRU |
| `intelkam.distribusi.info` | CRUD | CRU |
| `intelkam.distribusi.log` | CRUD | CRU |
| `intelkam.respon.wa` | CRUD | R |

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
| `seq_intelkam_distribusi` | `intelkam.distribusi.info` | DIST | 5 |

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
| `intelkam` | fa-eye | `loadIntelkam()` |

### Tahti Dashboard

**KPI Cards** (4 cards):

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
| `thHubChart` | Donut (pie 42%-68%) | Distribusi hubungan tamu |
| `thPerkaraChart` | Pie (filled) | Jenis perkara tahanan aktif |
| `thSelChart` | Stacked bar horizontal | Terisi vs sisa kapasitas per sel |

**Tabel**: 5 kunjungan terakhir

### Intelkam Dashboard

**KPI Cards** (4 cards):

| KPI | Icon | Color | Action |
|---|---|---|---|
| Distribusi Bulan Ini | fa-paper-plane | blue | openIntelkamDistribusiList |
| Terkirim Bulan Ini | fa-check-circle | green | openIntelkamDistribusiList(terkirim) |
| Respon Hari Ini | fa-comment | teal | openIntelkamResponList |
| Total Respon WA | fa-comments | purple | openIntelkamResponList |

**Charts** (ECharts):

| Ref | Chart | Warna | Data |
|---|---|---|---|
| `ikTrendChart` | Bar | Indigo `#4f46e5` | Trend distribusi 6 bulan terakhir |
| `ikResponChart` | Donut (pie 42%-68%) | Multi | Respon per group WA |
| `ikCalWaChart` | Calendar heatmap | Teal `#0d9488` | Aktivitas respon WA selama 1 tahun |

**Tabel**: 5 distribusi terbaru + 5 respon WA terbaru

**State Intelkam**:
```js
intelkam: {
    loading: false,
    kpi: { distribusiTotal, distribusiBulan, terkirimBulan, responTotal, responHariIni },
    trendData: [],         // [{bulan, count}] — 6 bulan
    responPerGroup: [],    // [{label, count}]
    distribusiTerbaru: [], // 5 records
    responTerbaru: [],     // 5 records
    calResponData: [],     // [[date, count]] — 1 tahun berjalan
    calYear: 2026,
}
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

## Dashboard — Badge Classes

```css
/* Generic state badges (tersedia di dashboard.css) */
.dkm-badge--secondary  { background: #f3f4f6; color: #4b5563; }
.dkm-badge--warning    { background: #fef3c7; color: #92400e; }
.dkm-badge--success    { background: #d1fae5; color: #065f46; }
.dkm-badge--danger     { background: #fee2e2; color: #991b1b; }
.dkm-badge--blue       { background: #dbeafe; color: #1d4ed8; }
.dkm-badge--orange     { background: #fef3c7; color: #92400e; }
.dkm-badge--green      { background: #d1fae5; color: #065f46; }
```

---

## Dashboard — Calendar Heatmap Pattern

```xml
<div class="dkm-calendar-card">
    <div class="dkm-chart-header">
        <span class="dkm-chart-title">Judul</span>
        <span class="dkm-chart-sub">
            <t t-esc="state.section.calYear"/> — Keterangan
        </span>
    </div>
    <div t-ref="refName" class="dkm-echarts-calendar"/>
    <div class="dkm-cal-legend">
        <span class="dkm-cal-legend-label">Sedikit</span>
        <span class="dkm-cal-cell" style="background:#ebedf0"/>
        <!-- ... warna lainnya ... -->
        <span class="dkm-cal-legend-label">Banyak</span>
    </div>
</div>
```

ECharts option untuk calendar heatmap:
```js
{
    visualMap: { show: false, min: 0, max: maxVal,
                 inRange: { color: ['#ebedf0', ...palette] } },
    calendar: [{ range: String(year), left: 70, right: 20, top: 30, bottom: 10,
                 cellSize: ['auto', 14], splitLine: { show: false },
                 yearLabel: { show: false },
                 monthLabel: { nameMap: ['Jan',...,'Des'], fontSize: 11, color: '#6b7280' },
                 dayLabel: { firstDay: 1, nameMap: ['Min','Sen',...,'Sab'], fontSize: 11 },
                 itemStyle: { borderColor: '#fff', borderWidth: 3, color: '#ebedf0' } }],
    series: [{ type: 'heatmap', coordinateSystem: 'calendar', calendarIndex: 0, data }],
}
```

---

## Views — Hal Penting Odoo 19

- `<group>` dalam `<search>` **tidak** support atribut `expand` dan `string`
- `widget="badge"` di list view bersifat **read-only** — tidak bisa dipakai di kolom editable
- `invisible` di button/field menggunakan **Python expression string**: `invisible="state != 'berlangsung'"`
- OWL directive (`t-if`, `t-att-*`) **dilarang** di form view arch → gunakan computed `fields.Html(sanitize=False)`
- Action dict inline `ir.actions.act_window` **wajib** menyertakan `'views': [[false,'list'],[false,'form']]` (bukan `view_mode:'list,form'`) agar `_preprocessAction` tidak error. Odoo 19 `_preprocessAction` langsung memanggil `.map()` pada `action.views` — jika `views` undefined maka crash `TypeError: Cannot read properties of undefined (reading 'map')`
- Calendar view: atribut `quick_create="False"` (bukan `quick_add="false"`)
- Groupby filter di search view wajib ada `domain="[]"`: `<filter name="x" domain="[]" context="{'group_by': 'field'}"/>`

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
| Intelkam primary | `#4f46e5` (indigo) |
| Intelkam accent | `#06b6d4` (cyan) |
| Intelkam cal WA | `#0d9488` (teal) |

---

## Changelog

| Versi | Fitur |
|---|---|
| 1.0.0 | Initial: Satlantas (e-Form Laka, Antrian), Satnarkoba, Satreskrim, Sabhara, Dashboard 4 seksi |
| 1.1.0 | Sabhara Live Patrol Map + Route Visualization |
| 1.2.0 | Tahti: Master Sel, Data Tahanan, Buku Tamu (Tamu + Kunjungan), Menu Tahti |
| 1.3.0 | Kiosk Web App (`/tahti/buku-tamu`) — OWL standalone, auth=public |
| 1.4.0 | Dashboard Tahti — KPI, trend 7 hari, pie perkara, stacked bar kapasitas sel, tabel kunjungan |
| 1.5.0 | Intelkam: Distribusi Informasi WA (Wablas), Respon WA Masuk, Master Group, Webhook, Dashboard Intelkam |
| 1.5.1 | Bugfix: semua `openXxxList()` di `dashboard.js` — `view_mode:'list,form'` → `views:[[false,'list'],[false,'form']]` (Odoo 19 `_preprocessAction` requirement) |
