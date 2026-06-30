from odoo import models, fields, api


class Konseling(models.Model):
    _name        = 'digital_kamtibmas.konseling'
    _description = 'Konseling Online Satnarkoba'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'id desc'
    _rec_name    = 'code'

    code               = fields.Char('No. Konseling', readonly=True, default='New', copy=False, tracking=True)
    user_id            = fields.Many2one('res.users', 'Akun Pengguna', ondelete='set null',
                                         help='Akun login pengguna dari aplikasi mobile')

    # ── Identitas Pemohon ──────────────────────────────────────────────────────
    nama               = fields.Char('Nama Lengkap', required=True, tracking=True)
    nik                = fields.Char('NIK', size=16)
    no_hp              = fields.Char('No. HP / WA')
    jenis_kelamin      = fields.Selection([
        ('laki',      'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ], string='Jenis Kelamin')
    tempat_lahir       = fields.Char('Tempat Lahir')
    tanggal_lahir      = fields.Date('Tanggal Lahir')
    alamat             = fields.Text('Alamat Lengkap')
    foto_pemohon       = fields.Image('Foto Pemohon', max_width=512, max_height=512)

    # ── Detail Permohonan ─────────────────────────────────────────────────────
    jenis_masalah      = fields.Selection([
        ('penyalahgunaan', 'Penyalahgunaan Narkoba'),
        ('ketergantungan', 'Ketergantungan Narkoba'),
        ('pencegahan',     'Pencegahan / Penyuluhan'),
        ('pasca_rehab',    'Pasca Rehabilitasi'),
        ('konsultasi',     'Konsultasi Keluarga Korban'),
        ('lainnya',        'Lainnya'),
    ], string='Jenis Permasalahan')
    sumber_rujukan     = fields.Selection([
        ('mandiri',  'Mandiri / Inisiatif Sendiri'),
        ('keluarga', 'Keluarga'),
        ('sekolah',  'Sekolah / Kampus'),
        ('instansi', 'Instansi / Lembaga'),
        ('lainnya',  'Lainnya'),
    ], string='Sumber Rujukan')
    keterangan         = fields.Text('Keterangan / Uraian Permasalahan')

    # ── Jadwal & Status ────────────────────────────────────────────────────────
    tanggal_pengajuan  = fields.Date('Tanggal Pengajuan', default=fields.Date.today)
    tanggal_jadwal     = fields.Datetime('Tanggal Jadwal Konseling', tracking=True)
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
                    'digital_kamtibmas.konseling') or 'New'
        return super().create(vals_list)

    def name_get(self):
        return [(rec.id, f"[{rec.code}] {rec.nama}") for rec in self]
