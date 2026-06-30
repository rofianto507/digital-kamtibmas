from odoo import models, fields, api


class Kecamatan(models.Model):
    _name        = 'digital_kamtibmas.kecamatan'
    _description = 'Kecamatan — Wilayah Palembang'
    _order       = 'name asc'
    _rec_name    = 'name'

    name         = fields.Char('Nama', required=True)
    code         = fields.Char('Kode')
    kabupaten_id = fields.Many2one('digital_kamtibmas.kabupaten', string='Kabupaten/Kota',
                                   ondelete='restrict')
    geometry     = fields.Text('GeoJSON Geometry')

    desa_ids   = fields.One2many('digital_kamtibmas.desa', 'kecamatan_id', string='Desa/Kelurahan')
    desa_count = fields.Integer('Total Desa/Kel.', compute='_compute_desa_count', store=True)

    @api.depends('desa_ids')
    def _compute_desa_count(self):
        for rec in self:
            rec.desa_count = len(rec.desa_ids)
