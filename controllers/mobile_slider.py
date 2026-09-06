import json
from odoo import http
from odoo.http import request, Response


class MobileSliderController(http.Controller):

    @http.route('/api/mobile/slider', type='http', auth='public', methods=['GET'], csrf=False)
    def get_slider(self, **kwargs):
        records = request.env['digital.kamtibmas.slider'].sudo().search([
            ('active', '=', True),
        ])

        items = [
            {
                'id': r.id,
                'name': r.name,
                'image_url': f'/web/image/digital.kamtibmas.slider/{r.id}/image',
            }
            for r in records
        ]

        return Response(
            json.dumps({'result': items}),
            content_type='application/json',
            headers={'Access-Control-Allow-Origin': '*'},
        )
