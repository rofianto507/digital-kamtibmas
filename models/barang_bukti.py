from odoo import models, fields, api


class BarangBukti(models.Model):
    _name        = 'digital_kamtibmas.barang_bukti'
    _description = 'Barang Bukti Online Curanmor'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'id desc'
    _rec_name    = 'code'

    code               = fields.Char('No. Barang Bukti', readonly=True, default='New', copy=False, tracking=True)

    # ── Informasi Perkara ─────────────────────────────────────────────────────
    nomor_perkara      = fields.Char('No. LP / Perkara', tracking=True)
    lokasi_kejadian    = fields.Char('TKP / Lokasi Kejadian')
    tanggal_penyitaan  = fields.Date('Tanggal Penyitaan')
    tanggal_penerimaan = fields.Date('Tanggal Diterima', default=fields.Date.today)
    petugas_id         = fields.Many2one('res.users', 'Penyidik / Petugas', tracking=True)

    # ── Identitas Kendaraan ───────────────────────────────────────────────────
    jenis_kendaraan    = fields.Selection([
        ('roda_dua',   'Sepeda Motor (Roda Dua)'),
        ('roda_empat', 'Kendaraan Roda Empat'),
        ('roda_tiga',  'Kendaraan Roda Tiga'),
        ('lainnya',    'Lainnya'),
    ], string='Jenis Kendaraan', required=True, tracking=True)
    merek              = fields.Char('Merek', help='Contoh: Honda, Yamaha, Toyota, Suzuki')
    tipe               = fields.Char('Tipe / Model', help='Contoh: Beat, Vario, Avanza, Xenia')
    warna              = fields.Char('Warna Kendaraan')
    tahun_kendaraan    = fields.Integer('Tahun Kendaraan')
    nomor_polisi       = fields.Char('Nomor Polisi (NOPOL)', tracking=True)
    nomor_rangka       = fields.Char('Nomor Rangka', tracking=True)
    nomor_mesin        = fields.Char('Nomor Mesin', tracking=True)

    # ── Data Kepemilikan (STNK / BPKB) ───────────────────────────────────────
    nama_pemilik_stnk  = fields.Char('Nama Pemilik (STNK/BPKB)')
    alamat_stnk        = fields.Text('Alamat Pemilik (STNK/BPKB)')

    # ── Identitas Pelapor ─────────────────────────────────────────────────────
    nama_pelapor       = fields.Char('Nama Pelapor', required=True)
    nik_pelapor        = fields.Char('NIK Pelapor', size=16)
    no_hp_pelapor      = fields.Char('No. HP / WA Pelapor')
    alamat_pelapor     = fields.Text('Alamat Pelapor')

    # ── Barang Bukti Pendukung ────────────────────────────────────────────────
    item_ids           = fields.One2many(
        'digital_kamtibmas.barang_bukti_item', 'barang_bukti_id',
        string='Barang Bukti Pendukung')

    # ── Penyimpanan & Catatan ─────────────────────────────────────────────────
    lokasi_penyimpanan = fields.Char('Lokasi Penyimpanan', help='Nomor rak / ruangan / halaman')
    keterangan         = fields.Text('Keterangan / Catatan')

    # ── Status ────────────────────────────────────────────────────────────────
    state              = fields.Selection([
        ('diterima',     'Diterima'),
        ('disimpan',     'Disimpan'),
        ('diproses',     'Diproses'),
        ('dikembalikan', 'Dikembalikan'),
        ('dimusnahkan',  'Dimusnahkan'),
    ], string='Status', default='diterima', required=True, tracking=True)

    # ── Workflow ──────────────────────────────────────────────────────────────

    def action_simpan(self):
        self.state = 'disimpan'

    def action_proses(self):
        self.state = 'diproses'

    def action_kembalikan(self):
        self.state = 'dikembalikan'

    def action_musnahkan(self):
        self.state = 'dimusnahkan'

    def action_proses_ulang(self):
        self.state = 'diproses'

    def action_reset(self):
        self.state = 'diterima'

    # ── Auto-code ─────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'digital_kamtibmas.barang_bukti') or 'New'
        return super().create(vals_list)


class BarangBuktiItem(models.Model):
    _name        = 'digital_kamtibmas.barang_bukti_item'
    _description = 'Barang Bukti Pendukung'
    _order       = 'sequence, id'

    sequence        = fields.Integer(default=10)
    barang_bukti_id = fields.Many2one(
        'digital_kamtibmas.barang_bukti', 'Barang Bukti',
        required=True, ondelete='cascade')

    nama_barang     = fields.Char('Nama / Deskripsi', required=True)
    jenis_barang    = fields.Selection([
        ('dokumen',    'Dokumen (STNK / BPKB / SIM)'),
        ('kunci',      'Kunci Kontak / Duplikat'),
        ('aksesoris',  'Aksesoris Kendaraan'),
        ('elektronik', 'Elektronik / Gadget'),
        ('uang',       'Uang'),
        ('lainnya',    'Lainnya'),
    ], string='Jenis')
    jumlah          = fields.Float('Jumlah', default=1.0)
    satuan          = fields.Char('Satuan', help='Contoh: pcs, lembar, unit')
    kondisi         = fields.Selection([
        ('baik',           'Baik'),
        ('sebagian_rusak', 'Sebagian Rusak'),
        ('rusak',          'Rusak'),
    ], string='Kondisi', default='baik')
    foto            = fields.Image('Foto', max_width=800, max_height=800)
    keterangan      = fields.Char('Keterangan')
