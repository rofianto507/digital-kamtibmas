from odoo import models, fields


class SertifikasiPeserta(models.Model):
    _name = 'digital_kamtibmas.sertifikasi.peserta'
    _description = 'Peserta Sertifikasi Narkoba'
    _order = 'waktu_mulai desc'

    sertifikasi_id = fields.Many2one(
        'digital_kamtibmas.sertifikasi', 'Sertifikasi',
        required=True, ondelete='cascade', index=True)
    profil_id = fields.Many2one(
        'digital_kamtibmas.sertifikasi.profil', 'Peserta',
        required=True, ondelete='restrict', index=True)

    # Denormalized dari profil — disimpan agar bisa di-filter/search tanpa join
    nik           = fields.Char(related='profil_id.nik',           store=True, index=True)
    nama          = fields.Char(related='profil_id.nama',          store=True)
    jenis_kelamin = fields.Selection(related='profil_id.jenis_kelamin', store=True)

    # Data spesifik sesi ujian
    waktu_mulai   = fields.Datetime('Waktu Mulai')
    waktu_selesai = fields.Datetime('Waktu Selesai')
    total_benar   = fields.Integer('Jawaban Benar')
    total_soal    = fields.Integer('Total Soal')
    nilai         = fields.Float('Nilai', digits=(5, 1))
    lulus         = fields.Boolean('Lulus')
    state         = fields.Selection([
        ('mengerjakan', 'Mengerjakan'),
        ('selesai',     'Selesai'),
    ], string='Status', default='mengerjakan')
    jawaban_ids   = fields.One2many(
        'digital_kamtibmas.sertifikasi.jawaban', 'peserta_id', 'Detail Jawaban')

    def action_cetak_sertifikat(self):
        self.ensure_one()
        return self.env.ref('digital_kamtibmas.action_report_sertifikat').with_context(landscape=True).report_action(self)


class SertifikasiJawaban(models.Model):
    _name = 'digital_kamtibmas.sertifikasi.jawaban'
    _description = 'Jawaban Peserta Sertifikasi'

    peserta_id = fields.Many2one(
        'digital_kamtibmas.sertifikasi.peserta',
        required=True, ondelete='cascade', index=True)
    soal_id    = fields.Many2one('digital_kamtibmas.sertifikasi.soal',    'Soal')
    pilihan_id = fields.Many2one('digital_kamtibmas.sertifikasi.pilihan', 'Pilihan Dipilih')
    is_correct = fields.Boolean('Benar')
