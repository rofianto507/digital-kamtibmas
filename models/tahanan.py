from odoo import models, fields, api


class Tahanan(models.Model):
    _name        = 'digital_kamtibmas.tahanan'
    _description = 'Data Tahanan Tahti'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'id desc'
    _rec_name    = 'nama'

    code          = fields.Char('No. Tahanan', readonly=True, default='New', copy=False)

    # ── Identitas ─────────────────────────────────────────────────────────────
    nama          = fields.Char('Nama Lengkap', required=True, tracking=True)
    nik           = fields.Char('NIK', size=16)
    jenis_kelamin = fields.Selection([
        ('laki',      'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ], string='Jenis Kelamin', required=True, default='laki')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    alamat        = fields.Text('Alamat')
    foto          = fields.Image('Foto', max_width=512, max_height=512)

    kategori_id   = fields.Many2one('digital_kamtibmas.tahanan.kategori', 'Kategori', ondelete='set null', tracking=True)

    # ── Perkara ───────────────────────────────────────────────────────────────
    nomor_perkara = fields.Char('No. Perkara', tracking=True)
    jenis_perkara = fields.Selection([
        ('pencurian',    'Pencurian / Perampokan'),
        ('penipuan',     'Penipuan / Penggelapan'),
        ('penganiayaan', 'Penganiayaan / Kekerasan'),
        ('narkoba',      'Narkotika / Psikotropika'),
        ('korupsi',      'Korupsi'),
        ('cybercrime',   'Cyber Crime'),
        ('kesusilaan',   'Kesusilaan'),
        ('pembunuhan',   'Pembunuhan'),
        ('lainnya',      'Lainnya'),
    ], string='Jenis Perkara')
    pasal         = fields.Char('Pasal yang Disangkakan')
    penyidik_id   = fields.Many2one('res.users', 'Penyidik')

    # ── Penahanan ─────────────────────────────────────────────────────────────
    tanggal_masuk  = fields.Date('Tanggal Masuk', required=True, default=fields.Date.today, tracking=True)
    tanggal_keluar = fields.Date('Tanggal Keluar', tracking=True)
    sel_id         = fields.Many2one('digital_kamtibmas.tahti_sel', 'Sel / Kamar', ondelete='set null', tracking=True)
    keterangan     = fields.Text('Keterangan')
    state          = fields.Selection([
        ('ditahan', 'Ditahan'),
        ('bebas',   'Bebas'),
    ], string='Status', default='ditahan', required=True, tracking=True)

    kunjungan_count = fields.Integer('Jumlah Kunjungan', compute='_compute_kunjungan_count')

    @api.depends()
    def _compute_kunjungan_count(self):
        KUJ = self.env['digital_kamtibmas.tahti_kunjungan']
        for rec in self:
            rec.kunjungan_count = KUJ.search_count([('tahanan_id', '=', rec.id)])

    def action_view_kunjungan(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Riwayat Kunjungan',
            'res_model': 'digital_kamtibmas.tahti_kunjungan',
            'view_mode': 'list,form',
            'domain': [('tahanan_id', '=', self.id)],
            'context': {'default_tahanan_id': self.id},
        }

    # ── Workflow ──────────────────────────────────────────────────────────────

    def action_bebaskan(self):
        self.write({'state': 'bebas', 'tanggal_keluar': fields.Date.today()})

    def action_tahan_kembali(self):
        self.write({'state': 'ditahan', 'tanggal_keluar': False})

    # ── Auto-code ─────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'digital_kamtibmas.tahanan') or 'New'
        return super().create(vals_list)
