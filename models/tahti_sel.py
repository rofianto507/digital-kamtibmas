from odoo import models, fields


class TahtiSel(models.Model):
    _name        = 'digital_kamtibmas.tahti_sel'
    _description = 'Sel / Kamar Tahanan'
    _order       = 'jenis, name'

    name       = fields.Char('Nama / Nomor Sel', required=True)
    jenis      = fields.Selection([
        ('pria',   'Pria'),
        ('wanita', 'Wanita'),
        ('anak',   'Anak-anak'),
    ], string='Jenis', required=True, default='pria')
    kapasitas  = fields.Integer('Kapasitas', default=1)
    keterangan = fields.Char('Keterangan')
