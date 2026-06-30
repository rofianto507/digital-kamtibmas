from odoo import models, fields, api


class JenisLayanan(models.Model):
    _name        = 'digital_kamtibmas.jenis_layanan'
    _description = 'Jenis Layanan Satlantas'
    _order       = 'name asc'
    _rec_name    = 'name'

    name   = fields.Char('Nama Layanan', required=True)
    code   = fields.Char('Kode', required=True, size=10,
                          help='Prefix nomor antrian, contoh: SIMA, SIMC, STNK')
    active = fields.Boolean('Aktif', default=True)

    loket_ids   = fields.One2many('digital_kamtibmas.loket', 'layanan_id', string='Loket')
    loket_count = fields.Integer('Jumlah Loket', compute='_compute_loket_count', store=True)

    @api.depends('loket_ids')
    def _compute_loket_count(self):
        for rec in self:
            rec.loket_count = len(rec.loket_ids)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Kode jenis layanan harus unik.'),
    ]
