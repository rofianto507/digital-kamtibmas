import uuid
from odoo import models, fields, api
from odoo.exceptions import UserError

PARAM_TOKEN = 'digital_kamtibmas.display_token'


class AntrianDisplayConfig(models.TransientModel):
    _name        = 'digital_kamtibmas.display_config'
    _description = 'Konfigurasi URL Display Antrian'

    token       = fields.Char('Token', readonly=True)
    display_url = fields.Char('URL Display', readonly=True)

    @api.model
    def default_get(self, fields_list):
        res  = super().default_get(fields_list)
        tok  = self.env['ir.config_parameter'].sudo().get_param(PARAM_TOKEN, '')
        base = self.env['ir.config_parameter'].sudo().get_param('web.base.url', 'http://localhost:8069')
        res['token']       = tok
        res['display_url'] = f'{base}/antrian/{tok}' if tok else ''
        return res

    def _base_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url', 'http://localhost:8069')

    def action_generate_token(self):
        tok = uuid.uuid4().hex
        self.env['ir.config_parameter'].sudo().set_param(PARAM_TOKEN, tok)
        new = self.create({
            'token':       tok,
            'display_url': f'{self._base_url()}/antrian/{tok}',
        })
        return {
            'type':      'ir.actions.act_window',
            'res_model': 'digital_kamtibmas.display_config',
            'view_mode': 'form',
            'res_id':    new.id,
            'target':    'new',
        }

    def action_open_display(self):
        tok = self.env['ir.config_parameter'].sudo().get_param(PARAM_TOKEN, '')
        if not tok:
            raise UserError('Generate token terlebih dahulu.')
        return {
            'type':   'ir.actions.act_url',
            'url':    f'{self._base_url()}/antrian/{tok}',
            'target': 'new',
        }
