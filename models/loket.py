from odoo import models, fields, api


HARI_SELECTION = [
    ('0', 'Senin'),
    ('1', 'Selasa'),
    ('2', 'Rabu'),
    ('3', 'Kamis'),
    ('4', 'Jumat'),
    ('5', 'Sabtu'),
    ('6', 'Minggu'),
]


class Loket(models.Model):
    _name        = 'digital_kamtibmas.loket'
    _description = 'Loket Layanan Satlantas'
    _order       = 'name asc'
    _rec_name    = 'name'

    name       = fields.Char('Nama Loket', required=True)
    layanan_id = fields.Many2one('digital_kamtibmas.jenis_layanan', string='Jenis Layanan',
                                  required=True, ondelete='restrict')
    kuota      = fields.Integer('Kuota Antrian/Hari', default=50, required=True)
    state      = fields.Selection([
        ('aktif',    'Aktif'),
        ('nonaktif', 'Non Aktif'),
    ], string='Status', default='aktif', required=True)

    jadwal_ids    = fields.One2many('digital_kamtibmas.loket_jadwal', 'loket_id',
                                     string='Jadwal Operasional')
    antrian_ids   = fields.One2many('digital_kamtibmas.antrian', 'loket_id',
                                     string='Antrian')
    antrian_count = fields.Integer('Total Antrian Hari Ini',
                                    compute='_compute_antrian_count',
                                    compute_sudo=True)

    @api.depends('antrian_ids.tanggal_booking', 'antrian_ids.state')
    def _compute_antrian_count(self):
        today = fields.Date.today()
        Antrian = self.env['digital_kamtibmas.antrian'].sudo()
        for rec in self:
            rec.antrian_count = Antrian.search_count([
                ('loket_id', '=', rec.id),
                ('tanggal_booking', '=', today),
                ('state', 'in', ('konfirmasi', 'dipanggil', 'selesai')),
            ])

    def action_view_antrian_hari_ini(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f'Antrian Hari Ini — {self.name}',
            'res_model': 'digital_kamtibmas.antrian',
            'view_mode': 'list,form',
            'domain': [
                ('loket_id', '=', self.id),
                ('tanggal_booking', '=', fields.Date.today()),
            ],
            'context': {'default_loket_id': self.id},
        }

    def action_aktif(self):
        self.state = 'aktif'

    def action_nonaktif(self):
        self.state = 'nonaktif'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if not rec.jadwal_ids:
                self.env['digital_kamtibmas.loket_jadwal'].create([
                    {'loket_id': rec.id, 'hari': str(i), 'libur': i >= 5}
                    for i in range(7)
                ])
        return records


class LoketJadwal(models.Model):
    _name        = 'digital_kamtibmas.loket_jadwal'
    _description = 'Jadwal Operasional Loket'
    _order       = 'hari asc'
    _rec_name    = 'hari'

    loket_id  = fields.Many2one('digital_kamtibmas.loket', required=True, ondelete='cascade')
    hari      = fields.Selection(HARI_SELECTION, string='Hari', required=True)
    libur     = fields.Boolean('Libur', default=False)
    jam_buka  = fields.Float('Jam Buka',  digits=(2, 2),
                              help='Format desimal: 8.0 = 08:00, 8.5 = 08:30')
    jam_tutup = fields.Float('Jam Tutup', digits=(2, 2))

    _sql_constraints = [
        ('loket_hari_uniq', 'unique(loket_id, hari)', 'Setiap hari hanya boleh satu jadwal per loket.'),
    ]

    @api.onchange('libur')
    def _onchange_libur(self):
        if self.libur:
            self.jam_buka  = 0.0
            self.jam_tutup = 0.0
