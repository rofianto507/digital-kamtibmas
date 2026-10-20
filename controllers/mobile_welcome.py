import json
from datetime import date
from odoo import http
from odoo.http import request, Response


class MobileWelcomeController(http.Controller):

    @http.route('/api/mobile/welcome-screen', type='http', auth='public', methods=['GET'], csrf=False)
    def get_welcome_screen(self, **kwargs):
        today = date.today()
        domain = [
            ('active', '=', True),
            '|', ('tanggal_mulai', '=', False), ('tanggal_mulai', '<=', today),
            '|', ('tanggal_selesai', '=', False), ('tanggal_selesai', '>=', today),
        ]
        rec = request.env['digital.kamtibmas.welcome.screen'].sudo().search(domain, limit=1)

        if not rec:
            return Response(
                json.dumps({'result': None}),
                content_type='application/json',
                headers={'Access-Control-Allow-Origin': '*'},
            )

        return Response(
            json.dumps({
                'result': {
                    'id': rec.id,
                    'name': rec.name,
                    'image_url': f'/web/image/digital.kamtibmas.welcome.screen/{rec.id}/image',
                    'keterangan': rec.keterangan or '',
                    'button_label': rec.button_label or 'Lihat detail',
                    'button_url': rec.button_url or '',
                }
            }),
            content_type='application/json',
            headers={'Access-Control-Allow-Origin': '*'},
        )
