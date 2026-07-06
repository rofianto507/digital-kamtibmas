from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SertifikasiSoal(models.Model):
    _name = 'digital_kamtibmas.sertifikasi.soal'
    _description = 'Soal Sertifikasi Narkoba'
    _order = 'sequence, id'

    name = fields.Text(string='Teks Soal', required=True)
    sequence = fields.Integer(string='Urutan', default=10)
    kategori = fields.Selection([
        ('umum',       'Umum'),
        ('hukum',      'Hukum & Regulasi'),
        ('kesehatan',  'Kesehatan'),
        ('pencegahan', 'Pencegahan & Rehabilitasi'),
    ], string='Kategori', required=True, default='umum')
    tingkat_kesulitan = fields.Selection([
        ('mudah',  'Mudah'),
        ('sedang', 'Sedang'),
        ('sulit',  'Sulit'),
    ], string='Tingkat Kesulitan', required=True, default='mudah')
    active = fields.Boolean(default=True)
    pilihan_ids = fields.One2many(
        'digital_kamtibmas.sertifikasi.pilihan', 'soal_id',
        string='Pilihan Jawaban')
    jumlah_pilihan = fields.Integer(
        string='Jml. Pilihan', compute='_compute_jumlah', store=True)
    has_kunci = fields.Boolean(
        string='Ada Kunci', compute='_compute_jumlah', store=True)

    @api.depends('pilihan_ids', 'pilihan_ids.is_correct')
    def _compute_jumlah(self):
        for rec in self:
            rec.jumlah_pilihan = len(rec.pilihan_ids)
            rec.has_kunci = any(p.is_correct for p in rec.pilihan_ids)

    @api.constrains('pilihan_ids')
    def _check_kunci_jawaban(self):
        for rec in self:
            if rec.pilihan_ids and not any(p.is_correct for p in rec.pilihan_ids):
                raise ValidationError(
                    f'Soal "{rec.name[:60]}..." harus memiliki minimal satu kunci jawaban yang benar.')
            correct_count = sum(1 for p in rec.pilihan_ids if p.is_correct)
            if correct_count > 1:
                raise ValidationError(
                    f'Soal "{rec.name[:60]}..." hanya boleh memiliki satu kunci jawaban yang benar.')


class SertifikasiPilihan(models.Model):
    _name = 'digital_kamtibmas.sertifikasi.pilihan'
    _description = 'Pilihan Jawaban Soal Sertifikasi'
    _order = 'sequence, id'

    soal_id = fields.Many2one(
        'digital_kamtibmas.sertifikasi.soal',
        string='Soal', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Urutan', default=10)
    name = fields.Char(string='Teks Pilihan', required=True)
    is_correct = fields.Boolean(string='Kunci Jawaban')
