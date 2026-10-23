import uuid
from odoo import models, fields, api
from odoo.exceptions import UserError

from .utils import public_base_url

PARAM_KIOSK_TOKEN = 'digital_kamtibmas.tahti_kiosk_token'


class TahtiKioskConfig(models.TransientModel):
    _name        = 'digital_kamtibmas.tahti_kiosk_config'
    _description = 'Konfigurasi URL Kiosk Buku Tamu Tahti'

    token     = fields.Char('Token', readonly=True)
    kiosk_url = fields.Char('URL Kiosk', readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        tok = self.env['ir.config_parameter'].sudo().get_param(PARAM_KIOSK_TOKEN, '')
        res['token']     = tok
        res['kiosk_url'] = self._kiosk_url(tok) if tok else ''
        return res

    def _kiosk_url(self, tok):
        return f'{public_base_url(self.env)}/tahti/buku-tamu/{tok}'

    def action_generate_token(self):
        tok = uuid.uuid4().hex
        self.env['ir.config_parameter'].sudo().set_param(PARAM_KIOSK_TOKEN, tok)
        new = self.create({'token': tok, 'kiosk_url': self._kiosk_url(tok)})
        return {
            'type':      'ir.actions.act_window',
            'res_model': 'digital_kamtibmas.tahti_kiosk_config',
            'view_mode': 'form',
            'res_id':    new.id,
            'target':    'new',
        }

    def action_open_kiosk(self):
        tok = self.env['ir.config_parameter'].sudo().get_param(PARAM_KIOSK_TOKEN, '')
        if not tok:
            raise UserError('Generate token terlebih dahulu.')
        return {'type': 'ir.actions.act_url', 'url': self._kiosk_url(tok), 'target': 'new'}
