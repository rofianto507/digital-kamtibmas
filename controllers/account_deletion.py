from odoo import http, fields
from odoo.http import request, Response


# ── Web form HTML ──────────────────────────────────────────────────────────────

_FORM_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Permintaan Hapus Akun – AMPERA247</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#F4F9FF;color:#0D1526;line-height:1.6;font-size:15px;min-height:100vh;display:flex;flex-direction:column}}
.header{{background:#1D2A44;padding:28px 24px;text-align:center}}
.header h1{{color:#fff;font-size:20px;font-weight:800;margin-bottom:4px}}
.header p{{color:rgba(255,255,255,.55);font-size:13px}}
.container{{max-width:520px;margin:32px auto;padding:0 20px;flex:1}}
.card{{background:#fff;border-radius:12px;border:1px solid #DDE6F0;padding:28px 24px}}
.card h2{{font-size:16px;font-weight:700;margin-bottom:6px}}
.card .desc{{color:#64748B;font-size:13px;margin-bottom:24px;line-height:1.6}}
label{{display:block;font-size:13px;font-weight:600;color:#1D2A44;margin-bottom:6px}}
input,textarea{{width:100%;padding:10px 12px;border:1px solid #DDE6F0;border-radius:8px;font-size:14px;color:#0D1526;background:#fff;margin-bottom:16px;outline:none;font-family:inherit}}
input:focus,textarea:focus{{border-color:#1565C0;box-shadow:0 0 0 3px rgba(21,101,192,.1)}}
textarea{{resize:vertical;min-height:80px}}
.btn{{width:100%;background:#DC2626;color:#fff;border:none;border-radius:8px;padding:13px;font-size:15px;font-weight:700;cursor:pointer;margin-top:4px}}
.btn:hover{{background:#b91c1c}}
.alert{{padding:14px 16px;border-radius:8px;font-size:13px;margin-bottom:20px;display:none}}
.alert-success{{background:#dcfce7;color:#166534;border:1px solid #bbf7d0;display:block}}
.alert-error{{background:#fef2f2;color:#991b1b;border:1px solid #fecaca;display:block}}
.note{{font-size:12px;color:#94A3B8;text-align:center;margin-top:20px;line-height:1.6}}
.footer{{text-align:center;padding:20px;color:#94A3B8;font-size:12px}}
</style>
</head>
<body>
<div class="header">
  <h1>Permintaan Hapus Akun</h1>
  <p>AMPERA247 &mdash; Layanan Digital Kamtibmas Kota Palembang</p>
</div>
<div class="container">
  <div class="card">
    <h2>Formulir Permintaan</h2>
    <p class="desc">
      Isi formulir di bawah untuk mengajukan permintaan penghapusan akun AMPERA247 Anda.
      Permintaan akan diproses oleh administrator dalam <strong>maksimal 30 hari kerja</strong>.
    </p>
    <div id="msg-success" class="alert alert-success" style="display:none">
      &#10003; Permintaan Anda telah diterima. Admin akan menghubungi Anda dan memproses dalam 30 hari kerja.
    </div>
    <div id="msg-error" class="alert alert-error" style="display:none">
      Terjadi kesalahan. Silakan coba lagi.
    </div>
    <form id="frm">
      <label for="nama">Nama Lengkap *</label>
      <input type="text" id="nama" name="nama" placeholder="Nama sesuai akun" required>
      <label for="login">Username / Email *</label>
      <input type="text" id="login" name="login" placeholder="Username atau email yang terdaftar" required>
      <label for="alasan">Alasan (opsional)</label>
      <textarea id="alasan" name="alasan" placeholder="Ceritakan alasan penghapusan akun Anda (opsional)"></textarea>
      <button type="submit" class="btn" id="btn-submit">Kirim Permintaan</button>
    </form>
    <p class="note">
      Dengan mengirim formulir ini, Anda memahami bahwa seluruh data layanan,
      riwayat aktivitas, dan profil yang terkait dengan akun ini akan dihapus secara permanen.
    </p>
  </div>
</div>
<div class="footer">&copy; 2026 AMPERA247 &mdash; CV Sel Studio</div>
<script>
document.getElementById('frm').addEventListener('submit', async function(e) {{
  e.preventDefault();
  const btn = document.getElementById('btn-submit');
  btn.disabled = true; btn.textContent = 'Mengirim...';
  document.getElementById('msg-success').style.display = 'none';
  document.getElementById('msg-error').style.display = 'none';
  try {{
    const res = await fetch('/hapus-akun/submit', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{
        jsonrpc: '2.0',
        method: 'call',
        params: {{
          nama:   document.getElementById('nama').value.trim(),
          login:  document.getElementById('login').value.trim(),
          alasan: document.getElementById('alasan').value.trim(),
        }}
      }})
    }});
    const data = await res.json();
    if (data.result && data.result.ok) {{
      document.getElementById('frm').style.display = 'none';
      document.getElementById('msg-success').style.display = 'block';
    }} else {{
      document.getElementById('msg-error').style.display = 'block';
      btn.disabled = false; btn.textContent = 'Kirim Permintaan';
    }}
  }} catch {{
    document.getElementById('msg-error').style.display = 'block';
    btn.disabled = false; btn.textContent = 'Kirim Permintaan';
  }}
}});
</script>
</body>
</html>"""


class AccountDeletionController(http.Controller):

    # ── Web form (publik) ──────────────────────────────────────────────────────

    @http.route('/hapus-akun', type='http', auth='public', website=False, csrf=False)
    def hapus_akun_form(self, **kwargs):
        return Response(_FORM_HTML.format(), content_type='text/html; charset=utf-8')

    @http.route('/hapus-akun/submit', type='json', auth='public', csrf=False)
    def hapus_akun_submit(self, nama='', login='', alasan='', **kwargs):
        if not nama or not login:
            return {'ok': False, 'error': 'Data tidak lengkap'}
        user = request.env['res.users'].sudo().search(
            [('login', '=', login.strip())], limit=1)
        request.env['digital_kamtibmas.account_deletion_request'].sudo().create({
            'nama': nama.strip(),
            'login': login.strip(),
            'alasan': alasan.strip() or False,
            'user_id': user.id if user else False,
            'tanggal_request': fields.Datetime.now(),
        })
        return {'ok': True}

    # ── Mobile API (user terautentikasi) ───────────────────────────────────────

    @http.route('/api/dkm/hapus-akun', type='json', auth='user', csrf=False)
    def hapus_akun_mobile(self, alasan='', **kwargs):
        user = request.env.user
        # Cegah duplikat request yang masih pending
        existing = request.env['digital_kamtibmas.account_deletion_request'].sudo().search([
            ('user_id', '=', user.id),
            ('state', '=', 'pending'),
        ], limit=1)
        if existing:
            return {'ok': True, 'message': 'Permintaan sudah tercatat sebelumnya'}

        request.env['digital_kamtibmas.account_deletion_request'].sudo().create({
            'nama': user.name,
            'login': user.login,
            'alasan': (alasan or '').strip() or False,
            'user_id': user.id,
            'tanggal_request': fields.Datetime.now(),
        })
        return {'ok': True, 'message': 'Permintaan hapus akun berhasil dikirim'}
