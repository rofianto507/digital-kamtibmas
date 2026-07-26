from odoo import http
from odoo.http import request, Response


_PRIVACY_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kebijakan Privasi – AMPERA247</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#F4F9FF;color:#0D1526;line-height:1.7;font-size:15px}
.header{background:#1D2A44;padding:36px 24px 32px;text-align:center}
.header-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(162,207,254,.15);border:1px solid rgba(162,207,254,.3);border-radius:20px;padding:4px 14px;margin-bottom:16px}
.header-badge span{color:#A2CFFE;font-size:12px;font-weight:600;letter-spacing:.8px;text-transform:uppercase}
.header h1{color:#fff;font-size:clamp(22px,5vw,28px);font-weight:800;letter-spacing:-.3px;margin-bottom:6px}
.header-sub{color:rgba(255,255,255,.55);font-size:13px}
.header-divider{width:40px;height:3px;background:#A2CFFE;border-radius:2px;margin:18px auto 0;opacity:.6}
.container{max-width:760px;margin:0 auto;padding:32px 20px 60px}
.intro{background:#fff;border-radius:12px;border:1px solid #DDE6F0;padding:20px 24px;margin-bottom:28px;border-left:4px solid #1565C0}
.intro p{color:#64748B;font-size:14px}
.intro strong{color:#0D1526}
.section{background:#fff;border:1px solid #DDE6F0;border-radius:12px;margin-bottom:16px;overflow:hidden}
.section-header{display:flex;align-items:center;gap:12px;padding:18px 20px;border-bottom:1px solid #DDE6F0}
.section-icon{width:36px;height:36px;border-radius:8px;background:rgba(21,101,192,.1);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.section-icon svg{width:18px;height:18px}
.section-title{font-size:15px;font-weight:700;color:#0D1526}
.section-body{padding:18px 20px}
.section-body p{color:#64748B;font-size:14px;margin-bottom:10px}
.section-body p:last-child{margin-bottom:0}
.item-list{list-style:none}
.item-list li{display:flex;gap:10px;color:#64748B;font-size:14px;padding:6px 0;border-bottom:1px solid #DDE6F0}
.item-list li:last-child{border-bottom:none}
.item-list li::before{content:'';width:6px;height:6px;border-radius:50%;background:#1565C0;margin-top:8px;flex-shrink:0}
.contact-box{background:#1D2A44;border-radius:12px;padding:24px;margin-top:28px;text-align:center}
.contact-box h3{color:#fff;font-size:16px;font-weight:700;margin-bottom:10px}
.contact-box p{color:rgba(255,255,255,.6);font-size:13px;margin-bottom:4px}
.contact-box a{color:#A2CFFE;text-decoration:none;font-weight:600}
.social-row{display:flex;justify-content:center;gap:16px;margin-top:16px}
.social-btn{display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);transition:background .2s,transform .2s;text-decoration:none}
.social-btn:hover{background:rgba(255,255,255,.22);transform:scale(1.08)}
.social-btn svg{width:22px;height:22px;fill:#fff}
.footer{text-align:center;padding:12px 24px 24px;color:#64748B;font-size:12px}
</style>
</head>
<body>
<div class="header">
  <div class="header-badge"><span>Dokumen Resmi</span></div>
  <h1>Kebijakan Privasi</h1>
  <p class="header-sub">Aplikasi AMPERA247 &mdash; Layanan Digital Kamtibmas Kota Palembang</p>
  <div class="header-divider"></div>
</div>
<div class="container">
  <div class="intro">
    <p><strong>Terakhir diperbarui: 19 Juli 2026</strong><br>
    Kebijakan Privasi ini menjelaskan bagaimana aplikasi <strong>AMPERA247</strong>
    yang dikembangkan dan dikelola oleh <strong>CV Sel Studio</strong> mengumpulkan,
    menggunakan, dan melindungi data pribadi pengguna. Dengan menggunakan aplikasi
    ini, Anda menyetujui ketentuan dalam kebijakan ini.</p>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
      </div>
      <div class="section-title">Data yang Kami Kumpulkan</div>
    </div>
    <div class="section-body">
      <p>Aplikasi ini mengumpulkan jenis data berikut:</p>
      <ul class="item-list">
        <li><strong>Data Lokasi</strong> &mdash; koordinat GPS perangkat, digunakan hanya pada saat pengguna mengisi e-Form Laka Lantas untuk menentukan lokasi kejadian secara otomatis. Data lokasi <em>tidak</em> dikumpulkan di luar penggunaan fitur tersebut.</li>
        <li><strong>Data Akun</strong> &mdash; nama lengkap dan username yang terdaftar di sistem AMPERA247.</li>
        <li><strong>Data Aktivitas Layanan</strong> &mdash; riwayat penggunaan fitur (antrian online, e-form laka lantas, sertifikasi, rehabilitasi, konseling) beserta waktu dan detail pengajuan.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
      </div>
      <div class="section-title">Tujuan Penggunaan Data</div>
    </div>
    <div class="section-body">
      <ul class="item-list">
        <li>Menyediakan dan mengelola fitur layanan digital kamtibmas (antrian online, e-form laka lantas, sertifikasi anti narkoba, rehabilitasi, dan konseling).</li>
        <li>Memproses pengajuan layanan yang disampaikan pengguna melalui aplikasi.</li>
        <li>Menggunakan data lokasi untuk memudahkan pengguna melaporkan titik kejadian pada e-Form Laka Lantas.</li>
        <li>Meningkatkan kualitas dan keandalan layanan AMPERA247.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </div>
      <div class="section-title">Berbagi Data dengan Pihak Lain</div>
    </div>
    <div class="section-body">
      <p>Data yang dikumpulkan <strong>tidak dijual, disewakan, atau dibagikan</strong> kepada pihak komersial mana pun. Data hanya dapat diakses oleh:</p>
      <ul class="item-list">
        <li>Tim pengelola AMPERA247 dan CV Sel Studio yang memiliki kewenangan dan akses sistem yang sah.</li>
        <li>Mitra instansi terkait yang terlibat dalam penyelenggaraan layanan, sesuai lingkup tugasnya.</li>
      </ul>
      <p style="margin-top:12px">Pengungkapan data kepada pihak eksternal hanya dilakukan apabila diwajibkan oleh peraturan perundang-undangan yang berlaku di Indonesia.</p>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      </div>
      <div class="section-title">Keamanan Data</div>
    </div>
    <div class="section-body">
      <p>Data disimpan di server pengelola AMPERA247 dengan proteksi akses berbasis autentikasi. Transmisi data antara aplikasi dan server menggunakan protokol HTTPS yang terenkripsi.</p>
      <p>Meskipun kami menerapkan langkah-langkah keamanan yang wajar, tidak ada sistem yang sepenuhnya aman. Kami berkomitmen untuk menangani setiap insiden keamanan secara cepat dan bertanggung jawab.</p>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
      </div>
      <div class="section-title">Penyimpanan &amp; Retensi Data</div>
    </div>
    <div class="section-body">
      <p>Data layanan dan lokasi disimpan selama diperlukan untuk kepentingan operasional AMPERA247. Data akun disimpan selama pengguna masih aktif menggunakan layanan. Pengguna dapat mengajukan penghapusan data melalui fitur Hapus Akun di aplikasi.</p>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </div>
      <div class="section-title">Hak Pengguna</div>
    </div>
    <div class="section-body">
      <p>Pengguna berhak untuk:</p>
      <ul class="item-list">
        <li>Mengetahui data pribadi apa saja yang tersimpan dalam sistem.</li>
        <li>Meminta koreksi data yang tidak akurat kepada administrator sistem.</li>
        <li>Mencabut izin akses lokasi kapan saja melalui pengaturan perangkat &mdash; namun hal ini akan menonaktifkan fitur deteksi lokasi otomatis pada e-Form Laka Lantas.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
      </div>
      <div class="section-title">Perubahan Kebijakan Privasi</div>
    </div>
    <div class="section-body">
      <p>Kebijakan ini dapat diperbarui sewaktu-waktu. Perubahan signifikan akan diinformasikan melalui notifikasi aplikasi atau pembaruan halaman ini. Tanggal "Terakhir diperbarui" di bagian atas halaman akan selalu mencerminkan versi terkini.</p>
    </div>
  </div>

  <div class="contact-box">
    <h3>Hubungi Kami</h3>
    <p>Pertanyaan seputar kebijakan privasi dapat disampaikan kepada:</p>
    <p style="margin-top:10px"><strong style="color:#fff">CV Sel Studio</strong></p>
    <p>Pengembang Aplikasi AMPERA247</p>
    <p style="margin-top:8px"><a href="mailto:mail@selstudio.id">mail@selstudio.id</a></p>
  </div>
</div>
<div class="footer">&copy; 2026 AMPERA247 &mdash; CV Sel Studio. Seluruh hak dilindungi.</div>
</body>
</html>"""


_CHILD_SAFETY_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kebijakan Keselamatan Anak – AMPERA247</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#F4F9FF;color:#0D1526;line-height:1.7;font-size:15px}
.header{background:#1D2A44;padding:36px 24px 32px;text-align:center}
.header-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(162,207,254,.15);border:1px solid rgba(162,207,254,.3);border-radius:20px;padding:4px 14px;margin-bottom:16px}
.header-badge span{color:#A2CFFE;font-size:12px;font-weight:600;letter-spacing:.8px;text-transform:uppercase}
.header h1{color:#fff;font-size:clamp(22px,5vw,28px);font-weight:800;letter-spacing:-.3px;margin-bottom:6px}
.header-sub{color:rgba(255,255,255,.55);font-size:13px}
.header-divider{width:40px;height:3px;background:#A2CFFE;border-radius:2px;margin:18px auto 0;opacity:.6}
.container{max-width:760px;margin:0 auto;padding:32px 20px 60px}
.intro{background:#fff;border-radius:12px;border:1px solid #DDE6F0;padding:20px 24px;margin-bottom:28px;border-left:4px solid #1565C0}
.intro p{color:#64748B;font-size:14px}
.intro strong{color:#0D1526}
.section{background:#fff;border:1px solid #DDE6F0;border-radius:12px;margin-bottom:16px;overflow:hidden}
.section-header{display:flex;align-items:center;gap:12px;padding:18px 20px;border-bottom:1px solid #DDE6F0}
.section-icon{width:36px;height:36px;border-radius:8px;background:rgba(21,101,192,.1);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.section-icon svg{width:18px;height:18px}
.section-title{font-size:15px;font-weight:700;color:#0D1526}
.section-body{padding:18px 20px}
.section-body p{color:#64748B;font-size:14px;margin-bottom:10px}
.section-body p:last-child{margin-bottom:0}
.item-list{list-style:none}
.item-list li{display:flex;gap:10px;color:#64748B;font-size:14px;padding:6px 0;border-bottom:1px solid #DDE6F0}
.item-list li:last-child{border-bottom:none}
.item-list li::before{content:'';width:6px;height:6px;border-radius:50%;background:#1565C0;margin-top:8px;flex-shrink:0}
.alert-box{background:#FEF2F2;border:1px solid #FECACA;border-radius:12px;padding:18px 20px;margin-bottom:16px}
.alert-box p{color:#991B1B;font-size:14px}
.contact-box{background:#1D2A44;border-radius:12px;padding:24px;margin-top:28px;text-align:center}
.contact-box h3{color:#fff;font-size:16px;font-weight:700;margin-bottom:10px}
.contact-box p{color:rgba(255,255,255,.6);font-size:13px;margin-bottom:4px}
.contact-box a{color:#A2CFFE;text-decoration:none;font-weight:600}
.footer{text-align:center;padding:12px 24px 24px;color:#64748B;font-size:12px}
</style>
</head>
<body>
<div class="header">
  <div class="header-badge"><span>Dokumen Resmi</span></div>
  <h1>Kebijakan Keselamatan Anak</h1>
  <p class="header-sub">Aplikasi AMPERA247 &mdash; Layanan Digital Kamtibmas Kota Palembang</p>
  <div class="header-divider"></div>
</div>
<div class="container">
  <div class="intro">
    <p><strong>Terakhir diperbarui: 25 Juli 2026</strong><br>
    CV Sel Studio selaku pengembang aplikasi <strong>AMPERA247</strong> berkomitmen penuh
    untuk menciptakan lingkungan digital yang aman, khususnya bagi anak-anak dan
    kelompok rentan. Kebijakan ini menjelaskan standar keselamatan anak yang kami terapkan
    dalam seluruh fitur dan layanan aplikasi AMPERA247.</p>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      </div>
      <div class="section-title">Komitmen Kami</div>
    </div>
    <div class="section-body">
      <p>AMPERA247 berkomitmen untuk:</p>
      <ul class="item-list">
        <li>Melindungi anak-anak dari segala bentuk pelecehan, eksploitasi, dan konten berbahaya di dalam platform kami.</li>
        <li>Mematuhi seluruh peraturan perundang-undangan perlindungan anak yang berlaku di Indonesia, termasuk UU No. 35 Tahun 2014 tentang Perlindungan Anak.</li>
        <li>Menindaklanjuti setiap laporan terkait keselamatan anak secara cepat dan bertanggung jawab.</li>
        <li>Melaporkan setiap temuan materi pelecehan seksual anak (CSAM) kepada otoritas yang berwenang.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
      </div>
      <div class="section-title">Konten dan Perilaku yang Dilarang</div>
    </div>
    <div class="section-body">
      <p>Pengguna AMPERA247 <strong>dilarang keras</strong> untuk:</p>
      <ul class="item-list">
        <li>Membagikan, memproduksi, atau mendistribusikan materi pelecehan seksual anak (CSAM) dalam bentuk apapun.</li>
        <li>Melakukan pendekatan tidak pantas (grooming) terhadap anak-anak melalui fitur konseling atau komunikasi lainnya.</li>
        <li>Menggunakan fitur aplikasi untuk eksploitasi, intimidasi, atau pelecehan terhadap anak.</li>
        <li>Menyebarkan konten kekerasan, pornografi, atau konten berbahaya lainnya yang dapat membahayakan anak.</li>
      </ul>
      <p style="margin-top:12px">Pelanggaran terhadap ketentuan ini akan mengakibatkan pemblokiran akun secara permanen dan pelaporan kepada pihak berwajib.</p>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </div>
      <div class="section-title">Pembatasan Pengguna</div>
    </div>
    <div class="section-body">
      <p>Aplikasi AMPERA247 ditujukan untuk pengguna berusia <strong>17 tahun ke atas</strong>. Fitur konseling online hanya dapat diakses oleh pengguna terdaftar yang telah memverifikasi identitasnya melalui proses pendaftaran akun.</p>
      <p>Pengguna yang diduga berusia di bawah 17 tahun akan dinonaktifkan aksesnya hingga verifikasi usia dapat dilakukan.</p>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.42 2 2 0 0 1 3.6 1.24h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6 6l.96-.96a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.73 16.92z"/></svg>
      </div>
      <div class="section-title">Cara Melaporkan Pelanggaran</div>
    </div>
    <div class="section-body">
      <p>Jika Anda menemukan konten atau perilaku yang melanggar standar keselamatan anak di dalam aplikasi AMPERA247, segera laporkan melalui:</p>
      <ul class="item-list">
        <li><strong>Email:</strong> selstudiojember@gmail.com &mdash; dengan subjek "Laporan Keselamatan Anak"</li>
        <li><strong>Telepon darurat anak:</strong> 129 (KPAI &mdash; Komisi Perlindungan Anak Indonesia)</li>
        <li><strong>Situs KPAI:</strong> www.kpai.go.id</li>
      </ul>
      <p style="margin-top:12px">Setiap laporan akan ditindaklanjuti dalam waktu <strong>maksimal 3 &times; 24 jam</strong> pada hari kerja.</p>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
      </div>
      <div class="section-title">Penanganan Laporan</div>
    </div>
    <div class="section-body">
      <ul class="item-list">
        <li>Tim kami akan meninjau setiap laporan secara confidential dan menyeluruh.</li>
        <li>Konten yang melanggar akan segera dihapus dan akun pelanggar diblokir permanen.</li>
        <li>Temuan CSAM atau pelanggaran serius lainnya akan dilaporkan langsung kepada Bareskrim Polri dan KPAI sesuai kewajiban hukum.</li>
        <li>Pelapor akan mendapat konfirmasi tindak lanjut melalui email dalam 3 hari kerja.</li>
      </ul>
    </div>
  </div>

  <div class="contact-box">
    <h3>Kontak Keselamatan Anak</h3>
    <p>Laporan dan pertanyaan terkait keselamatan anak:</p>
    <p style="margin-top:10px"><strong style="color:#fff">CV Sel Studio — Tim AMPERA247</strong></p>
    <p style="margin-top:6px"><a href="mailto:selstudiojember@gmail.com">selstudiojember@gmail.com</a></p>
    <p style="margin-top:4px">Subjek: <em>Laporan Keselamatan Anak</em></p>
  </div>
</div>
<div class="footer">&copy; 2026 AMPERA247 &mdash; CV Sel Studio. Seluruh hak dilindungi.</div>
</body>
</html>"""


class PrivacyPolicyController(http.Controller):

    @http.route('/kebijakan-privasi', type='http', auth='public', website=False, csrf=False)
    def privacy_policy(self, **kwargs):
        return Response(_PRIVACY_HTML, content_type='text/html; charset=utf-8')

    @http.route('/kebijakan-keselamatan-anak', type='http', auth='public', website=False, csrf=False)
    def child_safety(self, **kwargs):
        return Response(_CHILD_SAFETY_HTML, content_type='text/html; charset=utf-8')
