import uuid
from odoo import models, fields, api
from odoo.exceptions import UserError


class Sertifikasi(models.Model):
    _name = 'digital_kamtibmas.sertifikasi'
    _description = 'Sertifikasi Narkoba'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char('Nama Sertifikasi', required=True)
    jumlah_soal = fields.Integer('Jumlah Soal', default=20, required=True, tracking=True)
    waktu_menit = fields.Integer('Waktu Pengerjaan (Menit)', default=30, required=True, tracking=True)
    nilai_kelulusan = fields.Integer('Nilai Kelulusan (%)', default=70, required=True, tracking=True)
    tanggal_aktif = fields.Date('Tanggal Mulai', tracking=True)
    tanggal_expired = fields.Date('Tanggal Berakhir', tracking=True)
    state = fields.Selection([
        ('draft',    'Draft'),
        ('aktif',    'Aktif'),
        ('nonaktif', 'Nonaktif'),
    ], string='Status', default='draft', required=True, tracking=True)
    access_token = fields.Char('Token Akses', copy=False, readonly=True, index=True)
    url_public = fields.Char('Link Publik', compute='_compute_url', store=True)
    notes = fields.Text('Catatan')

    peserta_ids = fields.One2many(
        'digital_kamtibmas.sertifikasi.peserta', 'sertifikasi_id', 'Peserta')
    total_peserta = fields.Integer('Total Peserta', compute='_compute_stats', store=True)
    total_lulus   = fields.Integer('Lulus',         compute='_compute_stats', store=True)

    @api.depends('peserta_ids', 'peserta_ids.state', 'peserta_ids.lulus')
    def _compute_stats(self):
        for rec in self:
            selesai = rec.peserta_ids.filtered(lambda p: p.state == 'selesai')
            rec.total_peserta = len(selesai)
            rec.total_lulus   = len(selesai.filtered('lulus'))

    @api.depends('access_token')
    def _compute_url(self):
        base = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        for rec in self:
            rec.url_public = f'{base}/sertifikasi/{rec.access_token}' if rec.access_token else ''

    # ── Actions ──────────────────────────────────────────────────────────────

    def action_aktifkan(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError('Hanya sertifikasi berstatus Draft yang dapat diaktifkan.')
            if not rec.access_token:
                rec.access_token = uuid.uuid4().hex
            rec.state = 'aktif'

    def action_nonaktifkan(self):
        self.write({'state': 'nonaktif'})

    def action_reset_draft(self):
        for rec in self:
            if rec.state == 'nonaktif':
                rec.state = 'draft'

    def action_buka_link(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.url_public,
            'target': 'new',
        }

    def action_view_peserta(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Peserta — ' + self.name,
            'res_model': 'digital_kamtibmas.sertifikasi.peserta',
            'domain': [('sertifikasi_id', '=', self.id)],
            'view_mode': 'list,form',
            'context': {'default_sertifikasi_id': self.id},
        }

    def action_view_lulus(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Peserta Lulus — ' + self.name,
            'res_model': 'digital_kamtibmas.sertifikasi.peserta',
            'domain': [('sertifikasi_id', '=', self.id), ('lulus', '=', True)],
            'view_mode': 'list,form',
        }
