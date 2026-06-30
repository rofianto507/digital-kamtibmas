import json
from odoo import http, fields
from odoo.http import request, Response

PARAM_TOKEN = 'digital_kamtibmas.display_token'


def _valid_token(token):
    stored = request.env['ir.config_parameter'].sudo().get_param(PARAM_TOKEN, '')
    return stored and token == stored


class AntrianDisplayController(http.Controller):

    # ── Halaman display (publik) ───────────────────────────────────────────────

    @http.route('/antrian/<string:token>', type='http', auth='public', csrf=False)
    def display_page(self, token, **kw):
        if not _valid_token(token):
            return Response(
                '<body style="font-family:sans-serif;padding:60px;color:#666">'
                '<h2>403 — URL tidak valid atau sudah kedaluwarsa.</h2>'
                '<p>Hubungi administrator untuk mendapatkan URL baru.</p></body>',
                content_type='text/html', status=403,
            )
        return request.render('digital_kamtibmas.antrian_display_page', {'token': token})

    # ── API data (publik, JSON via GET) ───────────────────────────────────────

    @http.route('/antrian/<string:token>/data', type='http', auth='public', csrf=False, methods=['GET'])
    def display_data(self, token, **kw):
        if not _valid_token(token):
            return Response(json.dumps({'error': 'invalid_token'}),
                            content_type='application/json', status=403)

        today   = fields.Date.today()
        Loket   = request.env['digital_kamtibmas.loket'].sudo()
        Antrian = request.env['digital_kamtibmas.antrian'].sudo()

        lokets = Loket.search([('state', '=', 'aktif')], order='name asc')
        result = []
        for loket in lokets:
            dipanggil = Antrian.search([
                ('loket_id', '=', loket.id),
                ('tanggal_booking', '=', today),
                ('state', '=', 'dipanggil'),
            ], order='nomor_urut asc')

            menunggu = Antrian.search([
                ('loket_id', '=', loket.id),
                ('tanggal_booking', '=', today),
                ('state', '=', 'konfirmasi'),
            ], order='nomor_urut asc', limit=5)

            result.append({
                'loket':     loket.name,
                'layanan':   loket.layanan_id.name or '',
                'dipanggil': [{'nomor': a.nomor_antrian, 'nama': a.atas_nama} for a in dipanggil],
                'menunggu':  [{'nomor': a.nomor_antrian, 'nama': a.atas_nama} for a in menunggu],
            })

        return Response(
            json.dumps({'lokets': result}),
            content_type='application/json',
        )
