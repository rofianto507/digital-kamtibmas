import re
import secrets

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError

from odoo.addons.digital_kamtibmas.controllers.mobile_register import _validate_username


class PatroliGrup(models.Model):
    """Grup patroli Sabhara beserta akun login aplikasi patrolinya.

    Akun login dibuat/dikelola dari form ini (tombol Buat Akun, Reset Password,
    Nonaktifkan) sehingga admin DKM tidak perlu hak Settings → Users. Seperti
    menu Warga, aksi dijalankan dengan sudo terbatas: akun baru selalu hanya
    bergrup Patroli, dan aksi lanjutan hanya berlaku untuk akun bergrup Patroli.
    """
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
        ondelete='set null', copy=False,
        help='Akun yang digunakan grup ini untuk login ke aplikasi patroli. '
             'Dibuat lewat tombol "Buat Akun Login".',
    )
    username        = fields.Char(
        'Username', copy=False,
        help='Username untuk akun login baru: 4-30 karakter, diawali huruf, '
             'hanya huruf kecil, angka, titik, atau underscore.',
    )
    akun_login      = fields.Char('Username Login', compute='_compute_akun_info')
    akun_aktif      = fields.Boolean('Akun Aktif', compute='_compute_akun_info')
    active          = fields.Boolean('Aktif', default=True)

    patroli_count   = fields.Integer('Jumlah Patroli', compute='_compute_patroli_count')

    def _compute_patroli_count(self):
        PatroliModel = self.env['digital_kamtibmas.patroli']
        for rec in self:
            rec.patroli_count = PatroliModel.search_count([('grup_id', '=', rec.id)])

    @api.depends('user_id')
    def _compute_akun_info(self):
        for rec in self:
            user = rec.user_id.sudo().with_context(active_test=False)
            rec.akun_login = user.login or False
            rec.akun_aktif = bool(user) and user.active

    @api.onchange('name')
    def _onchange_name_username(self):
        if self.name and not self.user_id and not self.username:
            slug = re.sub(r'[^a-z0-9]+', '.', self.name.lower()).strip('.')
            self.username = ('patroli.%s' % slug)[:30].rstrip('.')

    def action_view_patroli(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f'Patroli – {self.name}',
            'res_model': 'digital_kamtibmas.patroli',
            'view_mode': 'list,form',
            'domain': [('grup_id', '=', self.id)],
            'context': {'default_grup_id': self.id},
        }

    # ── Penjagaan akun login ──────────────────────────────────────────────────

    def _guard_user_id(self, vals):
        """Akun login hanya boleh diatur lewat tombol (sudo) atau oleh admin
        sistem, supaya grup tidak bisa ditautkan ke akun admin atau warga."""
        if 'user_id' in vals and not self.env.su \
                and not self.env.user.has_group('base.group_system'):
            raise AccessError('Akun login grup hanya bisa diatur lewat tombol "Buat Akun Login".')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._guard_user_id(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._guard_user_id(vals)
        res = super().write(vals)
        if 'name' in vals:
            # Nama akun mengikuti nama grup (tampil di aplikasi & log patroli).
            # Hanya untuk akun Patroli murni; akun lain (data lama) dibiarkan.
            for rec in self.filtered('user_id'):
                user = rec.user_id.sudo()
                if user.has_group('digital_kamtibmas.group_dkm_patroli') \
                        and not user.has_group('base.group_system') \
                        and not user.has_group('digital_kamtibmas.group_dkm_admin'):
                    user.name = rec.name
        return res

    # ── Aksi admin ────────────────────────────────────────────────────────────

    def _check_admin(self):
        if not self.env.user.has_group('digital_kamtibmas.group_dkm_admin'):
            raise AccessError('Hanya Admin DKM yang boleh mengelola akun grup patroli.')

    def _patroli_user(self):
        """Akun login grup (sudo) bila akun itu memang akun Patroli saja."""
        self.ensure_one()
        user = self.user_id.sudo().with_context(active_test=False)
        if not user:
            return user
        if user.id == self.env.user.id:
            raise UserError('Anda tidak dapat memodifikasi akun Anda sendiri.')
        if not user.has_group('digital_kamtibmas.group_dkm_patroli'):
            raise UserError('Akun %s bukan akun Patroli.' % user.login)
        if user.has_group('base.group_system') or user.has_group('digital_kamtibmas.group_dkm_admin'):
            raise UserError('Akun %s memiliki hak admin dan tidak bisa dikelola dari sini.' % user.login)
        return user

    def _target_user(self):
        self._check_admin()
        self.ensure_one()
        user = self._patroli_user()
        if not user:
            raise UserError('Grup ini belum memiliki akun login.')
        return user

    @staticmethod
    def _random_password():
        """Password 8 digit angka, mudah disampaikan ke anggota grup patroli."""
        return ''.join(secrets.choice('0123456789') for _ in range(8))

    @staticmethod
    def _notif(title, message):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'type': 'success',
                'sticky': True,
                'next': {'type': 'ir.actions.client', 'tag': 'soft_reload'},
            },
        }

    def action_buat_akun(self):
        self._check_admin()
        self.ensure_one()
        if self.user_id:
            raise UserError('Grup ini sudah memiliki akun login.')
        username = (self.username or '').strip().lower()
        error = _validate_username(username)
        if error:
            raise UserError(error)
        pattern = username.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        Users = self.env['res.users'].sudo().with_context(active_test=False)
        if Users.search_count([('login', '=ilike', pattern)]):
            raise UserError('Username %s sudah dipakai.' % username)

        password = self._random_password()
        user = Users.with_context(no_reset_password=True).create({
            'name': self.name,
            'login': username,
            'password': password,
            # Grup dikunci di kode: hanya Patroli (+ user internal yang wajib).
            'group_ids': [(6, 0, [
                self.env.ref('digital_kamtibmas.group_dkm_patroli').id,
                self.env.ref('base.group_user').id,
            ])],
        })
        self.sudo().write({'user_id': user.id, 'username': username})
        return self._notif(
            'Akun dibuat: %s' % username,
            'Password: %s  (hanya tampil sekali, sampaikan ke grup patroli)' % password,
        )

    def action_reset_password(self):
        user = self._target_user()
        password = self._random_password()
        user.password = password
        return self._notif(
            'Password direset: %s' % user.login,
            'Password baru: %s  (hanya tampil sekali, sampaikan ke grup patroli)' % password,
        )

    def action_toggle_akun(self):
        user = self._target_user()
        user.active = not user.active
        return True
