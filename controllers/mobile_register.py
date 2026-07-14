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


class MobileRegisterController(http.Controller):

    @http.route('/mobile/dkm/register', type='jsonrpc', auth='public', csrf=False)
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
                    f"*Registrasi AMPERA247 Berhasil* ✅\n\n"
                    f"Halo *{nama}*,\n"
                    f"Akun Anda telah berhasil dibuat.\n\n"
                    f"🔑 *Informasi Login:*\n"
                    f"Username: {login}\n"
                    f"Password: {password}\n\n"
                    f"Silakan login di aplikasi AMPERA247.\n"
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
