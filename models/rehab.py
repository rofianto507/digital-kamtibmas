from datetime import date
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
    jenis_kelamin      = fields.Selection([
        ('laki',      'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ], string='Jenis Kelamin')
    tempat_lahir       = fields.Char('Tempat Lahir')
    tanggal_lahir      = fields.Date('Tanggal Lahir')
    umur               = fields.Integer('Umur', compute='_compute_umur', store=False)
    alamat             = fields.Text('Alamat Lengkap')
    foto_pemohon       = fields.Image('Foto Pemohon', max_width=512, max_height=512)

    # ── Rehabilitasi ───────────────────────────────────────────────────────────
    tempat_rehab_id    = fields.Many2one(
        'digital_kamtibmas.rehab.tempat', 'Tempat Rehabilitasi',
        ondelete='set null', tracking=True)
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

    @api.depends('tanggal_lahir')
    def _compute_umur(self):
        today = date.today()
        for rec in self:
            if rec.tanggal_lahir:
                tl = rec.tanggal_lahir
                rec.umur = today.year - tl.year - (
                    (today.month, today.day) < (tl.month, tl.day))
            else:
                rec.umur = 0

    # ── Workflow ──────────────────────────────────────────────────────────────

    def action_konfirmasi(self):
        self.state = 'konfirmasi'

    def action_proses(self):
        self.state = 'proses'

    def action_selesai(self):
        self.state = 'selesai'

    def action_reset(self):
        self.state = 'menunggu'

    def write(self, vals):
        new_state = vals.get('state')
        res = super().write(vals)
        if new_state:
            _msgs = {
                'konfirmasi': ('Rehab Dikonfirmasi',
                               lambda r: f'Permohonan rehabilitasi {r.code} atas nama {r.nama} telah dikonfirmasi.'),
                'proses':     ('Rehab Sedang Diproses',
                               lambda r: f'Permohonan rehabilitasi {r.code} sedang dalam proses penanganan.'),
                'selesai':    ('Rehab Selesai',
                               lambda r: f'Permohonan rehabilitasi {r.code} telah selesai. Terima kasih.'),
            }
            if new_state in _msgs:
                judul, isi_fn = _msgs[new_state]
                Notif = self.env['digital_kamtibmas.notifikasi'].sudo()
                for rec in self:
                    if rec.user_id:
                        Notif.create({
                            'user_id': rec.user_id.id,
                            'judul': judul,
                            'isi': isi_fn(rec),
                            'tipe': 'rehab',
                        })
        return res

    # ── Auto-code ─────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'digital_kamtibmas.rehab') or 'New'
        return super().create(vals_list)
