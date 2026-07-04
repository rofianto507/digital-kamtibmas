from odoo import models, fields, api


class TahtiTamu(models.Model):
    _name        = 'digital_kamtibmas.tahti_tamu'
    _description = 'Data Tamu Tahti'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'nama'
    _rec_name    = 'nama'

    nama          = fields.Char('Nama Lengkap', required=True)
    nik           = fields.Char('NIK', size=16, required=True)
    no_hp         = fields.Char('No. HP / WA')
    alamat        = fields.Text('Alamat')
    foto_ktp      = fields.Image('Foto KTP', max_width=800, max_height=600)

    kunjungan_ids   = fields.One2many('digital_kamtibmas.tahti_kunjungan', 'tamu_id', string='Riwayat Kunjungan')
    kunjungan_count = fields.Integer('Jumlah Kunjungan', compute='_compute_kunjungan_count')

    _sql_constraints = [
        ('nik_uniq', 'unique(nik)', 'NIK sudah terdaftar. Pilih tamu dari data yang ada.'),
    ]

    @api.depends('kunjungan_ids')
    def _compute_kunjungan_count(self):
        for rec in self:
            rec.kunjungan_count = len(rec.kunjungan_ids)

    def name_get(self):
        return [(rec.id, f"[{rec.nik}] {rec.nama}") for rec in self]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            records = self.search(
                ['|', ('nama', operator, name), ('nik', operator, name)] + args,
                limit=limit,
            )
        else:
            records = self.search(args, limit=limit)
        return records.name_get()

    def action_view_kunjungan(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Riwayat Kunjungan',
            'res_model': 'digital_kamtibmas.tahti_kunjungan',
            'view_mode': 'list,form',
            'domain': [('tamu_id', '=', self.id)],
            'context': {'default_tamu_id': self.id},
        }
