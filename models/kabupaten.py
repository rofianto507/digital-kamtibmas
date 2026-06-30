from odoo import models, fields, api


class Kabupaten(models.Model):
    _name        = 'digital_kamtibmas.kabupaten'
    _description = 'Kabupaten/Kota — Wilayah Palembang'
    _order       = 'name asc'
    _rec_name    = 'name'

    name     = fields.Char('Nama', required=True)
    code     = fields.Char('Kode')
    type     = fields.Selection([
        ('KABUPATEN', 'Kabupaten'),
        ('KOTA', 'Kota'),
    ], string='Tipe')
    geometry = fields.Text('GeoJSON Geometry')

    kecamatan_ids   = fields.One2many('digital_kamtibmas.kecamatan', 'kabupaten_id', string='Kecamatan')
    kecamatan_count = fields.Integer('Total Kecamatan', compute='_compute_kecamatan_count', store=True)

    @api.depends('kecamatan_ids')
    def _compute_kecamatan_count(self):
        for rec in self:
            rec.kecamatan_count = len(rec.kecamatan_ids)
