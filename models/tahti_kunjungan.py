from odoo import models, fields, api


class TahtiKunjungan(models.Model):
    _name        = 'digital_kamtibmas.tahti_kunjungan'
    _description = 'Buku Tamu Tahti'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'waktu_masuk desc'
    _rec_name    = 'code'

    code         = fields.Char('No. Kunjungan', readonly=True, default='New', copy=False)

    tamu_id      = fields.Many2one('digital_kamtibmas.tahti_tamu', 'Tamu / Pengunjung',
                                    required=True, ondelete='restrict', tracking=True)
    tahanan_id   = fields.Many2one('digital_kamtibmas.tahanan', 'Tahanan yang Dikunjungi',
                                    required=True, ondelete='restrict', tracking=True,
                                    domain=[('state', '=', 'ditahan')])
    hubungan     = fields.Selection([
        ('keluarga',  'Keluarga'),
        ('pengacara', 'Pengacara / Kuasa Hukum'),
        ('teman',     'Teman / Kenalan'),
        ('lainnya',   'Lainnya'),
    ], string='Hubungan dengan Tahanan', required=True, default='keluarga')
    keperluan    = fields.Text('Keperluan / Tujuan Kunjungan')

    waktu_masuk  = fields.Datetime('Waktu Masuk', required=True, default=fields.Datetime.now, tracking=True)
    waktu_keluar = fields.Datetime('Waktu Keluar', tracking=True)
    petugas_id   = fields.Many2one('res.users', 'Petugas Jaga', default=lambda self: self.env.user)
    keterangan   = fields.Text('Keterangan')

    state        = fields.Selection([
        ('berlangsung', 'Berlangsung'),
        ('selesai',     'Selesai'),
    ], string='Status', default='berlangsung', required=True, tracking=True)

    # Related fields untuk tampilan list
    tamu_nik     = fields.Char(related='tamu_id.nik',  string='NIK Tamu',  store=True)
    tamu_no_hp   = fields.Char(related='tamu_id.no_hp', string='No. HP Tamu')

    # ── Workflow ──────────────────────────────────────────────────────────────

    def action_selesaikan(self):
        self.write({'state': 'selesai', 'waktu_keluar': fields.Datetime.now()})

    def action_buka_kembali(self):
        self.write({'state': 'berlangsung', 'waktu_keluar': False})

    # ── Auto-code ─────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'digital_kamtibmas.tahti_kunjungan') or 'New'
        return super().create(vals_list)
