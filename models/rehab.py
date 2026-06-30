from odoo import models, fields, api


class Rehab(models.Model):
    _name        = 'digital_kamtibmas.rehab'
    _description = 'Permohonan Rehabilitasi Narkoba'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'id desc'
    _rec_name    = 'code'

    code               = fields.Char('No. Permohonan', readonly=True, default='New', copy=False, tracking=True)
    user_id            = fields.Many2one('res.users', 'Akun Pengguna', ondelete='set null',
                                         help='Akun login pengguna dari aplikasi mobile')

    # ── Identitas Pemohon ──────────────────────────────────────────────────────
    nama               = fields.Char('Nama Lengkap', required=True, tracking=True)
    nik                = fields.Char('NIK', size=16)
    no_hp              = fields.Char('No. HP / WA')
    jenis_kelamin      = fields.Selection([
        ('laki',     'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ], string='Jenis Kelamin')
    tempat_lahir       = fields.Char('Tempat Lahir')
    tanggal_lahir      = fields.Date('Tanggal Lahir')
    alamat             = fields.Text('Alamat Lengkap')
    foto_pemohon       = fields.Image('Foto Pemohon', max_width=512, max_height=512)

    # ── Informasi Penggunaan ───────────────────────────────────────────────────
    jenis_narkoba      = fields.Char('Jenis Narkoba / Zat')
    lama_penggunaan    = fields.Char('Lama Penggunaan', help='Contoh: 2 tahun, 6 bulan')
    keterangan         = fields.Text('Keterangan / Alasan Permohonan')

    # ── Jadwal & Status ────────────────────────────────────────────────────────
    tanggal_pengajuan  = fields.Date('Tanggal Pengajuan', default=fields.Date.today)
    tanggal_jadwal     = fields.Datetime('Tanggal Jadwal Rehab', tracking=True)
    state              = fields.Selection([
        ('menunggu',   'Menunggu'),
        ('konfirmasi', 'Dikonfirmasi'),
        ('proses',     'Sedang Diproses'),
        ('selesai',    'Selesai'),
    ], string='Status', default='menunggu', required=True, tracking=True)

    # ── Workflow ──────────────────────────────────────────────────────────────

    def action_konfirmasi(self):
        self.state = 'konfirmasi'

    def action_proses(self):
        self.state = 'proses'

    def action_selesai(self):
        self.state = 'selesai'

    def action_reset(self):
        self.state = 'menunggu'

    # ── Auto-code ─────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'digital_kamtibmas.rehab') or 'New'
        return super().create(vals_list)
