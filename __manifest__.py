{
    'name': 'Digital Kamtibmas',
    'version': '19.0.1.0.0',
    'summary': 'Sistem Informasi Digital Kamtibmas Polrestabes Palembang (AMPERA PBM)',
    'description': """
AMPERA PBM - Polisi Bersama Masyarakat
======================================

Sistem informasi digital untuk Kepolisian Resor Kota Besar (Polrestabes)
Palembang. Modul ini adalah backend dari aplikasi seluler resmi
**AMPERA PBM - Polisi Bersama Masyarakat** (Android dan iOS) yang berada di
bawah tanggung jawab Polrestabes Palembang.

Dikembangkan dan dikelola secara teknis oleh CV. Mitra Hoki Maju Mapan
berdasarkan Surat Pernyataan Kapolrestabes Palembang No. B/1718/X/2026
tanggal 20 Oktober 2026.

Fitur Utama
-----------
* Antrian online: jenis layanan, loket, layar display antrian, dan kiosk.
* e-Form Kecelakaan: laporan kejadian lengkap dengan titik lokasi pada peta.
* Sertifikasi online: bank soal, tes daring, dan sertifikat digital.
* Rehabilitasi: tempat rehabilitasi dan permohonan rehabilitasi.
* Barang Bukti: pencatatan dan informasi barang bukti.
* Konseling: konsultasi melalui chat dan panggilan video (Discuss).
* Tahanan Titipan (Tahti): data tahanan, sel, kunjungan, dan buku tamu kiosk.
* Patroli: grup patroli dan rute patroli.
* Intelkam: distribusi informasi dan pencatatan respons melalui WhatsApp.
* Manajemen Warga: data pengguna aplikasi seluler dan permintaan hapus akun.
* Konten aplikasi: layar sambut dan banner beranda yang dapat dibuka tautannya.
* Dashboard statistik dan peta.

Aplikasi Seluler
----------------
* Pendaftaran dengan username dan kata sandi, ubah nama dan foto profil.
* Menyediakan API untuk aplikasi seluler Android dan iOS.
* Halaman publik: informasi aplikasi, dukungan, kebijakan privasi, dan
  penghapusan akun (https://ampera2407.id/ampera247).

Pengembang
----------
CV. Mitra Hoki Maju Mapan (Tim AMPERA PBM)
""",
    'category': 'Tools',
    'author': 'CV. Mitra Hoki Maju Mapan',
    'website': 'https://ampera2407.id/ampera247',
    'depends': ['base', 'web', 'mail', 'calendar', 'contacts', 'hr', 'spreadsheet_dashboard'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/config_parameter.xml',
        'views/polsek_views.xml',
        'views/kabupaten_views.xml',
        'views/kecamatan_views.xml',
        'views/desa_views.xml',
        'views/eform_laka_views.xml',
        'views/antrian_views.xml',
        'views/loket_views.xml',
        'views/jenis_layanan_views.xml',
        'views/dashboard_views.xml',
        'views/display_config_views.xml',
        'views/antrian_display_template.xml',
        'views/konseling_views.xml',
        'views/mobile_chat_template.xml',
        'views/rehab_tempat_views.xml',
        'views/rehab_report.xml',
        'views/rehab_views.xml',
        'views/barang_bukti_views.xml',
        'views/patroli_grup_views.xml',
        'views/patroli_views.xml',
        'views/tahti_sel_views.xml',
        'views/tahanan_kategori_views.xml',
        'views/tahanan_views.xml',
        'views/tahti_tamu_views.xml',
        'views/tahti_kunjungan_views.xml',
        'views/tahti_kiosk_template.xml',
        'views/tahti_kiosk_config_views.xml',
        'views/intelkam_views.xml',
        'views/sertifikasi_soal_views.xml',
        'views/sertifikasi_profil_views.xml',
        'views/sertifikasi_views.xml',
        'views/sertifikasi_kiosk_template.xml',
        'views/sertifikasi_cetak_template.xml',
        'views/account_deletion_views.xml',
        'views/warga_views.xml',
        'views/welcome_screen_views.xml',
        'views/slider_views.xml',
        'views/menu.xml',
        'views/login_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'digital_kamtibmas/static/src/css/login_brand.css',
        ],
        'web.assets_backend': [
            # Libs
            'digital_kamtibmas/static/lib/leaflet/leaflet.css',
            'digital_kamtibmas/static/lib/leaflet/leaflet.js',
            # Markercluster: re-attach setelah leaflet agar tidak konflik dengan petadigi
            'digital_kamtibmas/static/lib/leaflet-markercluster/MarkerCluster.css',
            'digital_kamtibmas/static/lib/leaflet-markercluster/MarkerCluster.Default.css',
            'digital_kamtibmas/static/lib/leaflet-markercluster/leaflet.markercluster.js',
            'digital_kamtibmas/static/lib/echart/echarts.min.js',
            # Map widget
            'digital_kamtibmas/static/src/css/map_widget.css',
            'digital_kamtibmas/static/src/xml/map_widget.xml',
            'digital_kamtibmas/static/src/js/map_widget.js',
            # Patroli route map
            'digital_kamtibmas/static/src/xml/patroli_map_widget.xml',
            'digital_kamtibmas/static/src/js/patroli_map_widget.js',
            # Dashboard
            'digital_kamtibmas/static/src/css/dashboard.css',
            'digital_kamtibmas/static/src/xml/dashboard.xml',
            'digital_kamtibmas/static/src/js/dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'sequence': 2,
    'license': 'LGPL-3',
}
