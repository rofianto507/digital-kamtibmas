from odoo import models, fields


class PatroliGrup(models.Model):
    _name        = 'digital_kamtibmas.patroli_grup'
    _description = 'Grup Patroli Sabhara'
    _order       = 'name asc'
    _rec_name    = 'name'

    name            = fields.Char('Nama Grup', required=True)
    no_pol          = fields.Char('Nomor Polisi Kendaraan')
    jenis_kendaraan = fields.Selection([
        ('mobil', 'Mobil'),
        ('motor', 'Motor'),
        ('lain',  'Lainnya'),
    ], string='Jenis Kendaraan', default='mobil')
    keterangan      = fields.Text('Keterangan')
    user_id         = fields.Many2one(
        'res.users', 'Akun Login Grup',
        ondelete='set null',
        help='Akun yang digunakan grup ini untuk login ke aplikasi patroli.',
    )
    active          = fields.Boolean('Aktif', default=True)

    patroli_count   = fields.Integer('Jumlah Patroli', compute='_compute_patroli_count')

    def _compute_patroli_count(self):
        PatroliModel = self.env['digital_kamtibmas.patroli']
        for rec in self:
            rec.patroli_count = PatroliModel.search_count([('grup_id', '=', rec.id)])

    def action_view_patroli(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f'Patroli – {self.name}',
            'res_model': 'digital_kamtibmas.patroli',
            'view_mode': 'list,form',
            'domain': [('grup_id', '=', self.id)],
            'context': {'default_grup_id': self.id},
        }
