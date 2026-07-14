import logging
from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


class MobileSertifikasiController(http.Controller):

    @http.route('/mobile/dkm/sertifikasi/list', type='jsonrpc', auth='public', csrf=False)
    def list_sertifikasi(self, **kwargs):
        today = str(fields.Date.today())
        domain = [
            ('state', '=', 'aktif'),
            '|',
            ('tanggal_expired', '=', False),
            ('tanggal_expired', '>=', today),
        ]
        records = request.env['digital_kamtibmas.sertifikasi'].sudo().search_read(
            domain,
            fields=[
                'id', 'name', 'tanggal_aktif', 'tanggal_expired',
                'jumlah_soal', 'waktu_menit', 'nilai_kelulusan',
                'notes', 'url_public', 'total_peserta', 'total_lulus',
            ],
            order='id desc',
        )
        # Konversi False → None agar JSON-serializable
        for rec in records:
            for key in ('tanggal_aktif', 'tanggal_expired', 'notes'):
                if rec.get(key) is False:
                    rec[key] = None
        return {'success': True, 'data': records}
