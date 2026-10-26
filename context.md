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
├── Warga (sequence 5)                  [admin only]
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
    ├── Konfigurasi Wablas              [admin only]
    └── Permintaan Hapus Akun (sequence 90) [admin only]
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

## Mobile Home Content — Slider & Welcome Screen

Konten dinamis yang dikelola dari backend Odoo untuk ditampilkan di dashboard mobile (Flutter).

### digital.kamtibmas.slider

Banner carousel di dashboard mobile. Ditampilkan berurutan sesuai `sequence`.

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Judul (required) |
| `image` | Binary | Gambar banner (required, attachment) |
| `sequence` | Integer | Urutan tampil (default 10) |
| `active` | Boolean | Aktif/nonaktif |

**Endpoint**: `GET /api/mobile/slider` (`controllers/mobile_slider.py`, auth public) — return list `{id, name, image_url}`, hanya record `active=True`, urut `sequence`.

### digital.kamtibmas.welcome.screen

Dialog sambutan yang muncul sekali per sesi saat dashboard mobile dibuka. **Hanya boleh 1 record aktif** (`@api.constrains`).

| Field | Tipe | Keterangan |
|---|---|---|
| `name` | Char | Judul (required) |
| `image` | Binary | Gambar welcome (required, attachment) |
| `active` | Boolean | Aktif/nonaktif — validasi single-active |
| `tanggal_mulai` / `tanggal_selesai` | Date | Rentang tampil (opsional, kosong = tanpa batas) |
| `keterangan` | Text | Catatan tambahan (opsional) |
| `button_label` | Char | Label tombol aksi (default "Lihat detail") |
| `button_url` | Char | URL tujuan tombol — dibuka via `url_launcher` di browser eksternal mobile |

**Endpoint**: `GET /api/mobile/welcome-screen` (`controllers/mobile_welcome.py`, auth public) — domain filter `active=True` + rentang tanggal terhadap `date.today()`, return `null` jika tidak ada yang cocok.

**Flutter**: `lib/features/dashboard/presentation/providers/welcome_screen_provider.dart` (`WelcomeScreenData`) + `_WelcomeDialog` di `dashboard_screen.dart`. Tombol aksi hanya muncul jika `button_url` tidak kosong.

---

## Warga & Registrasi Mobile

### Registrasi mobile — dua versi (jangan hapus v1)

| Endpoint | Dipakai app | Login |
|---|---|---|
| `POST /mobile/dkm/register` (v1) | ≤ 1.3.0+6 (sudah rilis) | Nomor WhatsApp (`628xxx`); password acak dikirim lewat WA |
| `POST /mobile/dkm/v2/check-username` | ≥ 1.4.0+7 | Cek username tersedia / belum |
| `POST /mobile/dkm/v2/register` | ≥ 1.4.0+7 | Username + nama + password (+ foto opsional); tanpa WA dan tanpa nomor telepon |

Semuanya di `controllers/mobile_register.py`, `type='jsonrpc'`, `auth='public'`. **Endpoint v1 dibiarkan apa adanya** supaya app lama yang sudah rilis tetap bisa daftar. Perubahan perilaku pendaftaran selalu lewat endpoint berversi baru, bukan mengubah yang lama.

**Aturan v2** (divalidasi di server, dan sama persis di Flutter `registration_screen.dart` — ubah keduanya bersamaan):
- Username dinormalisasi ke huruf kecil, regex `^[a-z][a-z0-9._]{3,29}$` (4–30 karakter). Wajib diawali huruf, jadi tidak bisa berupa angka murni — mencegah bentrok dengan login nomor WA milik akun v1.
- Nama dicadangkan (`admin`, `polri`, `polrestabes`, `ampera247`, dst.) ditolak dengan pesan "Username tidak tersedia".
- Cek ketersediaan case-insensitive dan ikut menghitung akun terarsip (`=ilike` dengan escape `_` dan `%`, `active_test=False`).
- Password 8–64 karakter, wajib kombinasi huruf dan angka.
- Flutter: cek username otomatis (debounce 500 ms, counter `_checkSeq` untuk membuang respons usang), form tidak bisa dikirim bila username terpakai / masih diperiksa. Foto opsional dan disembunyikan di web.

**Belum ada**: rate limit pada endpoint register / check-username, dan "lupa password". Akun v2 tidak punya nomor telepon, jadi pemulihan lewat admin (menu Warga → Reset Password).

### digital_kamtibmas.warga (menu Warga)

Daftar akun grup **Masyarakat** untuk admin. Model view SQL read-only (`_auto = False`) di atas `res.users` + `res.partner` (`models/warga.py`, `views/warga_views.xml`), menu **Warga** di root (sequence 5, hanya `group_dkm_admin`). Dengan view SQL, admin DKM tidak perlu hak Settings dan tidak bisa mengubah grup / hak akses user lain.

| Field | Keterangan |
|---|---|
| `user_id` | Akun `res.users` (id baris = id user) |
| `name`, `login`, `phone`, `street` | Dari user / partner |
| `active`, `create_date` | Status dan tanggal daftar |
| `image_128` | `Binary` related ke `user_id.image_128` |
| `antrian_count`, `eform_count`, `konseling_count`, `rehab_count` | Compute (sudo + `_read_group`) → smart button ke riwayat layanan |
| `deletion_pending` | Compute: ada `account_deletion_request` berstatus pending |

**Aksi** (hanya `group_dkm_admin`, hanya target bergrup Masyarakat, tidak boleh akun sendiri):
- `action_toggle_active` — nonaktifkan / aktifkan.
- `action_reset_password` — password acak (`secrets`), ditampilkan sekali lewat notifikasi sticky. Satu akun per panggilan.
- `action_hapus_akun` — **anonimisasi**, bukan `unlink`: nama partner jadi "Akun Dihapus", alamat / telepon / email / foto dikosongkan, login jadi `dihapus.<id>` (username lama bisa dipakai lagi), password diacak, akun dinonaktifkan, dan `account_deletion_request` pending milik user itu ditandai `processed` dengan catatan. Baris layanan (antrian, laka, konseling, rehab) tetap utuh agar relasi tidak rusak.
- `account_deletion_request.action_hapus_akun` (tombol "Hapus Akun Pengguna" di form Permintaan Hapus Akun) memanggil aksi di atas, jadi hanya ada satu jalur hapus akun. Baris permintaan sendiri masih menyimpan `nama` dan `login` asli sebagai jejak audit.

**Catatan teknis view SQL**:
- `_log_access = True` dan view wajib menyediakan kolom `create_uid`, `create_date`, `write_uid`, `write_date`. Web client selalu meminta `write_date` saat membuka form; tanpa kolom itu muncul `ValueError: Invalid field 'write_date'`.
- Gunakan `fields.Binary` (bukan `fields.Image`) untuk related foto — `Image` mensyaratkan `_log_access` dan memunculkan warning.
- `<group string>` tidak valid di `<search>` Odoo 19; taruh `<filter>` group-by langsung.
- Filter grup di SQL lewat `ir_model_data` (`module='digital_kamtibmas'`, `name='group_masyarakat'`) di `EXISTS`, jadi view bisa dibuat sebelum data grup dimuat.
- Menuitem yang parent-nya didefinisikan di `menu.xml` **harus** ditaruh di `menu.xml` (dimuat paling akhir di manifest). Menu Warga dan Permintaan Hapus Akun sudah dipindah ke sana.

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
| 1.5.2 | Fix akses e-Form Laka dari mobile: tambah read-only `base.group_user` di `ir.model.access.csv` untuk model `yang_terlibat`, `kabupaten`, `kecamatan`, `desa`, `polsek`. Tambah halaman web publik `/dukungan` (Support URL) dan `/ampera247` (Marketing URL) di `controllers/privacy_policy.py` untuk keperluan App Store listing. |
| 1.5.3 | Fix CORS error web app `ampera247.polisibaik.id`: root cause adalah `env.prod.json` menggunakan BASE_URL `kamtibmas.polrestabes-palembang.id` (salah) dan DB_NAME `odoo_prod` (tidak ada) — difix ke `palembang.polisibaik.id` dan `palembang`. CORS di nginx `palembang.conf` sudah dikonfigurasi via `map $cors_origin` untuk `ampera247.polisibaik.id`, tidak perlu `cors='*'` di controller (menyebabkan duplicate header). Flutter web rebuild dan deploy ke `/home/rofi/ampera247/` di server. Foto picker registrasi dikondisikan `if (!kIsWeb)` — web pakai avatar Odoo otomatis, mobile tetap bisa upload foto. iOS App Store: build 1.1.0 (4) disubmit ulang, reply dikirim ke Apple untuk Guideline 2.1 (hubungan CV Sel Studio / CV Mitra Hoki dengan Polrestabes Palembang) dan 5.1.1v (Alamat opsional, WhatsApp wajib untuk kirim password). |
| 1.5.4 | iOS App Store lanjutan: Apple menolak 2x lagi dengan Guideline 5.1.1(ix) — seller name harus mencerminkan nama instansi pemerintah. Reply klarifikasi dikirim 2x (posisi sebagai community app, bukan app pemerintah). Reply pertama yang menyebut "Polrestabes Palembang" justru memicu 5.1.1(ix). Ditemukan bahwa `dharukun@yahoo.com` punya akses ke akun Apple Developer **Divisi Teknologi Informasi dan Komunikasi Kepolisian Negara Republik Indonesia** (Divtik Polri) — opsional untuk transfer/resubmit. Sementara menunggu respons Apple, setup **TestFlight External Testing**: grup "Ampera External" dibuat, build 1.1.0 (4) status "Waiting for Review" untuk Beta App Review, public link `https://testflight.apple.com/join/QPGb7CsZ`. Domain baru `ampera2407.id` dibeli sebagai URL netral (tanpa kata "polisi") untuk App Store listing. Nginx dikonfigurasi di server: `/etc/nginx/sites-available/ampera2407.id/ampera2407.conf` — reverse proxy ke Odoo dengan `Host: palembang.polisibaik.id` (database palembang). SSL via Let's Encrypt untuk `ampera2407.id`. Ditambahkan `proxy_mode = True` ke `/etc/odoo/odoo.conf`. Server mengalami OOM kill nginx 2x karena tidak ada swap (Swap = 0) — pending penambahan swap 4GB oleh server admin. URL App Store perlu diupdate ke: Support `https://ampera2407.id/dukungan`, Privacy Policy `https://ampera2407.id/kebijakan-privasi`, Marketing `https://ampera2407.id/ampera247` — semua halaman sudah diverifikasi bersih dari kata polisi/police. |
| 1.5.5 | **Flutter mobile 1.2.0+5**: (1) Ripple effect audit menyeluruh — semua `GestureDetector`/`Container` bertappable diganti `Material + InkWell` di: profile_screen, dashboard_screen, antrian_screen, konseling_screen, barang_bukti_screen, patroli_home_screen. Pattern: `DecoratedBox` (shadow) + `Material` (ink surface, clipBehavior) + `InkWell`. (2) Bugfix crash `barang_bukti_screen.dart` dan `konseling_screen.dart`: `Material` tidak boleh menerima `borderRadius` DAN `shape` secara bersamaan — hapus `borderRadius`, gunakan hanya `shape: RoundedRectangleBorder(...)`. (3) AndroidManifest.xml: tambah `<queries>` intent untuk `mailto:` dan `https:` agar `canLaunchUrl()` tidak selalu return false di Android 11+. (4) **Play Store**: update ditolak karena "Kebijakan Klaim Menyesatkan — Tidak Ada Link Sumber Informasi Pemerintah". Fix: deskripsi diupdate dengan disclaimer di bagian paling atas, link sumber resmi (`palembang.go.id`, `polrestapalembang.polri.go.id`), repositioning sebagai "community app", developer diubah dari CV Sel Studio → CV. "Mitra Hoki Maju Mapan". AAB 1.2.0+5 disubmit. (5) **App Store**: banding Guideline 5.1.1(ix) disiapkan ulang — strategi: SIUP CV. "Mitra Hoki Maju Mapan" (No. 517/0160/35.73.407/2015) + Surat Pernyataan bilingual (Indonesia + English) yang menyatakan AMPERA247 adalah produk CV. "Mitra Hoki Maju Mapan", tanpa menyebut instansi pemerintah. |
| 1.5.6 | **App Store lanjutan**: reject 3x dengan Guideline 5.1.1(ix) — Apple eksplisit minta seller name mencerminkan "Pemerintah Kota Palembang". Strategi baru: **Bank Sumsel Babel** (PT Bank Pembangunan Daerah Sumatera Selatan dan Bangka Belitung) sebagai institusi pendukung netral (bukan penegak hukum, relevan geografis Palembang). Dibuat Surat Permohonan Dukungan dari CV Mitra Hoki ke Bank Sumsel Babel (`.docx`, alamat Jl. Gubernur H. Ahmad Bastari No. 7, Jakabaring Palembang) untuk memperoleh surat dukungan resmi balasan sebagai evidence of relationship ke Apple. **Model baru Odoo**: `digital.kamtibmas.welcome.screen` (`models/welcome_screen.py`, `controllers/mobile_welcome.py`, `views/welcome_screen_views.xml`) dan `digital.kamtibmas.slider` untuk banner dashboard mobile — endpoint `/api/mobile/welcome-screen` dan `/api/mobile/slider`, auth public. Welcome screen ditambah field `button_label` (default "Lihat detail") dan `button_url` agar bisa menampilkan tombol aksi yang buka browser eksternal (dipakai untuk link Bank Sumsel Babel sebagai sponsor). Dibuat gambar welcome screen 1080×1350 kombinasi logo AMPERA247 + Bank Sumsel Babel dengan tagline "Membangun Daerah, Melayani Sepenuh Hati". |
| 1.5.7 | **Flutter mobile 1.3.0+6 — bugfix session & migrasi domain**: (1) **Root cause auto-logout tidak jalan**: `AuthInterceptor` mencocokkan nama exception `odoo.exceptions.SessionExpiredException`, tapi Odoo 19 mengirim `odoo.http.SessionExpiredException` (kelas pindah modul) — dibuktikan via curl dengan session_id palsu ke `/web/dataset/call_kw`. Fix: cocokkan akhiran `endsWith('SessionExpiredException')` agar tahan beda versi. (2) **Bug kedua setelah fix #1**: begitu deteksi jalan, terjadi loop 231× panggilan `/web/session/destroy` (self-feeding logout) — root cause: `sessionExpiredProvider` di-`reset()` terlalu dini (seusai satu logout) sementara banyak request lain yang sedang terbang juga balas expired dan masing-masing memicu logout baru. Fix: flag `hasExpired` dikunci sampai ada login berikutnya yang **berhasil** (`reset()` dipindah ke `AuthNotifier.login()`, hanya jika `state.valueOrNull != null`). Juga `apiClientProvider`: `sessionExpired: ref.watch(...)` → `ref.read(...)` — dengan `watch`, tiap `notifyListeners()` membangun ulang `Dio` + seluruh provider turunannya sehingga badai request makin besar. (3) **Crash banner slider**: `_BannerSliderState._startTimer` memanggil `_ctrl.animateToPage()` walau `PageController` belum/tidak lagi attached ke `PageView` (`'positions.isNotEmpty'` assertion) — terjadi saat provider slider balik ke state loading sehingga `PageView` sempat lepas dari tree walau `State` masih `mounted`. Fix: tambah guard `_ctrl.hasClients`. (4) **Migrasi domain**: base URL production `https://palembang.polisibaik.id` → `https://ampera2407.id` (domain netral untuk App Store, lihat 1.5.4) di `app_config.dart`, `login_screen.dart`, `profile_screen.dart` (URL kebijakan privasi), `.vscode/launch.json`. Diverifikasi via curl bahwa `ampera2407.id` melayani DB `palembang` yang sama (reverse proxy nginx dengan `Host: palembang.polisibaik.id`) sebelum migrasi — endpoint API, auth, dan halaman statis (`/kebijakan-privasi`, `/dukungan`) identik. Bundle ID (`id.polisibaik.ampera247`) **tidak diubah** — itu identitas app di store, beda dari base URL. Semua fix diverifikasi live di device `058990610406` via `flutter run` + hot reload/restart lewat Dart Tooling Daemon (`mcp__dart__dtd` connect ke DTD URI dari `flutter devices`/log run), cross-check jumlah baris log dan endpoint yang di-hit sebelum/sesudah fix. AAB 1.3.0+6 dibuild dan disubmit ke Play Store. |
| 1.5.8 | **Perubahan strategi App Store / Play Store**: Polrestabes Palembang bersedia memberi surat pernyataan bahwa AMPERA247 berada di bawah tanggung jawab Polri satwil Polrestabes Palembang dan CV. Mitra Hoki Maju Mapan ditunjuk sebagai pengembang / pengelola teknis. Rute Bank Sumsel Babel dan posisi "community app" ditinggalkan. Draft surat bilingual (Indonesia + Inggris, `.docx`, field kosong di-highlight kuning) dibuat di `Documents/Surat_Pernyataan_Polrestabes_AMPERA247.docx` — menunggu scan PDF bertanda tangan + cap; surat yang sama dipakai untuk Play Console dan App Store Connect (nama app, Bundle ID `id.polisibaik.ampera247`, dan nama CV harus persis sama dengan akun developer). `controllers/privacy_policy.py` diubah: disclaimer "tidak berafiliasi dengan instansi pemerintah" diganti pernyataan **Aplikasi Resmi Polrestabes Palembang** (title, badge, hero, bagian about, intro kebijakan privasi, link `polrestapalembang.polri.go.id`). **Jangan deploy halaman ini dan jangan ubah listing sebelum surat ada** — klaim resmi tanpa bukti berisiko dianggap menyesatkan. Listing Play Store (disclaimer "community app" di atas deskripsi) diubah manual di Play Console setelah surat; welcome screen sponsor Bank Sumsel Babel perlu ditinjau ulang. |
| 1.5.9 | **Registrasi v2 + manajemen Warga**: (1) Pendaftaran app diganti username + nama + password + ulangi password + foto opsional (tanpa WhatsApp / telepon) lewat endpoint baru `/mobile/dkm/v2/check-username` dan `/mobile/dkm/v2/register`; endpoint v1 `/mobile/dkm/register` **tidak diubah** agar app lama tetap jalan. Aturan username dan password: lihat bagian "Warga & Registrasi Mobile". Server live sudah diverifikasi merespons endpoint baru dan lama. (2) Menu **Warga** (`digital_kamtibmas.warga`, view SQL read-only) untuk admin: list + pencarian + smart button riwayat layanan + Reset Password / Nonaktifkan / Hapus Akun (anonimisasi); tombol "Hapus Akun Pengguna" ditambahkan di Permintaan Hapus Akun. Bug saat dibuka di live: `Invalid field 'write_date'` — view SQL harus menyediakan kolom log akses (`_log_access = True`). (3) Instalasi bersih modul sebelumnya tidak mungkin dan sudah diperbaiki: ID duplikat di `ir.model.access.csv` (`access_rehab_*` dan `access_rehab_tempat_*`, baris terakhir yang berlaku sehingga izin tidak berubah) dan menu Permintaan Hapus Akun yang memakai parent dari `menu.xml` sebelum dimuat (dipindah ke `menu.xml`, xmlid sama). Diuji lewat instalasi di database sementara (19 skenario fungsional lulus: akses, aksi, reset password, anonimisasi). (4) **Flutter 1.4.0+7**: `registration_screen.dart` dan `registration_provider.dart` memakai endpoint v2. `env.prod.json` masih berisi `palembang.polisibaik.id` (usang) — build rilis memakai `--dart-define=BASE_URL=https://ampera2407.id --dart-define=DB_NAME=palembang --dart-define=IS_PRODUCTION=true` secara eksplisit. Upgrade modul di server live (`-u digital_kamtibmas`) diperlukan untuk model / menu Warga. |
| 1.5.10 | **Rebranding: nama tampilan AMPERA247 diganti AMPERA PBM** (short description / tagline: "Polisi Bersama Masyarakat"). Diganti: label Android, `CFBundleName`/`CFBundleDisplayName` iOS, web manifest & index, judul/teks di login, splash, profil, `pubspec.yaml`; backend: halaman publik (`privacy_policy.py`, `account_deletion.py`), menu root Odoo, kiosk Tahti & sertifikasi, display antrian, template cetak sertifikasi, pesan WhatsApp registrasi v1. **Tidak diubah (pengenal teknis)**: package / bundle id `id.polisibaik.ampera247`, `applicationId`, `userAgentPackageName`, `ampera247.keystore`, path URL `/ampera247` (Marketing URL listing), daftar username terlarang, nama repo. Domain tetap `ampera2407.id`. Versi Flutter dinaikkan ke **1.4.0+8** karena build iOS 1.4.0 (7) sudah terunggah ke App Store Connect dengan nama lama. Desain welcome screen dibuat ulang (1080x1920, judul "AMPERA PBM", logo baru + tulisan Polrestabes Palembang); skrip render ada di sesi kerja, hasil `welcome_amperapbm.png`. Yang harus diubah manual di toko: nama app "AMPERA PBM" (maks 30 karakter), subtitle App Store / short description Play Store "Polisi Bersama Masyarakat", screenshot. |
