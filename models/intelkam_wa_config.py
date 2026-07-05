from odoo import models, fields, api, exceptions
import requests
import logging

_logger = logging.getLogger(__name__)


class IntelkamWaConfig(models.Model):
    _name = 'intelkam.wa.config'
    _description = 'Konfigurasi Wablas API'
    _rec_name = 'name'

    name = fields.Char('Nama Konfigurasi', required=True, default='Konfigurasi Utama')
    base_url = fields.Char('Base URL', required=True, default='https://jogja.wablas.com')
    token = fields.Char('API Token', required=True)
    secret_key = fields.Char('Secret Key', required=True)
    nomor_bot = fields.Char('Nomor Bot WhatsApp', required=True,
                             help='Nomor WhatsApp bot tanpa + (contoh: 6285608855007)')
    active = fields.Boolean(default=True)
    notes = fields.Text('Catatan')

    @api.model
    def get_config(self):
        config = self.sudo().search([('active', '=', True)], limit=1)
        if not config:
            raise exceptions.UserError(
                'Konfigurasi Wablas belum diatur. '
                'Silakan isi token dan secret key di menu Intelkam > Konfigurasi Wablas.'
            )
        return config

    def _auth_header(self):
        """Header Authorization untuk POST (send-message)."""
        return {
            'Authorization': f'{self.token.strip()}.{self.secret_key.strip()}',
            'Content-Type': 'application/json',
        }

    def send_message(self, phone, message, is_group=False):
        """
        Kirim pesan via Wablas API v2.
        Response Wablas: {status: true, data: {device_id, quota, messages: [{id, status:'pending', ...}]}}
        Return: {success, message_id, wablas_status, error}
        """
        self.ensure_one()
        url = f'{self.base_url.rstrip("/")}/api/v2/send-message'
        payload = {
            'data': [{
                'phone': phone,
                'message': message,
                'isGroup': 'true' if is_group else 'false',
            }]
        }
        try:
            resp = requests.post(url, json=payload, headers=self._auth_header(), timeout=30)
            resp.raise_for_status()
        except requests.exceptions.Timeout:
            return {'success': False, 'message_id': '', 'wablas_status': 'failed', 'error': 'Request timeout (30s)'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message_id': '', 'wablas_status': 'failed', 'error': str(e)}

        try:
            data = resp.json()
        except Exception:
            return {'success': False, 'message_id': '', 'wablas_status': 'failed',
                    'error': f'Response bukan JSON: {resp.text[:300]}'}

        _logger.info('Wablas send_message [%s] HTTP=%s body=%s', phone, resp.status_code, data)

        # Jika Wablas menolak (auth gagal, dsb)
        if not data.get('status'):
            return {'success': False, 'message_id': '', 'wablas_status': 'failed',
                    'error': data.get('message') or str(data)}

        # Wablas status=True → pesan diterima / diantrekan
        # Struktur: data['data']['messages'][0] = {id, status:'pending', phone, ...}
        message_id = ''
        wablas_status = 'pending'
        try:
            nested = data['data']           # dict: {device_id, quota, messages:[...]}
            first_msg = nested['messages'][0]
            message_id = first_msg.get('id', '')
            wablas_status = first_msg.get('status', 'pending')
        except (KeyError, IndexError, TypeError) as e:
            _logger.warning('Wablas parse messages: %s | full response: %s', e, data)

        return {'success': True, 'message_id': message_id, 'wablas_status': wablas_status, 'error': ''}

    def check_message_status(self, message_id):
        """
        Cek status pengiriman pesan via Wablas.
        Coba beberapa endpoint dan format auth karena Wablas tidak konsisten dokumentasinya.
        Return: status string ('pending'|'sent'|'delivered'|'read'|'failed') atau None.
        """
        self.ensure_one()
        if not message_id:
            return None

        base = self.base_url.rstrip('/')
        candidates = [
            (f'{base}/api/message', {'id': message_id}, self.token.strip()),
            (f'{base}/api/message', {'id': message_id}, f'{self.token.strip()}.{self.secret_key.strip()}'),
            (f'{base}/api/v2/message/{message_id}', {}, f'{self.token.strip()}.{self.secret_key.strip()}'),
            (f'{base}/api/v2/message', {'id': message_id}, f'{self.token.strip()}.{self.secret_key.strip()}'),
        ]
        for url, params, auth in candidates:
            try:
                resp = requests.get(url, params=params, headers={'Authorization': auth}, timeout=10)
                if resp.status_code == 404:
                    continue
                data = resp.json()
                _logger.info('Wablas check status [%s] via %s: %s', message_id, url, data)
                if data.get('status'):
                    msg_data = data.get('data') or {}
                    if isinstance(msg_data, dict):
                        s = msg_data.get('status')
                        if s:
                            return s
                    if isinstance(msg_data, list) and msg_data:
                        return msg_data[0].get('status')
            except Exception as e:
                _logger.debug('Wablas check status [%s] %s error: %s', message_id, url, e)
        return None

    def action_test_connection(self):
        self.ensure_one()
        url = f'{self.base_url.rstrip("/")}/api/v2/send-message'
        payload = {
            'data': [{
                'phone': self.nomor_bot.strip(),
                'message': '[TEST] Koneksi Wablas dari Odoo Digital Kamtibmas berhasil.',
                'isGroup': 'false',
            }]
        }
        try:
            resp = requests.post(url, json=payload, headers=self._auth_header(), timeout=15)
            data = resp.json()
            _logger.info('Wablas test connection [HTTP %s]: %s', resp.status_code, data)
            success = bool(data.get('status'))
            error_msg = '' if success else (data.get('message') or str(data))
            if success:
                msg = (
                    f"Koneksi berhasil!\n"
                    f"Token & Secret Key valid.\n"
                    f"Pesan test dikirim ke nomor bot {self.nomor_bot}."
                )
                notif_type = 'success'
            else:
                msg = f"Gagal: {error_msg}"
                notif_type = 'danger'
        except Exception as e:
            msg = f"Error: {e}"
            notif_type = 'danger'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Test Koneksi Wablas',
                'message': msg,
                'type': notif_type,
                'sticky': True,
            }
        }
