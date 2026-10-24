import base64
import binascii
import logging

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools.image import image_process

_logger = logging.getLogger(__name__)

_NAME_MAX = 60
_FOTO_MAX_BYTES = 5 * 1024 * 1024  # setelah decode base64


class MobileProfileController(http.Controller):

    @http.route('/api/dkm/profil/update', type='jsonrpc', auth='user', csrf=False)
    def update_profil(self, nama=None, foto=None, **kwargs):
        """Ubah nama dan/atau foto profil milik user yang sedang login.

        Hanya akun sendiri (request.env.user); user lain tidak bisa diubah
        lewat endpoint ini. Field lain (login, grup, dll.) tidak tersentuh.
        """
        user = request.env.user
        vals = {}

        if nama is not None:
            nama = ' '.join(str(nama).split())
            if not nama:
                return {'ok': False, 'error': 'Nama tidak boleh kosong'}
            if len(nama) > _NAME_MAX:
                return {'ok': False, 'error': 'Nama maksimal %d karakter' % _NAME_MAX}
            vals['name'] = nama

        if foto:
            try:
                raw = base64.b64decode(foto, validate=True)
            except (binascii.Error, ValueError):
                return {'ok': False, 'error': 'Foto tidak valid'}
            if len(raw) > _FOTO_MAX_BYTES:
                return {'ok': False, 'error': 'Ukuran foto maksimal 5 MB'}
            try:
                # Verifikasi benar-benar gambar dan normalkan ukurannya
                vals['image_1920'] = base64.b64encode(
                    image_process(raw, size=(1024, 1024), verify_resolution=True)
                )
            except UserError:
                return {'ok': False, 'error': 'File bukan gambar yang valid'}

        if not vals:
            return {'ok': False, 'error': 'Tidak ada perubahan'}

        try:
            user.sudo().write(vals)
        except Exception:
            _logger.exception('update_profil gagal untuk user %s', user.id)
            return {'ok': False, 'error': 'Terjadi kesalahan server. Silakan coba lagi.'}

        return {'ok': True, 'name': user.name}
