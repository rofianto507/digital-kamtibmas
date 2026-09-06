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
  <p class="header-sub">Aplikasi AMPERA247 &mdash; Layanan Publik Digital Kota Palembang</p>
  <div class="header-divider"></div>
</div>
<div class="container">
  <div class="intro">
    <p><strong>Terakhir diperbarui: 31 Juli 2026</strong><br>
    Kebijakan Privasi ini menjelaskan bagaimana aplikasi <strong>AMPERA247</strong>
    yang dikembangkan dan dikelola oleh <strong>CV Mitra Hoki Maju Mapan (Tim AMPERA247)</strong> mengumpulkan,
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
        <li><strong>Data Lokasi</strong> &mdash; koordinat GPS perangkat, digunakan hanya pada saat pengguna mengisi e-Form Kecelakaan untuk menentukan lokasi kejadian secara otomatis. Data lokasi <em>tidak</em> dikumpulkan di luar penggunaan fitur tersebut.</li>
        <li><strong>Data Akun</strong> &mdash; nama lengkap dan username yang terdaftar di sistem AMPERA247.</li>
        <li><strong>Data Aktivitas Layanan</strong> &mdash; riwayat penggunaan fitur (antrian online, e-form kecelakaan, sertifikasi, rehabilitasi, konseling) beserta waktu dan detail pengajuan.</li>
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
        <li>Menyediakan dan mengelola fitur layanan publik digital (antrian online, e-form kecelakaan, sertifikasi online, rehabilitasi, dan konseling).</li>
        <li>Memproses pengajuan layanan yang disampaikan pengguna melalui aplikasi.</li>
        <li>Menggunakan data lokasi untuk memudahkan pengguna melaporkan titik kejadian pada e-Form Kecelakaan.</li>
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
        <li>Tim pengelola AMPERA247 dan CV Mitra Hoki Maju Mapan (Tim AMPERA247) yang memiliki kewenangan dan akses sistem yang sah.</li>
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
        <li>Mencabut izin akses lokasi kapan saja melalui pengaturan perangkat &mdash; namun hal ini akan menonaktifkan fitur deteksi lokasi otomatis pada e-Form Kecelakaan.</li>
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
    <p style="margin-top:10px"><strong style="color:#fff">CV Mitra Hoki Maju Mapan (Tim AMPERA247)</strong></p>
    <p>Pengembang Aplikasi AMPERA247</p>
    <p style="margin-top:8px"><a href="mailto:dharukun@yahoo.com">dharukun@yahoo.com</a></p>
  </div>
</div>
<div class="footer">&copy; 2026 AMPERA247 &mdash; CV Mitra Hoki Maju Mapan (Tim AMPERA247). Seluruh hak dilindungi.</div>
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
  <p class="header-sub">Aplikasi AMPERA247 &mdash; Layanan Publik Digital Kota Palembang</p>
  <div class="header-divider"></div>
</div>
<div class="container">
  <div class="intro">
    <p><strong>Terakhir diperbarui: 31 Juli 2026</strong><br>
    CV Mitra Hoki Maju Mapan (Tim AMPERA247) selaku pengembang aplikasi <strong>AMPERA247</strong> berkomitmen penuh
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
        <li><strong>Email:</strong> dharukun@yahoo.com &mdash; dengan subjek "Laporan Keselamatan Anak"</li>
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
    <p style="margin-top:10px"><strong style="color:#fff">CV Mitra Hoki Maju Mapan (Tim AMPERA247) — Tim AMPERA247</strong></p>
    <p style="margin-top:6px"><a href="mailto:dharukun@yahoo.com">dharukun@yahoo.com</a></p>
    <p style="margin-top:4px">Subjek: <em>Laporan Keselamatan Anak</em></p>
  </div>
</div>
<div class="footer">&copy; 2026 AMPERA247 &mdash; CV Mitra Hoki Maju Mapan (Tim AMPERA247). Seluruh hak dilindungi.</div>
</body>
</html>"""


_SUPPORT_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dukungan &amp; Bantuan – AMPERA247</title>
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
.faq-item{border-bottom:1px solid #DDE6F0;padding:14px 0}
.faq-item:last-child{border-bottom:none}
.faq-q{font-size:14px;font-weight:700;color:#0D1526;margin-bottom:6px}
.faq-a{font-size:14px;color:#64748B}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px}
@media(max-width:480px){.contact-grid{grid-template-columns:1fr}}
.contact-card{background:#fff;border:1px solid #DDE6F0;border-radius:12px;padding:18px 20px;text-align:center}
.contact-card-icon{width:44px;height:44px;border-radius:50%;background:rgba(21,101,192,.1);display:flex;align-items:center;justify-content:center;margin:0 auto 12px}
.contact-card-icon svg{width:22px;height:22px}
.contact-card h4{font-size:14px;font-weight:700;color:#0D1526;margin-bottom:4px}
.contact-card p{font-size:13px;color:#64748B}
.contact-card a{color:#1565C0;text-decoration:none;font-weight:600}
.doc-links{display:flex;flex-direction:column;gap:10px;margin-top:4px}
.doc-link{display:flex;align-items:center;gap:10px;padding:12px 16px;background:#F4F9FF;border:1px solid #DDE6F0;border-radius:8px;text-decoration:none;color:#1565C0;font-size:14px;font-weight:600}
.doc-link svg{width:16px;height:16px;flex-shrink:0}
.badge-hours{display:inline-block;background:rgba(21,101,192,.1);color:#1565C0;font-size:12px;font-weight:700;padding:2px 10px;border-radius:20px;margin-top:6px}
.footer{text-align:center;padding:12px 24px 24px;color:#64748B;font-size:12px}
</style>
</head>
<body>
<div class="header">
  <div class="header-badge"><span>Pusat Bantuan</span></div>
  <h1>Dukungan &amp; Bantuan</h1>
  <p class="header-sub">Aplikasi AMPERA247 &mdash; Layanan Publik Digital Kota Palembang</p>
  <div class="header-divider"></div>
</div>
<div class="container">
  <div class="intro">
    <p><strong>Kami siap membantu Anda.</strong><br>
    Temukan jawaban atas pertanyaan umum di bawah ini, atau hubungi tim kami
    langsung melalui email. Kami akan merespons setiap pertanyaan dalam waktu
    <strong>1 &times; 24 jam</strong> pada hari kerja.</p>
  </div>

  <div class="contact-grid">
    <div class="contact-card">
      <div class="contact-card-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
      </div>
      <h4>Email Dukungan</h4>
      <p><a href="mailto:dharukun@yahoo.com">dharukun@yahoo.com</a></p>
      <span class="badge-hours">Senin &ndash; Jumat, 08.00 &ndash; 17.00 WIB</span>
    </div>
    <div class="contact-card">
      <div class="contact-card-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      </div>
      <h4>Waktu Respons</h4>
      <p>Laporan teknis direspons dalam</p>
      <span class="badge-hours">Maks. 1 &times; 24 jam kerja</span>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      </div>
      <div class="section-title">Pertanyaan Umum (FAQ)</div>
    </div>
    <div class="section-body">
      <div class="faq-item">
        <div class="faq-q">Bagaimana cara mendaftar akun AMPERA247?</div>
        <div class="faq-a">Buka aplikasi, pilih "Daftar", lalu isi nama lengkap, nomor telepon, dan buat kata sandi. Akun Anda akan langsung aktif setelah pendaftaran selesai.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Aplikasi tidak bisa login setelah update. Apa yang harus dilakukan?</div>
        <div class="faq-a">Coba hapus cache aplikasi melalui Pengaturan perangkat &gt; Aplikasi &gt; AMPERA247 &gt; Hapus Cache. Jika masih bermasalah, logout lalu login kembali. Hubungi kami jika masalah berlanjut.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">GPS saya tidak terdeteksi saat mengisi e-Form Kecelakaan.</div>
        <div class="faq-a">Pastikan izin lokasi sudah diberikan untuk aplikasi AMPERA247 di pengaturan perangkat Anda. Aktifkan GPS perangkat dan pastikan Anda berada di lokasi dengan sinyal yang baik.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Bagaimana cara menghapus akun saya?</div>
        <div class="faq-a">Buka menu Profil di dalam aplikasi, pilih "Hapus Akun", lalu ikuti langkah konfirmasi. Seluruh data Anda akan dihapus secara permanen dari sistem kami.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Apakah data saya aman?</div>
        <div class="faq-a">Ya. Seluruh transmisi data menggunakan protokol HTTPS yang terenkripsi. Data Anda tidak dijual atau dibagikan kepada pihak komersial manapun. Baca Kebijakan Privasi kami untuk informasi lengkap.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Status pengajuan saya sudah lama tidak berubah.</div>
        <div class="faq-a">Waktu pemrosesan bergantung pada instansi terkait. Pastikan notifikasi aplikasi diaktifkan agar Anda tidak melewatkan pembaruan status. Untuk pengajuan lebih dari 7 hari kerja, hubungi kami via email dengan menyertakan nomor pengajuan.</div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
      </div>
      <div class="section-title">Dokumen Resmi</div>
    </div>
    <div class="section-body">
      <div class="doc-links">
        <a class="doc-link" href="/kebijakan-privasi">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Kebijakan Privasi
        </a>
        <a class="doc-link" href="/kebijakan-keselamatan-anak">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
          Kebijakan Keselamatan Anak
        </a>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <div class="section-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
      </div>
      <div class="section-title">Informasi Aplikasi</div>
    </div>
    <div class="section-body">
      <ul class="item-list">
        <li><strong>Nama Aplikasi</strong>&nbsp;&mdash;&nbsp;AMPERA247</li>
        <li><strong>Pengembang</strong>&nbsp;&mdash;&nbsp;CV Mitra Hoki Maju Mapan (Tim AMPERA247)</li>
        <li><strong>Platform</strong>&nbsp;&mdash;&nbsp;Android &amp; iOS</li>
        <li><strong>Kontak Pengembang</strong>&nbsp;&mdash;&nbsp;dharukun@yahoo.com</li>
      </ul>
    </div>
  </div>
</div>
<div class="footer">&copy; 2026 AMPERA247 &mdash; CV Mitra Hoki Maju Mapan (Tim AMPERA247). Seluruh hak dilindungi.</div>
</body>
</html>"""


_MARKETING_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="AMPERA247 - Platform layanan publik digital untuk warga Kota Palembang. Antrian online, e-Form Kecelakaan, sertifikasi, rehabilitasi, dan konseling dalam satu aplikasi.">
<title>AMPERA247 – Layanan Publik Digital Kota Palembang</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#F4F9FF;color:#0D1526;line-height:1.7;font-size:15px}

/* HERO */
.hero{background:linear-gradient(145deg,#0D1526 0%,#1D2A44 60%,#1a3a6b 100%);padding:60px 24px 56px;text-align:center;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 110%,rgba(162,207,254,.12) 0%,transparent 70%);pointer-events:none}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(162,207,254,.15);border:1px solid rgba(162,207,254,.3);border-radius:20px;padding:5px 16px;margin-bottom:24px}
.hero-badge span{color:#A2CFFE;font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase}
.hero-logo{width:72px;height:72px;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;box-shadow:0 8px 32px rgba(0,0,0,.25)}
.hero-logo svg{width:40px;height:40px}
.hero h1{color:#fff;font-size:clamp(28px,7vw,42px);font-weight:900;letter-spacing:-.5px;margin-bottom:12px;line-height:1.15}
.hero h1 span{color:#A2CFFE}
.hero-sub{color:rgba(255,255,255,.65);font-size:clamp(14px,3vw,16px);max-width:480px;margin:0 auto 32px}
.btn-row{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.btn-store{display:inline-flex;align-items:center;gap:10px;padding:12px 22px;border-radius:12px;text-decoration:none;font-weight:700;font-size:14px;transition:transform .15s,box-shadow .15s}
.btn-android{background:#fff;color:#0D1526}
.btn-android:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.2)}
.btn-ios{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.25)}
.btn-ios:hover{background:rgba(255,255,255,.2);transform:translateY(-2px)}
.btn-store svg{width:22px;height:22px;flex-shrink:0}
.hero-divider{width:40px;height:3px;background:#A2CFFE;border-radius:2px;margin:40px auto 0;opacity:.5}

/* STATS */
.stats{background:#fff;border-bottom:1px solid #DDE6F0}
.stats-inner{max-width:760px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);text-align:center;padding:28px 20px}
.stat-val{font-size:clamp(22px,5vw,28px);font-weight:900;color:#1D2A44;line-height:1}
.stat-label{font-size:12px;color:#64748B;margin-top:4px}

/* CONTAINER */
.container{max-width:760px;margin:0 auto;padding:36px 20px 60px}
.section-label{font-size:11px;font-weight:800;color:#1565C0;letter-spacing:1.4px;text-transform:uppercase;margin-bottom:10px}
.section-title{font-size:clamp(20px,4vw,26px);font-weight:900;color:#0D1526;line-height:1.25;margin-bottom:8px}
.section-desc{color:#64748B;font-size:14px;margin-bottom:28px}

/* FEATURES */
.features{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:40px}
@media(max-width:480px){.features{grid-template-columns:1fr}}
.feat{background:#fff;border:1px solid #DDE6F0;border-radius:14px;padding:20px;transition:box-shadow .2s}
.feat:hover{box-shadow:0 4px 20px rgba(21,101,192,.1)}
.feat-icon{width:42px;height:42px;border-radius:10px;background:rgba(21,101,192,.08);display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.feat-icon svg{width:22px;height:22px}
.feat h3{font-size:14px;font-weight:800;color:#0D1526;margin-bottom:6px}
.feat p{font-size:13px;color:#64748B;line-height:1.55}

/* HOW */
.how{background:#fff;border:1px solid #DDE6F0;border-radius:14px;overflow:hidden;margin-bottom:40px}
.how-step{display:flex;gap:16px;padding:18px 20px;border-bottom:1px solid #DDE6F0}
.how-step:last-child{border-bottom:none}
.step-num{width:32px;height:32px;border-radius:50%;background:#1D2A44;color:#fff;font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px}
.step-body h4{font-size:14px;font-weight:700;color:#0D1526;margin-bottom:3px}
.step-body p{font-size:13px;color:#64748B}

/* DISCLAIMER */
.disclaimer{background:#FFF7ED;border:1px solid #FED7AA;border-radius:12px;padding:18px 20px;margin-bottom:28px}
.disclaimer p{font-size:13px;color:#92400E;line-height:1.6}
.disclaimer strong{color:#78350F}

/* ABOUT */
.about{background:#1D2A44;border-radius:14px;padding:28px 24px;text-align:center;margin-bottom:28px}
.about h3{color:#fff;font-size:18px;font-weight:800;margin-bottom:8px}
.about p{color:rgba(255,255,255,.6);font-size:13px;line-height:1.6;max-width:520px;margin:0 auto 16px}
.about a{color:#A2CFFE;text-decoration:none;font-weight:700}

/* FOOTER */
.footer{text-align:center;padding:12px 24px 28px;color:#64748B;font-size:12px}
.footer a{color:#1565C0;text-decoration:none}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-badge"><span>Platform Layanan Publik Digital</span></div>
  <div class="hero-logo">
    <svg viewBox="0 0 40 40" fill="none">
      <rect width="40" height="40" rx="10" fill="#1D2A44"/>
      <path d="M20 8 L32 14 L32 26 L20 32 L8 26 L8 14 Z" stroke="#A2CFFE" stroke-width="2" fill="none"/>
      <circle cx="20" cy="20" r="4" fill="#A2CFFE"/>
    </svg>
  </div>
  <h1>AMPERA<span>247</span></h1>
  <p class="hero-sub">Akses layanan publik Kota Palembang kapan saja dan di mana saja, langsung dari smartphone Anda.</p>
  <div class="btn-row">
    <a class="btn-store btn-android" href="https://play.google.com/store/apps/details?id=id.polisibaik.ampera247" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.18 23.76c.3.16.65.18.97.06L14.76 12 3.15.18C2.83.06 2.48.08 2.18.24 1.6.56 1.25 1.19 1.25 1.88v20.24c0 .69.35 1.32.93 1.64zM17.22 8.79l-2.44-2.44 2.44-2.44 2.89 1.67c.83.48.83 1.71 0 2.19l-2.89 1.02zM16.07 10l-1.31 1.31L4.43 2l11.64 8zM16.07 14l-1.31-1.31L4.43 22l11.64-8z"/></svg>
      Google Play
    </a>
    <a class="btn-store btn-ios" href="#" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>
      App Store
    </a>
  </div>
  <div class="hero-divider"></div>
</div>

<div class="stats">
  <div class="stats-inner">
    <div>
      <div class="stat-val">7+</div>
      <div class="stat-label">Layanan Tersedia</div>
    </div>
    <div>
      <div class="stat-val">24/7</div>
      <div class="stat-label">Akses Kapan Saja</div>
    </div>
    <div>
      <div class="stat-val">GPS</div>
      <div class="stat-label">Deteksi Lokasi Otomatis</div>
    </div>
  </div>
</div>

<div class="container">
  <p class="section-label">Fitur Unggulan</p>
  <h2 class="section-title">Semua layanan publik dalam satu aplikasi</h2>
  <p class="section-desc">Tidak perlu antre panjang atau datang langsung. AMPERA247 menghadirkan kemudahan akses layanan untuk seluruh warga Kota Palembang.</p>

  <div class="features">
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
      </div>
      <h3>Antrian Online</h3>
      <p>Ambil nomor antrian dari mana saja. Pantau posisi secara real-time tanpa harus hadir di lokasi.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
      </div>
      <h3>e-Form Kecelakaan</h3>
      <p>Laporkan kejadian kecelakaan langsung dari lokasi. GPS mendeteksi koordinat secara otomatis.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
      </div>
      <h3>Sertifikasi Online</h3>
      <p>Ikuti tes sertifikasi kesehatan kapan saja. Sertifikat digital langsung tersedia setelah lulus.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.42 2 2 0 0 1 3.6 1.24h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6 6z"/></svg>
      </div>
      <h3>Konseling Online</h3>
      <p>Konsultasi dengan konselor profesional melalui chat real-time. Layanan rahasia dan tersedia kapan saja.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
      </div>
      <h3>Program Rehabilitasi</h3>
      <p>Ajukan permohonan program rehabilitasi secara digital, tanpa perlu datang langsung.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 3v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
      </div>
      <h3>Cek Status Kendaraan</h3>
      <p>Lacak informasi kendaraan menggunakan nomor kendaraan, nomor rangka, atau nomor mesin.</p>
    </div>
  </div>

  <p class="section-label">Cara Menggunakan</p>
  <h2 class="section-title">Mulai dalam 3 langkah mudah</h2>
  <p class="section-desc">Tidak perlu registrasi rumit. Cukup unduh, daftar, dan langsung gunakan.</p>

  <div class="how">
    <div class="how-step">
      <div class="step-num">1</div>
      <div class="step-body">
        <h4>Unduh Aplikasi</h4>
        <p>Unduh AMPERA247 gratis dari Google Play Store atau Apple App Store.</p>
      </div>
    </div>
    <div class="how-step">
      <div class="step-num">2</div>
      <div class="step-body">
        <h4>Buat Akun</h4>
        <p>Daftarkan diri menggunakan nama lengkap dan nomor telepon. Proses berlangsung kurang dari 1 menit.</p>
      </div>
    </div>
    <div class="how-step">
      <div class="step-num">3</div>
      <div class="step-body">
        <h4>Gunakan Layanan</h4>
        <p>Pilih layanan yang dibutuhkan dari dashboard. Semua fitur langsung tersedia setelah masuk.</p>
      </div>
    </div>
  </div>

  <div class="disclaimer">
    <p><strong>Pernyataan Penyangkalan:</strong> AMPERA247 adalah aplikasi yang dikembangkan oleh CV Mitra Hoki Maju Mapan (Tim AMPERA247), perusahaan swasta independen. Aplikasi ini tidak berafiliasi dengan, tidak mewakili, dan tidak beroperasi atas nama instansi pemerintah manapun. AMPERA247 merupakan platform teknologi yang memfasilitasi akses informasi dan layanan publik secara digital.</p>
  </div>

  <div class="about">
    <h3>Dikembangkan oleh CV Mitra Hoki Maju Mapan (Tim AMPERA247)</h3>
    <p>CV Mitra Hoki Maju Mapan (Tim AMPERA247) adalah perusahaan teknologi yang berkomitmen menghadirkan solusi digitalisasi layanan publik yang modern, terpercaya, dan mudah diakses oleh seluruh lapisan masyarakat.</p>
    <a href="mailto:dharukun@yahoo.com">dharukun@yahoo.com</a>
  </div>
</div>

<div class="footer">
  &copy; 2026 AMPERA247 &mdash; CV Mitra Hoki Maju Mapan (Tim AMPERA247). Seluruh hak dilindungi. &nbsp;|&nbsp;
  <a href="/kebijakan-privasi">Kebijakan Privasi</a> &nbsp;|&nbsp;
  <a href="/dukungan">Dukungan</a>
</div>
</body>
</html>"""


class PrivacyPolicyController(http.Controller):

    @http.route('/kebijakan-privasi', type='http', auth='public', website=False, csrf=False)
    def privacy_policy(self, **kwargs):
        return Response(_PRIVACY_HTML, content_type='text/html; charset=utf-8')

    @http.route('/kebijakan-keselamatan-anak', type='http', auth='public', website=False, csrf=False)
    def child_safety(self, **kwargs):
        return Response(_CHILD_SAFETY_HTML, content_type='text/html; charset=utf-8')

    @http.route('/dukungan', type='http', auth='public', website=False, csrf=False)
    def support(self, **kwargs):
        return Response(_SUPPORT_HTML, content_type='text/html; charset=utf-8')

    @http.route('/ampera247', type='http', auth='public', website=False, csrf=False)
    def marketing(self, **kwargs):
        return Response(_MARKETING_HTML, content_type='text/html; charset=utf-8')
