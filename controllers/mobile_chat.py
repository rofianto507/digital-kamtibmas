import json
from markupsafe import Markup
from odoo import http
from odoo.http import request


class MobileChatController(http.Controller):

    @http.route(
        '/mobile/konseling/chat/<int:channel_id>',
        auth='user', type='http', website=False, csrf=False,
    )
    def mobile_chat_page(self, channel_id, **kwargs):
        channel = request.env['discuss.channel'].sudo().browse(channel_id)
        if not channel.exists():
            return request.not_found()

        # Pastikan user saat ini adalah anggota channel
        is_member = request.env['discuss.channel.member'].sudo().search_count([
            ('channel_id', '=', channel_id),
            ('partner_id', '=', request.env.user.partner_id.id),
        ])
        if not is_member:
            return request.make_response(
                'Akses ditolak',
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=403,
            )

        return request.render('digital_kamtibmas.mobile_chat_template', {
            'channel_id': channel_id,
            'channel_name': channel.name,
            'channel_name_json': Markup(json.dumps(channel.name)),
            'current_partner_id': request.env.user.partner_id.id,
        })
