from odoo import models, fields, api


class IntelkamWaGroup(models.Model):
    _name = 'intelkam.wa.group'
    _description = 'Group WhatsApp Intelkam'
    _order = 'satker, name'
    _rec_name = 'name'

    name = fields.Char('Nama Group', required=True)
    group_id = fields.Char('Group ID WhatsApp', required=True,
                            help='Nomor group dari Wablas Inbox (contoh: 120363428002197043). Buka Wablas > Inbox, lihat nomor di daftar chat group.')
    satker = fields.Selection([
        ('polrestabes', 'Polrestabes Palembang'),
        ('satlantas', 'Satlantas'),
        ('satnarkoba', 'Satnarkoba'),
        ('satreskrim', 'Satreskrim'),
        ('sabhara', 'Sabhara'),
        ('tahti', 'Tahti'),
        ('intelkam', 'Intelkam'),
        ('binmas', 'Binmas'),
        ('polsek', 'Polsek'),
        ('lainnya', 'Lainnya'),
    ], string='Satuan Kerja / Satwil', required=True)
    keterangan = fields.Char('Keterangan')
    active = fields.Boolean(default=True)

    respon_ids = fields.One2many('intelkam.respon.wa', 'wa_group_id', string='Pesan Masuk')
    respon_count = fields.Integer('Total Pesan', compute='_compute_respon_count', store=True)

    distribusi_ids = fields.Many2many(
        'intelkam.distribusi.info',
        'intelkam_distribusi_group_rel',
        'group_id_rel', 'distribusi_id',
        string='Riwayat Distribusi',
    )
    distribusi_count = fields.Integer('Total Distribusi', compute='_compute_distribusi_count', store=True)

    _sql_constraints = [
        ('unique_group_id', 'UNIQUE(group_id)', 'Group ID WhatsApp harus unik.'),
    ]

    @api.depends('respon_ids')
    def _compute_respon_count(self):
        for rec in self:
            rec.respon_count = len(rec.respon_ids)

    @api.depends('distribusi_ids')
    def _compute_distribusi_count(self):
        for rec in self:
            rec.distribusi_count = len(rec.distribusi_ids)

    def name_get(self):
        return [(r.id, r.name) for r in self]

    def action_view_respon(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Pesan Masuk — {self.name}',
            'res_model': 'intelkam.respon.wa',
            'view_mode': 'list,form',
            'domain': [('wa_group_id', '=', self.id)],
            'context': {'default_wa_group_id': self.id},
        }

    def action_view_distribusi(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Distribusi — {self.name}',
            'res_model': 'intelkam.distribusi.info',
            'view_mode': 'list,form',
            'domain': [('group_ids', 'in', self.id)],
        }
