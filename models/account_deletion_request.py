from odoo import models, fields
from odoo.exceptions import UserError


class AccountDeletionRequest(models.Model):
    _name = 'digital_kamtibmas.account_deletion_request'
    _description = 'Permintaan Hapus Akun'
    _order = 'tanggal_request desc'

    user_id = fields.Many2one('res.users', string='Pengguna', ondelete='set null')
    nama = fields.Char(string='Nama', required=True)
    login = fields.Char(string='Login / Email', required=True)
    alasan = fields.Text(string='Alasan (opsional)')
    tanggal_request = fields.Datetime(string='Tanggal Permintaan',
                                      default=fields.Datetime.now)
    state = fields.Selection([
        ('pending', 'Menunggu Diproses'),
        ('processed', 'Sudah Diproses'),
    ], string='Status', default='pending', required=True)
    catatan_admin = fields.Text(string='Catatan Admin')
    tanggal_proses = fields.Datetime(string='Tanggal Diproses')

    def action_hapus_akun(self):
        """Anonimkan + nonaktifkan akun pemohon (lihat menu Warga)."""
        warga_model = self.env['digital_kamtibmas.warga']
        for rec in self:
            if not rec.user_id:
                raise UserError('Permintaan ini tidak terhubung ke akun pengguna.')
            warga = warga_model.browse(rec.user_id.id).exists()
            if not warga:
                raise UserError(
                    'Akun %s bukan akun Masyarakat atau sudah dihapus.' % rec.login)
            warga.action_hapus_akun()
        return True

    def action_proses(self):
        self.write({
            'state': 'processed',
            'tanggal_proses': fields.Datetime.now(),
        })
