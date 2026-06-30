from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Antrian(models.Model):
    _name        = 'digital_kamtibmas.antrian'
    _description = 'Antrian Layanan Satlantas'
    _order       = 'tanggal_booking desc, nomor_urut asc'
    _rec_name    = 'nomor_antrian'

    nomor_antrian   = fields.Char('Nomor Antrian', readonly=True, default='New', copy=False)
    nomor_urut      = fields.Integer('Nomor Urut', readonly=True)
    user_id         = fields.Many2one('res.users', string='Pendaftar', required=True,
                                       default=lambda self: self.env.user)
    atas_nama       = fields.Char('Atas Nama', required=True,
                                   help='Nama penerima layanan (boleh berbeda dengan pendaftar)')
    tanggal_booking = fields.Date('Tanggal Booking', required=True, default=fields.Date.today)
    loket_id        = fields.Many2one('digital_kamtibmas.loket', string='Loket',
                                       required=True, ondelete='restrict')
    layanan_id      = fields.Many2one('digital_kamtibmas.jenis_layanan', string='Jenis Layanan',
                                       related='loket_id.layanan_id', store=True, readonly=True)
    state           = fields.Selection([
        ('menunggu',   'Menunggu'),
        ('konfirmasi', 'Dikonfirmasi'),
        ('dipanggil',  'Dipanggil'),
        ('selesai',    'Selesai'),
        ('batal',      'Batal'),
    ], string='Status', default='menunggu', required=True, tracking=True)

    catatan = fields.Text('Catatan')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('nomor_antrian', 'New') == 'New':
                loket = self.env['digital_kamtibmas.loket'].browse(vals['loket_id'])
                tanggal = vals.get('tanggal_booking') or fields.Date.today()

                # Nomor urut per layanan per hari (reset tiap hari)
                urut = self.search_count([
                    ('layanan_id', '=', loket.layanan_id.id),
                    ('tanggal_booking', '=', tanggal),
                ]) + 1

                code = (loket.layanan_id.code or 'ANT').upper().replace(' ', '')
                vals['nomor_urut']    = urut
                vals['nomor_antrian'] = f"{code}-{urut:03d}"
        return super().create(vals_list)

    def action_konfirmasi(self):
        for rec in self:
            # Validasi kuota saat konfirmasi — hanya antrian yang sudah dikonfirmasi/aktif
            terpakai = self.search_count([
                ('loket_id', '=', rec.loket_id.id),
                ('tanggal_booking', '=', rec.tanggal_booking),
                ('state', 'in', ('konfirmasi', 'dipanggil', 'selesai')),
            ])
            if terpakai >= rec.loket_id.kuota:
                raise ValidationError(
                    f'Kuota antrian loket "{rec.loket_id.name}" untuk tanggal '
                    f'{rec.tanggal_booking} sudah penuh ({rec.loket_id.kuota} antrian).'
                )
            rec.state = 'konfirmasi'

    def action_panggil(self):
        self.state = 'dipanggil'

    def action_selesai(self):
        self.state = 'selesai'

    def action_batal(self):
        self.state = 'batal'

    def action_reset(self):
        self.state = 'menunggu'

    @api.constrains('loket_id')
    def _check_loket_aktif(self):
        for rec in self:
            if rec.loket_id.state == 'nonaktif':
                raise ValidationError(
                    f'Loket "{rec.loket_id.name}" sedang tidak aktif.'
                )
