from odoo import models, fields, api


class Patroli(models.Model):
    _name        = 'digital_kamtibmas.patroli'
    _description = 'Patroli Sabhara'
    _inherit     = ['mail.thread', 'mail.activity.mixin']
    _order       = 'id desc'
    _rec_name    = 'code'

    code             = fields.Char('No. Patroli', readonly=True, default='New', copy=False, tracking=True)
    tanggal_patroli  = fields.Datetime('Tanggal Mulai Patroli', required=True, tracking=True)
    tanggal_selesai  = fields.Datetime('Tanggal Selesai', tracking=True)
    keterangan       = fields.Text('Keterangan / Rute')
    state            = fields.Selection([
        ('menunggu', 'Menunggu'),
        ('berjalan', 'Berjalan'),
        ('selesai',  'Selesai'),
    ], string='Status', default='menunggu', required=True, tracking=True)

    personel_ids = fields.One2many(
        'digital_kamtibmas.patroli_personel', 'patroli_id',
        string='Personel')
    titik_ids    = fields.One2many(
        'digital_kamtibmas.patroli_titik', 'patroli_id',
        string='Titik Lokasi')

    # ── Workflow ──────────────────────────────────────────────────────────────

    def action_mulai(self):
        self.state = 'berjalan'

    def action_selesai(self):
        self.write({'state': 'selesai', 'tanggal_selesai': fields.Datetime.now()})

    def action_reset(self):
        self.state = 'menunggu'

    # ── Auto-code ─────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'digital_kamtibmas.patroli') or 'New'
        return super().create(vals_list)


class PatroliPersonel(models.Model):
    _name        = 'digital_kamtibmas.patroli_personel'
    _description = 'Personel Patroli'
    _order       = 'sequence, id'

    sequence    = fields.Integer(default=10)
    patroli_id  = fields.Many2one(
        'digital_kamtibmas.patroli', required=True, ondelete='cascade')
    nama        = fields.Char('Nama', required=True)
    pangkat     = fields.Char('Pangkat')


class PatroliTitik(models.Model):
    _name        = 'digital_kamtibmas.patroli_titik'
    _description = 'Titik Lokasi Patroli'
    _order       = 'create_date asc, id asc'

    patroli_id  = fields.Many2one(
        'digital_kamtibmas.patroli', required=True, ondelete='cascade')
    latitude    = fields.Float('Latitude',  digits=(10, 6))
    longitude   = fields.Float('Longitude', digits=(10, 6))
