from odoo import models, fields, api


class RehabTempat(models.Model):
    _name = 'digital_kamtibmas.rehab.tempat'
    _description = 'Tempat Rehabilitasi'
    _order = 'name'

    name       = fields.Char('Nama Tempat', required=True)
    alamat     = fields.Text('Alamat')
    no_telp    = fields.Char('No. Telepon')
    active     = fields.Boolean(default=True)
    partner_id = fields.Many2one('res.partner', 'Kontak', ondelete='set null', readonly=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Nama tempat rehabilitasi sudah terdaftar.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if not rec.partner_id:
                partner = self.env['res.partner'].sudo().create({
                    'name': rec.name,
                    'phone': rec.no_telp or False,
                    'street': rec.alamat or False,
                    'is_company': True,
                })
                rec.partner_id = partner.id
        return records

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.partner_id:
                partner_vals = {}
                if 'name' in vals:
                    partner_vals['name'] = vals['name']
                if 'no_telp' in vals:
                    partner_vals['phone'] = vals['no_telp']
                if 'alamat' in vals:
                    partner_vals['street'] = vals['alamat']
                if partner_vals:
                    rec.partner_id.sudo().write(partner_vals)
        return res

    def action_buka_partner(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'new',
        }
