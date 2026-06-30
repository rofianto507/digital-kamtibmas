from odoo import models, fields


class Desa(models.Model):
    _name        = 'digital_kamtibmas.desa'
    _description = 'Desa/Kelurahan — Wilayah Palembang'
    _order       = 'name asc'
    _rec_name    = 'name'

    name         = fields.Char('Nama', required=True)
    code         = fields.Char('Kode')
    type         = fields.Selection([
        ('DESA',       'Desa'),
        ('KELURAHAN',  'Kelurahan'),
    ], string='Tipe')
    kecamatan_id = fields.Many2one('digital_kamtibmas.kecamatan', string='Kecamatan',
                                   ondelete='restrict')
    kabupaten_id = fields.Many2one('digital_kamtibmas.kabupaten', string='Kabupaten/Kota',
                                   related='kecamatan_id.kabupaten_id', store=True, readonly=True)
    geometry     = fields.Text('GeoJSON Geometry')
