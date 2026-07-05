from odoo import http
from odoo.http import request
import json
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

# Wablas status string → status log Odoo
_STATUS_MAP = {
    'pending': 'pending',
    'process': 'pending',
    'sent': 'delivered',
    'delivered': 'delivered',
    'read': 'read',
    'failed': 'failed',
    'cancel': 'failed',
}


class IntelkamWebhookController(http.Controller):

    @http.route('/intelkam/webhook/wablas', type='http', auth='public',
                methods=['POST'], csrf=False)
    def wablas_incoming(self, **kwargs):
        """Webhook pesan masuk dari group WhatsApp."""
        try:
            body = request.httprequest.get_data(as_text=True)
            data = json.loads(body) if body else {}
            _logger.info('Wablas incoming webhook: %s', data)

            messages = data if isinstance(data, list) else [data]

            for msg in messages:
                # Abaikan event tanpa konten sama sekali (read receipt, notifikasi grup, dsb)
                has_text = bool((msg.get('message') or '').strip())
                has_file = bool((msg.get('file') or msg.get('url') or '').strip())
                if not has_text and not has_file:
                    continue

                group_id_wa = msg.get('groupId') or msg.get('phone', '')
                is_group = msg.get('isGroup', False)
                # Abaikan pesan bukan dari group
                if not is_group and '@g.us' not in str(group_id_wa):
                    continue

                # Timestamp bisa ISO string ("2026-07-04T23:57:12Z") atau Unix int
                ts = msg.get('timestamp')
                tanggal = datetime.utcnow()
                if ts:
                    try:
                        tanggal = datetime.utcfromtimestamp(int(ts))
                    except (ValueError, TypeError):
                        try:
                            ts_str = str(ts).rstrip('Z').replace('T', ' ')
                            tanggal = datetime.strptime(ts_str[:19], '%Y-%m-%d %H:%M:%S')
                        except Exception:
                            pass

                # Untuk pesan grup: pengirim asli ada di msg['group']['sender'],
                # bukan msg['sender'] (yang bisa berisi nomor bot)
                group_info = msg.get('group') or {}
                pengirim_no = (group_info.get('sender') or
                               msg.get('sender') or msg.get('phone', ''))

                # Nama: pushName kadang kosong untuk pesan grup
                nama = (msg.get('pushName') or msg.get('pushname') or
                        msg.get('senderName') or group_info.get('pushName') or '')

                request.env['intelkam.respon.wa'].sudo().create({
                    'group_id_wa': group_id_wa,
                    'pengirim': pengirim_no,
                    'nama_pengirim': nama,
                    'pesan': msg.get('message', ''),
                    'file_url': msg.get('file') or msg.get('url') or '',
                    'mime_type': msg.get('mimeType') or '',
                    'tanggal': tanggal,
                    'wablas_message_id': msg.get('id', ''),
                    'raw_payload': json.dumps(msg, ensure_ascii=False),
                })

            return request.make_response(
                json.dumps({'status': 'ok'}),
                headers=[('Content-Type', 'application/json')],
            )
        except Exception as e:
            _logger.error('Wablas incoming webhook error: %s', e, exc_info=True)
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500,
            )

    @http.route('/intelkam/webhook/wablas/tracking', type='http', auth='public',
                methods=['POST'], csrf=False)
    def wablas_tracking(self, **kwargs):
        """
        Webhook tracking status pesan dari Wablas.
        Wablas POST ke sini saat status pesan berubah (delivered, read, failed).
        Payload: {"id": "uuid", "status": "delivered", "phone": "...", ...}
        Isi field 'Tracking URL' di Wablas Device Settings dengan URL endpoint ini.
        """
        try:
            body = request.httprequest.get_data(as_text=True)
            data = json.loads(body) if body else {}
            _logger.info('Wablas tracking webhook: %s', data)

            items = data if isinstance(data, list) else [data]
            updated = 0

            for item in items:
                msg_id = item.get('id') or item.get('messageId') or item.get('message_id', '')
                wablas_status = item.get('status', '')
                if not msg_id or not wablas_status:
                    continue

                new_status = _STATUS_MAP.get(wablas_status.lower())
                if not new_status or new_status == 'pending':
                    continue

                # Cari log distribusi berdasarkan wablas_message_id
                log = request.env['intelkam.distribusi.log'].sudo().search(
                    [('wablas_message_id', '=', msg_id)], limit=1
                )
                if log and log.status != new_status:
                    log.write({'status': new_status})
                    _logger.info('Tracking update: msg %s → %s', msg_id, new_status)
                    updated += 1

            return request.make_response(
                json.dumps({'status': 'ok', 'updated': updated}),
                headers=[('Content-Type', 'application/json')],
            )
        except Exception as e:
            _logger.error('Wablas tracking webhook error: %s', e, exc_info=True)
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500,
            )
