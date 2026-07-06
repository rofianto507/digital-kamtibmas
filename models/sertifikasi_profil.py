from odoo import models, fields, api


class SertifikasiProfil(models.Model):
    _name = 'digital_kamtibmas.sertifikasi.profil'
    _description = 'Profil Peserta Sertifikasi'
    _order = 'nama'
    _rec_name = 'nama'

    nik = fields.Char('NIK', required=True, index=True)
    nama = fields.Char('Nama Lengkap', required=True)
    tempat_lahir = fields.Char('Tempat Lahir')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    jenis_kelamin = fields.Selection([
        ('laki',      'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ], 'Jenis Kelamin')
    no_hp = fields.Char('No. HP')
    alamat = fields.Text('Alamat')

    partner_id = fields.Many2one(
        'res.partner', 'Kontak Terhubung', ondelete='set null')

    peserta_ids = fields.One2many(
        'digital_kamtibmas.sertifikasi.peserta', 'profil_id', 'Riwayat Sertifikasi')
    total_sertifikasi = fields.Integer(
        'Total Sertifikasi', compute='_compute_stats', store=True)
    total_lulus = fields.Integer(
        'Total Lulus', compute='_compute_stats', store=True)

    _sql_constraints = [
        ('nik_unique', 'UNIQUE(nik)', 'NIK sudah terdaftar di sistem.'),
    ]

    @api.depends('peserta_ids', 'peserta_ids.state', 'peserta_ids.lulus')
    def _compute_stats(self):
        for rec in self:
            selesai = rec.peserta_ids.filtered(lambda p: p.state == 'selesai')
            rec.total_sertifikasi = len(selesai)
            rec.total_lulus = len(selesai.filtered('lulus'))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if not rec.partner_id:
                partner = self.env['res.partner'].sudo().create({
                    'name': rec.nama,
                    'ref': rec.nik,
                    'phone': rec.no_hp or False,
                    'comment': f'NIK: {rec.nik}',
                })
                rec.partner_id = partner.id
        return records

    def action_buka_partner(self):
        self.ensure_one()
        if not self.partner_id:
            partner = self.env['res.partner'].sudo().create({
                'name': self.nama,
                'ref': self.nik,
                'phone': self.no_hp or False,
                'comment': f'NIK: {self.nik}',
            })
            self.partner_id = partner.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'new',
        }
