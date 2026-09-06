from odoo import models, fields


class Slider(models.Model):
    _name = 'digital.kamtibmas.slider'
    _description = 'Slider Mobile'
    _order = 'sequence asc, id asc'

    name = fields.Char('Judul', required=True)
    image = fields.Binary('Gambar', required=True, attachment=True)
    image_filename = fields.Char('Nama File')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)
