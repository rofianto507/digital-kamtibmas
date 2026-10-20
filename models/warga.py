import secrets
import string

from odoo import models, fields, api, tools
from odoo.exceptions import AccessError, UserError

_LAYANAN = [
    # (field hitung, model, label)
    ('antrian_count',   'digital_kamtibmas.antrian',   'Antrian'),
    ('eform_count',     'digital_kamtibmas.eform_laka', 'e-Form Laka'),
    ('konseling_count', 'digital_kamtibmas.konseling', 'Konseling'),
    ('rehab_count',     'digital_kamtibmas.rehab',     'Rehabilitasi'),
]


class Warga(models.Model):
    """Daftar akun masyarakat (grup Masyarakat) dari aplikasi mobile.

    View SQL read-only di atas res.users: admin DKM tidak perlu hak Settings
    dan tidak bisa mengubah grup/hak akses user lain. Aksi (nonaktifkan, reset
    password, hapus) dijalankan lewat method di bawah dengan sudo terbatas pada
    user bergrup Masyarakat saja.
    """
    _name = 'digital_kamtibmas.warga'
    _description = 'Warga (Akun Masyarakat)'
    _auto = False
    # Web client selalu meminta write_date saat membuka form, jadi view SQL
    # harus menyediakan kolom log akses (create_uid, write_uid, write_date).
    _log_access = True
    _order = 'create_date desc'
    _rec_name = 'name'

    user_id = fields.Many2one('res.users', string='Akun', readonly=True)
    name = fields.Char('Nama', readonly=True)
    login = fields.Char('Username', readonly=True)
    phone = fields.Char('No. Telepon', readonly=True)
    street = fields.Char('Alamat', readonly=True)
    active = fields.Boolean('Aktif', readonly=True)
    create_date = fields.Datetime('Tanggal Daftar', readonly=True)
    # Binary (bukan Image): model view SQL tidak punya _log_access.
    image_128 = fields.Binary('Foto', related='user_id.image_128', readonly=True)

    antrian_count = fields.Integer('Antrian', compute='_compute_counts')
    eform_count = fields.Integer('e-Form Laka', compute='_compute_counts')
    konseling_count = fields.Integer('Konseling', compute='_compute_counts')
    rehab_count = fields.Integer('Rehabilitasi', compute='_compute_counts')
    deletion_pending = fields.Boolean('Minta Hapus Akun', compute='_compute_deletion_pending')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT u.id AS id,
                       u.id AS user_id,
                       p.name AS name,
                       u.login AS login,
                       p.phone AS phone,
                       p.street AS street,
                       u.active AS active,
                       u.create_uid AS create_uid,
                       u.create_date AS create_date,
                       u.write_uid AS write_uid,
                       u.write_date AS write_date
                FROM res_users u
                JOIN res_partner p ON p.id = u.partner_id
                WHERE EXISTS (
                    SELECT 1
                    FROM res_groups_users_rel r
                    JOIN ir_model_data d
                      ON d.res_id = r.gid
                     AND d.model = 'res.groups'
                     AND d.module = 'digital_kamtibmas'
                     AND d.name = 'group_masyarakat'
                    WHERE r.uid = u.id
                )
            )
        """ % self._table)

    # ── Hitung pemakaian layanan ──────────────────────────────────────────────

    @api.depends('user_id')
    def _compute_counts(self):
        user_ids = self.mapped('user_id').ids
        counts = {}
        for field_name, model, _label in _LAYANAN:
            groups = self.env[model].sudo().with_context(active_test=False)._read_group(
                [('user_id', 'in', user_ids)], ['user_id'], ['__count'])
            counts[field_name] = {user.id: n for user, n in groups}
        for rec in self:
            for field_name, _model, _label in _LAYANAN:
                rec[field_name] = counts[field_name].get(rec.user_id.id, 0)

    def _compute_deletion_pending(self):
        pending = self.env['digital_kamtibmas.account_deletion_request'].sudo().search([
            ('user_id', 'in', self.mapped('user_id').ids),
            ('state', '=', 'pending'),
        ]).mapped('user_id').ids
        for rec in self:
            rec.deletion_pending = rec.user_id.id in pending

    # ── Smart button ──────────────────────────────────────────────────────────

    def _open_layanan(self, model, title):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': '%s — %s' % (title, self.name),
            'res_model': model,
            'view_mode': 'list,form',
            'domain': [('user_id', '=', self.user_id.id)],
        }

    def action_open_antrian(self):
        return self._open_layanan('digital_kamtibmas.antrian', 'Antrian')

    def action_open_eform(self):
        return self._open_layanan('digital_kamtibmas.eform_laka', 'e-Form Laka')

    def action_open_konseling(self):
        return self._open_layanan('digital_kamtibmas.konseling', 'Konseling')

    def action_open_rehab(self):
        return self._open_layanan('digital_kamtibmas.rehab', 'Rehabilitasi')

    # ── Aksi admin ────────────────────────────────────────────────────────────

    def _target_users(self):
        """Validasi hak akses + pastikan target adalah akun Masyarakat."""
        if not self.env.user.has_group('digital_kamtibmas.group_dkm_admin'):
            raise AccessError('Hanya Admin DKM yang boleh melakukan aksi ini.')
        group = self.env.ref('digital_kamtibmas.group_masyarakat')
        users = self.mapped('user_id').sudo()
        for user in users:
            if user.id == self.env.user.id:
                raise UserError('Anda tidak dapat memodifikasi akun Anda sendiri.')
            if group not in user.group_ids:
                raise UserError('Akun %s bukan akun Masyarakat.' % user.login)
        return users

    @staticmethod
    def _random_password(length=10):
        chars = string.ascii_letters + string.digits
        while True:
            pwd = ''.join(secrets.choice(chars) for _ in range(length))
            if any(c.isalpha() for c in pwd) and any(c.isdigit() for c in pwd):
                return pwd

    def action_toggle_active(self):
        users = self._target_users()
        for user in users:
            user.active = not user.active
        return True

    def action_reset_password(self):
        users = self._target_users()
        if len(users) != 1:
            raise UserError('Reset password hanya untuk satu akun setiap kali.')
        user = users[0]
        password = self._random_password()
        user.password = password
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Password direset: %s' % user.login,
                'message': 'Password baru: %s  (hanya tampil sekali, sampaikan ke warga)' % password,
                'type': 'success',
                'sticky': True,
            },
        }

    def action_hapus_akun(self):
        """Hapus akun dengan menganonimkan: data pribadi dihapus, akun
        dinonaktifkan, tetapi baris layanan (antrian, laka, dll.) tetap utuh
        agar relasi data tidak rusak."""
        users = self._target_users()
        requests = self.env['digital_kamtibmas.account_deletion_request'].sudo()
        for user in users:
            partner = user.partner_id
            old_login = user.login
            partner.write({
                'name': 'Akun Dihapus',
                'street': False, 'street2': False, 'city': False, 'zip': False,
                'phone': False, 'email': False, 'image_1920': False,
            })
            # Login diganti sebelum nonaktif agar username bisa dipakai lagi
            # dan password lama tidak berlaku.
            user.write({
                'login': 'dihapus.%s' % user.id,
                'password': self._random_password(24),
                'active': False,
            })
            requests.search([
                ('user_id', '=', user.id), ('state', '=', 'pending'),
            ]).write({
                'state': 'processed',
                'tanggal_proses': fields.Datetime.now(),
                'catatan_admin': 'Akun %s dianonimkan dan dinonaktifkan oleh %s.' % (
                    old_login, self.env.user.name),
            })
        return True
