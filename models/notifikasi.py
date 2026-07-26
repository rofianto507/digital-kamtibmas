from odoo import models, fields, api


class Notifikasi(models.Model):
    _name        = 'digital_kamtibmas.notifikasi'
    _description = 'Notifikasi Mobile'
    _order       = 'created_at desc'

    user_id    = fields.Many2one('res.users', string='Pengguna', required=True,
                                  ondelete='cascade', index=True)
    judul      = fields.Char('Judul', required=True)
    isi        = fields.Text('Isi')
    tipe       = fields.Selection([
        ('antrian',    'Antrian'),
        ('rehab',      'Rehabilitasi'),
        ('konseling',  'Konseling'),
        ('eform_laka', 'E-Form Laka'),
        ('system',     'Sistem'),
    ], string='Tipe', default='system', required=True)
    is_read    = fields.Boolean('Sudah Dibaca', default=False, index=True)
    created_at = fields.Datetime('Waktu', default=fields.Datetime.now, readonly=True)

    @api.model
    def get_allowed_dashboard_sections(self):
        """Return list of satker sections the current user may see in the dashboard."""
        user = self.env.user
        ALL = ['satlantas', 'satnarkoba', 'satreskrim', 'sabhara', 'tahti', 'intelkam']
        if user.has_group('digital_kamtibmas.group_dkm_admin') or \
                user.has_group('digital_kamtibmas.group_dkm_operator'):
            return ALL
        satker_map = {
            'satlantas':  'digital_kamtibmas.group_satlantas',
            'satnarkoba': 'digital_kamtibmas.group_satnarkoba',
            'satreskrim': 'digital_kamtibmas.group_satreskrim',
            'sabhara':    'digital_kamtibmas.group_sabhara',
            'tahti':      'digital_kamtibmas.group_tahti',
            'intelkam':   'digital_kamtibmas.group_intelkam',
        }
        sections = [s for s, g in satker_map.items() if user.has_group(g)]
        return sections if sections else ALL
