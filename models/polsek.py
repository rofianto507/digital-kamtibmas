from odoo import models, fields


class Polsek(models.Model):
    _name        = 'digital_kamtibmas.polsek'
    _description = 'Polsek — Wilayah Palembang'
    _order       = 'name asc'
    _rec_name    = 'name'

    name         = fields.Char('Nama Polsek', required=True)
    kecamatan_id = fields.Many2one('digital_kamtibmas.kecamatan', string='Kecamatan',
                                   ondelete='restrict')
    kabupaten_id = fields.Many2one('digital_kamtibmas.kabupaten', string='Kabupaten/Kota',
                                   related='kecamatan_id.kabupaten_id', store=True, readonly=True)
