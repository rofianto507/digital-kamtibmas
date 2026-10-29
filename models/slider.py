from urllib.parse import urlparse

from odoo import api, models, fields
from odoo.exceptions import ValidationError


class Slider(models.Model):
    _name = 'digital.kamtibmas.slider'
    _description = 'Slider Mobile'
    _order = 'sequence asc, id asc'

    name = fields.Char('Judul', required=True)
    image = fields.Binary('Gambar', required=True, attachment=True)
    image_filename = fields.Char('Nama File')
    url = fields.Char(
        'URL Tujuan',
        help='Opsional. Jika diisi, banner bisa diketuk di aplikasi mobile dan '
             'membuka alamat ini di browser. Harus diawali http:// atau https://.')
    sequence = fields.Integer('Urutan', default=10)
    active = fields.Boolean('Aktif', default=True)

    @api.constrains('url')
    def _check_url(self):
        # Hanya http/https: cegah skema berbahaya (javascript:, file:, intent:, dll.)
        for rec in self:
            if not rec.url:
                continue
            parsed = urlparse(rec.url.strip())
            if parsed.scheme not in ('http', 'https') or not parsed.netloc:
                raise ValidationError(
                    'URL Tujuan harus berupa alamat lengkap yang diawali http:// atau https:// '
                    '(contoh: https://contoh.id/halaman).')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('url'):
                vals['url'] = vals['url'].strip()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('url'):
            vals['url'] = vals['url'].strip()
        return super().write(vals)
