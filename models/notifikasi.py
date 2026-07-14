from odoo import models, fields


class Notifikasi(models.Model):
    _name        = 'digital_kamtibmas.notifikasi'
    _description = 'Notifikasi Mobile'
    _order       = 'created_at desc'

    user_id    = fields.Many2one('res.users', string='Pengguna', required=True,
                                  ondelete='cascade', index=True)
    judul      = fields.Char('Judul', required=True)
    isi        = fields.Text('Isi')
    tipe       = fields.Selection([
        ('antrian',    'Antrian'),
        ('rehab',      'Rehabilitasi'),
        ('konseling',  'Konseling'),
        ('eform_laka', 'E-Form Laka'),
        ('system',     'Sistem'),
    ], string='Tipe', default='system', required=True)
    is_read    = fields.Boolean('Sudah Dibaca', default=False, index=True)
    created_at = fields.Datetime('Waktu', default=fields.Datetime.now, readonly=True)
