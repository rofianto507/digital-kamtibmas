import re
import random
import string
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


def _normalize_phone(phone):
    """Normalize ke format 628xxx (tanpa + atau spasi)."""
    phone = re.sub(r'\D', '', phone.strip())
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    elif not phone.startswith('62'):
        phone = '62' + phone
    return phone


def _generate_password(length=8):
    chars = string.ascii_letters + string.digits
    while True:
        pwd = ''.join(random.choices(chars, k=length))
        if any(c.isalpha() for c in pwd) and any(c.isdigit() for c in pwd):
            return pwd


# ── Registrasi v2 (username + password) ──────────────────────────────────────
# Endpoint v1 (/mobile/dkm/register, login = nomor WA) tetap dipertahankan apa
# adanya untuk app versi lama yang sudah rilis.

_USERNAME_RE = re.compile(r'^[a-z][a-z0-9._]{3,29}$')
_RESERVED_USERNAMES = {
    'admin', 'administrator', 'root', 'system', 'support', 'dukungan',
    'polisi', 'polri', 'polrestabes', 'ampera', 'ampera247', 'ampera2407',
}


def _validate_username(username):
    """Return pesan error, atau None kalau format valid."""
    if len(username) < 4 or len(username) > 30:
        return 'Username harus 4-30 karakter'
    if not _USERNAME_RE.match(username):
        return 'Username harus diawali huruf dan hanya boleh huruf kecil, angka, titik, atau underscore'
    if username in _RESERVED_USERNAMES:
        return 'Username tidak tersedia'
    return None


def _validate_password(password):
    """Return pesan error, atau None kalau password valid."""
    if len(password) < 8:
        return 'Password minimal 8 karakter'
    if len(password) > 64:
        return 'Password maksimal 64 karakter'
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return 'Password harus kombinasi huruf dan angka'
    return None


def _username_taken(username):
    """Cek username (case-insensitive, termasuk akun yang diarsipkan)."""
    pattern = username.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
    return bool(
        request.env['res.users'].sudo().with_context(active_test=False)
        .search_count([('login', '=ilike', pattern)])
    )


class MobileRegisterController(http.Controller):

    @http.route('/mobile/dkm/v2/check-username', type='jsonrpc', auth='public', csrf=False, cors='*')
    def check_username_v2(self, username=None, **kwargs):
        username = (username or '').strip().lower()
        error = _validate_username(username)
        if error:
            return {'success': True, 'available': False, 'error': error}
        if _username_taken(username):
            return {'success': True, 'available': False, 'error': 'Username sudah dipakai'}
        return {'success': True, 'available': True}

    @http.route('/mobile/dkm/v2/register', type='jsonrpc', auth='public', csrf=False, cors='*')
    def register_v2(self, data=None, **kwargs):
        data = data or {}

        username = (data.get('username') or '').strip().lower()
        nama     = (data.get('nama') or '').strip()
        password = data.get('password') or ''
        foto_b64 = (data.get('foto') or '').strip()

        error = _validate_username(username)
        if error:
            return {'success': False, 'error': error}
        if not nama:
            return {'success': False, 'error': 'Nama wajib diisi'}
        error = _validate_password(password)
        if error:
            return {'success': False, 'error': error}
        if _username_taken(username):
            return {'success': False, 'error': 'Username sudah dipakai'}

        try:
            group_masyarakat = request.env.ref('digital_kamtibmas.group_masyarakat')
            group_user = request.env.ref('base.group_user')

            create_vals = {
                'name': nama,
                'login': username,
                'password': password,
                'group_ids': [(4, group_masyarakat.id), (4, group_user.id)],
            }
            if foto_b64:
                create_vals['image_1920'] = foto_b64

            user = request.env['res.users'].sudo().create(create_vals)
            _logger.info('REGISTER v2: user created id=%s login=%s', user.id, user.login)
            return {
                'success': True,
                'login': username,
                'message': 'Registrasi berhasil! Silakan login.',
            }
        except Exception:
            _logger.exception('Registration v2 error untuk %s', username)
            return {'success': False, 'error': 'Terjadi kesalahan server. Silakan coba lagi.'}

    @http.route('/mobile/dkm/register', type='jsonrpc', auth='public', csrf=False, cors='*')
    def register(self, data=None, **kwargs):
        data = data or {}

        nama     = (data.get('nama') or '').strip()
        phone    = (data.get('phone') or '').strip()
        alamat   = (data.get('alamat') or '').strip()
        foto_b64 = (data.get('foto') or '').strip()

        if not nama:
            return {'success': False, 'error': 'Nama wajib diisi'}
        if not phone:
            return {'success': False, 'error': 'Nomor WhatsApp wajib diisi'}

        phone_normalized = _normalize_phone(phone)
        if len(phone_normalized) < 10:
            return {'success': False, 'error': 'Nomor WhatsApp tidak valid'}

        login = phone_normalized

        existing = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
        if existing:
            return {'success': False, 'error': 'Nomor WhatsApp sudah terdaftar'}

        password = _generate_password()

        try:
            group_masyarakat = request.env.ref('digital_kamtibmas.group_masyarakat')
            group_user = request.env.ref('base.group_user')

            create_vals = {
                'name': nama,
                'login': login,
                'password': password,
                'phone': phone_normalized,
                'group_ids': [(4, group_masyarakat.id), (4, group_user.id)],
            }
            if alamat:
                create_vals['street'] = alamat
            if foto_b64:
                create_vals['image_1920'] = foto_b64

            user = request.env['res.users'].sudo().create(create_vals)
            _logger.info('REGISTER: user created id=%s login=%s', user.id, user.login)

            # Kirim info login via WhatsApp
            try:
                wa_config = request.env['intelkam.wa.config'].sudo().get_config()
                wa_msg = (
                    f"*Registrasi AMPERA PBM Berhasil* ✅\n\n"
                    f"Halo *{nama}*,\n"
                    f"Akun Anda telah berhasil dibuat.\n\n"
                    f"🔑 *Informasi Login:*\n"
                    f"Username: {login}\n"
                    f"Password: {password}\n\n"
                    f"Silakan login di aplikasi AMPERA PBM.\n"
                    f"_Jangan bagikan informasi ini ke siapapun._"
                )
                result = wa_config.send_message(phone_normalized, wa_msg)
                if not result.get('success'):
                    _logger.warning('WA gagal untuk %s: %s', login, result.get('error'))
            except Exception as wa_err:
                _logger.warning('WA exception untuk %s: %s', login, wa_err)
                # Gagal kirim WA tidak membatalkan registrasi

            return {
                'success': True,
                'login': login,
                'message': 'Registrasi berhasil! Cek WhatsApp Anda untuk informasi login.',
            }

        except Exception:
            _logger.exception('Registration error untuk %s', login)
            return {'success': False, 'error': 'Terjadi kesalahan server. Silakan coba lagi.'}
