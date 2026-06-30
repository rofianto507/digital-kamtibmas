from odoo import models, fields, api


class BarangBukti(models.Model):
    _name        = 'digital_kamtibmas.barang_bukti'
    _description = 'Barang Bukti Online Satreskrim'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'id desc'
    _rec_name    = 'code'

    code                = fields.Char('No. Barang Bukti', readonly=True, default='New', copy=False, tracking=True)

    # ── Informasi Perkara ─────────────────────────────────────────────────────
    nomor_perkara       = fields.Char('No. Perkara / SP3', tracking=True)
    jenis_perkara       = fields.Selection([
        ('pencurian',     'Pencurian'),
        ('penipuan',      'Penipuan / Penggelapan'),
        ('penganiayaan',  'Penganiayaan / Kekerasan'),
        ('narkoba',       'Narkoba'),
        ('korupsi',       'Korupsi'),
        ('cybercrime',    'Cyber Crime'),
        ('pemerkosaan',   'Kesusilaan'),
        ('pembunuhan',    'Pembunuhan'),
        ('lainnya',       'Lainnya'),
    ], string='Jenis Perkara', tracking=True)
    lokasi_kejadian     = fields.Char('Lokasi Kejadian')
    tanggal_penyitaan   = fields.Date('Tanggal Penyitaan')
    tanggal_penerimaan  = fields.Date('Tanggal Diterima', default=fields.Date.today)
    petugas_id          = fields.Many2one('res.users', 'Penyidik / Petugas', tracking=True)

    # ── Identitas Pelapor / Pemilik ───────────────────────────────────────────
    nama_pelapor        = fields.Char('Nama Pelapor / Pemilik', required=True)
    nik_pelapor         = fields.Char('NIK', size=16)
    no_hp_pelapor       = fields.Char('No. HP / WA')
    alamat_pelapor      = fields.Text('Alamat Pelapor')

    # ── Daftar Item Barang Bukti ──────────────────────────────────────────────
    item_ids            = fields.One2many(
        'digital_kamtibmas.barang_bukti_item', 'barang_bukti_id',
        string='Daftar Barang Bukti')

    # ── Lokasi Penyimpanan & Catatan ──────────────────────────────────────────
    lokasi_penyimpanan  = fields.Char('Lokasi Penyimpanan', help='Nomor rak / ruangan')
    keterangan          = fields.Text('Keterangan / Catatan')

    # ── Status ────────────────────────────────────────────────────────────────
    state               = fields.Selection([
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
    _description = 'Item Barang Bukti'
    _order       = 'sequence, id'

    sequence        = fields.Integer(default=10)
    barang_bukti_id = fields.Many2one(
        'digital_kamtibmas.barang_bukti', 'Barang Bukti',
        required=True, ondelete='cascade')

    nama_barang     = fields.Char('Nama / Deskripsi Barang', required=True)
    jenis_barang    = fields.Selection([
        ('senjata',     'Senjata / Sajam'),
        ('narkoba',     'Narkotika / Psikotropika'),
        ('dokumen',     'Dokumen / Surat'),
        ('elektronik',  'Elektronik / Gadget'),
        ('kendaraan',   'Kendaraan'),
        ('uang',        'Uang'),
        ('pakaian',     'Pakaian / Tekstil'),
        ('lainnya',     'Lainnya'),
    ], string='Jenis Barang')
    jumlah          = fields.Float('Jumlah', default=1.0)
    satuan          = fields.Char('Satuan', help='Contoh: pcs, gram, kg, liter, unit')
    kondisi         = fields.Selection([
        ('baik',           'Baik'),
        ('sebagian_rusak', 'Sebagian Rusak'),
        ('rusak',          'Rusak'),
    ], string='Kondisi', default='baik')
    foto            = fields.Image('Foto', max_width=800, max_height=800)
    keterangan      = fields.Char('Keterangan')
