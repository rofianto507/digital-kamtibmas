from odoo import models, fields


class TahananKategori(models.Model):
    _name        = 'digital_kamtibmas.tahanan.kategori'
    _description = 'Kategori Tahanan'
    _order       = 'name'

    name        = fields.Char('Nama Kategori', required=True)
    keterangan  = fields.Text('Keterangan')
    active      = fields.Boolean(default=True)

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'Nama kategori sudah terdaftar.',
    )
