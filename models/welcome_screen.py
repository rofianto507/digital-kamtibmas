from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class WelcomeScreen(models.Model):
    _name = 'digital.kamtibmas.welcome.screen'
    _description = 'Welcome Screen Mobile'

    name = fields.Char('Judul', required=True)
    image = fields.Binary('Gambar', required=True, attachment=True)
    image_filename = fields.Char('Nama File Gambar')
    active = fields.Boolean('Aktif', default=True)
    tanggal_mulai = fields.Date('Tampil Mulai')
    tanggal_selesai = fields.Date('Tampil Sampai')
    keterangan = fields.Text('Keterangan')

    @api.constrains('active')
    def _check_single_active(self):
        for rec in self:
            if rec.active:
                others = self.search([('active', '=', True), ('id', '!=', rec.id)])
                if others:
                    raise ValidationError(
                        'Hanya boleh ada satu Welcome Screen yang aktif. '
                        'Nonaktifkan yang lain terlebih dahulu.'
                    )
