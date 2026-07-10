from odoo import models, fields, api


class EformLaka(models.Model):
    _name = 'digital_kamtibmas.eform_laka'
    _description = 'e-Form Laka Lantas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'tanggal_kejadian desc'
    _rec_name = 'code'

    code = fields.Char('Kode', readonly=True, copy=False, default='New')
    user_id = fields.Many2one(
        'res.users', string='Pelapor',
        required=True, default=lambda self: self.env.user,
        tracking=True,
    )
    tanggal_kejadian = fields.Datetime(
        'Tanggal Kejadian', required=True,
        default=fields.Datetime.now, tracking=True,
    )
    yang_terlibat_id = fields.Many2one(
        'digital_kamtibmas.yang_terlibat',
        string='Yang Terlibat',
        tracking=True,
    )
    jumlah_luka_luka = fields.Integer('Jumlah Luka-luka', default=0)
    jumlah_meninggal = fields.Integer('Jumlah Meninggal', default=0)
    rumah_sakit = fields.Char('Rumah Sakit Tujuan')
    keterangan = fields.Text('Keterangan')
    lat = fields.Float('Latitude', digits=(10, 6))
    lng = fields.Float('Longitude', digits=(10, 6))
    foto = fields.Binary('Foto', attachment=True)
    foto_filename = fields.Char('Nama File Foto')
    state = fields.Selection([
        ('BARU', 'BARU'),
        ('DIPROSES', 'DIPROSES'),
        ('SELESAI', 'SELESAI'),
    ], string='Status', required=True, default='BARU', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') or vals['code'] == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'digital_kamtibmas.eform_laka.sequence') or 'New'
        return super().create(vals_list)

    def action_set_diproses(self):
        self.write({'state': 'DIPROSES'})

    def action_set_selesai(self):
        self.write({'state': 'SELESAI'})

    def action_set_baru(self):
        self.write({'state': 'BARU'})
