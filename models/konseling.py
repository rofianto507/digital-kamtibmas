from markupsafe import Markup
from odoo import models, fields, api
from odoo.exceptions import UserError


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
    # ── Detail Permohonan ─────────────────────────────────────────────────────
    keterangan         = fields.Text('Keterangan / Uraian Permasalahan')

    # ── Jadwal, Konselor & Status ─────────────────────────────────────────────
    tanggal_pengajuan  = fields.Date('Tanggal Pengajuan', default=fields.Date.today)
    tanggal_jadwal     = fields.Datetime('Tanggal Jadwal Konseling', tracking=True)
    konselor_id        = fields.Many2one('res.users', 'Konselor / Petugas', tracking=True)
    hasil_konseling    = fields.Text('Hasil Konseling / Rekomendasi')
    channel_id         = fields.Many2one('discuss.channel', 'Saluran Konsultasi',
                                         readonly=True, ondelete='set null')
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
        if not self.konselor_id:
            raise UserError('Konselor harus diisi sebelum memulai proses konseling.')
        self.state = 'proses'
        if self.user_id and self.konselor_id and not self.channel_id:
            partner_ids = [self.user_id.partner_id.id, self.konselor_id.partner_id.id]
            channel = self.env['discuss.channel'].sudo().create({
                'name': f'Konseling {self.code} – {self.nama}',
                'channel_type': 'group',
                'description': f'Sesi konseling untuk {self.nama}. Konselor: {self.konselor_id.name}.',
                'channel_member_ids': [(0, 0, {'partner_id': pid}) for pid in partner_ids],
            })
            channel.sudo().message_post(
                body=Markup(
                    'Sesi konseling <b>{code}</b> untuk <b>{nama}</b> telah dimulai.<br/>'
                    'Konselor yang ditugaskan: <b>{konselor}</b>.<br/>'
                    'Silakan mulai sesi konsultasi di sini.'
                ).format(
                    code=self.code,
                    nama=self.nama,
                    konselor=self.konselor_id.name,
                ),
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
            )
            self.channel_id = channel.id

    def action_selesai(self):
        self.state = 'selesai'

    def action_reset(self):
        self.state = 'menunggu'

    def action_open_channel(self):
        self.ensure_one()
        if not self.channel_id:
            return False
        return {
            'type': 'ir.actions.act_url',
            'url': f'/odoo/discuss?active_id=discuss.channel_{self.channel_id.id}',
            'target': 'self',
        }

    def write(self, vals):
        new_state = vals.get('state')
        if new_state == 'proses':
            for rec in self:
                if not rec.konselor_id and not vals.get('konselor_id'):
                    raise UserError(f'Konselor harus diisi sebelum memulai proses konseling ({rec.code}).')
        res = super().write(vals)
        if new_state:
            _msgs = {
                'konfirmasi': ('Konseling Dikonfirmasi',
                               lambda r: f'Permohonan konseling {r.code} atas nama {r.nama} telah dikonfirmasi.'),
                'proses':     ('Sesi Konseling Dimulai',
                               lambda r: f'Sesi konseling {r.code} telah dimulai. Silakan buka fitur chat untuk berkonsultasi.'),
                'selesai':    ('Konseling Selesai',
                               lambda r: f'Sesi konseling {r.code} telah selesai. Terima kasih.'),
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
                            'tipe': 'konseling',
                        })
            if new_state == 'proses':
                for rec in self:
                    if rec.user_id and rec.konselor_id and not rec.channel_id:
                        partner_ids = [rec.user_id.partner_id.id, rec.konselor_id.partner_id.id]
                        channel = self.env['discuss.channel'].sudo().create({
                            'name': f'Konseling {rec.code} – {rec.nama}',
                            'channel_type': 'group',
                            'description': f'Sesi konseling untuk {rec.nama}. Konselor: {rec.konselor_id.name}.',
                            'channel_member_ids': [(0, 0, {'partner_id': pid}) for pid in partner_ids],
                        })
                        channel.sudo().message_post(
                            body=Markup(
                                'Sesi konseling <b>{code}</b> untuk <b>{nama}</b> telah dimulai.<br/>'
                                'Konselor yang ditugaskan: <b>{konselor}</b>.<br/>'
                                'Silakan mulai sesi konsultasi di sini.'
                            ).format(
                                code=rec.code,
                                nama=rec.nama,
                                konselor=rec.konselor_id.name,
                            ),
                            message_type='comment',
                            subtype_xmlid='mail.mt_comment',
                        )
                        rec.channel_id = channel.id
        return res

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
