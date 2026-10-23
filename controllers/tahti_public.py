import hmac
import logging
import re

from odoo import http, fields
from odoo.exceptions import AccessDenied
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

PARAM_KIOSK_TOKEN = 'digital_kamtibmas.tahti_kiosk_token'
_NIK_RE = re.compile(r'^\d{16}$')
_HUBUNGAN = {'keluarga', 'pengacara', 'teman', 'lainnya'}


def _valid_token(token):
    stored = request.env['ir.config_parameter'].sudo().get_param(PARAM_KIOSK_TOKEN, '')
    return bool(stored) and bool(token) and hmac.compare_digest(str(token), stored)


def _check_token(token):
    """API kiosk hanya untuk perangkat yang memegang token (lihat menu Tahti > Kiosk Buku Tamu)."""
    if not _valid_token(token):
        raise AccessDenied('Token kiosk tidak valid.')


class TahtiKioskController(http.Controller):

    # ── Halaman kiosk ─────────────────────────────────────────────────────────

    @http.route('/tahti/buku-tamu', type='http', auth='public', csrf=False, website=False)
    def kiosk_index_legacy(self, **kwargs):
        # URL lama tanpa token sengaja dimatikan: data tahanan & pengunjung
        # tidak boleh terbuka untuk publik.
        return Response(
            '<body style="font-family:sans-serif;padding:60px;color:#666">'
            '<h2>Alamat kiosk buku tamu sudah berubah.</h2>'
            '<p>Hubungi administrator untuk mendapatkan URL kiosk yang baru.</p></body>',
            content_type='text/html', status=403,
        )

    @http.route('/tahti/buku-tamu/<string:token>', type='http', auth='public', csrf=False, website=False)
    def kiosk_index(self, token, **kwargs):
        if not _valid_token(token):
            return Response(
                '<body style="font-family:sans-serif;padding:60px;color:#666">'
                '<h2>403 — URL kiosk tidak valid atau sudah kedaluwarsa.</h2>'
                '<p>Hubungi administrator untuk mendapatkan URL baru.</p></body>',
                content_type='text/html', status=403,
            )
        return request.render('digital_kamtibmas.tahti_kiosk_template', {'token': token})

    # ── API: cari tahanan aktif ───────────────────────────────────────────────

    @http.route('/tahti/api/cari_tahanan', type='jsonrpc', auth='public', csrf=False)
    def api_cari_tahanan(self, token='', keyword='', **kwargs):
        _check_token(token)
        domain = [('state', '=', 'ditahan')]
        if keyword:
            domain += [('nama', 'ilike', keyword)]
        records = request.env['digital_kamtibmas.tahanan'].sudo().search_read(
            domain,
            ['id', 'nama', 'jenis_kelamin', 'kategori_id', 'sel_id'],
            order='nama asc',
            limit=20,
        )
        for r in records:
            r['sel_nama']     = r['sel_id'][1] if r.get('sel_id') else '-'
            r['kategori_nama'] = r['kategori_id'][1] if r.get('kategori_id') else '—'
            r.pop('sel_id', None)
            r.pop('kategori_id', None)
        return records

    # ── API: cari / cek tamu by NIK ───────────────────────────────────────────

    @http.route('/tahti/api/cek_nik', type='jsonrpc', auth='public', csrf=False)
    def api_cek_nik(self, token='', nik='', **kwargs):
        _check_token(token)
        nik = (nik or '').strip()
        if not _NIK_RE.match(nik):
            return {'found': False}
        tamu = request.env['digital_kamtibmas.tahti_tamu'].sudo().search(
            [('nik', '=', nik)], limit=1
        )
        if tamu:
            # Hanya yang dipakai layar kiosk; alamat tidak dikirim.
            return {
                'found': True,
                'nama': tamu.nama,
                'no_hp': tamu.no_hp or '',
            }
        return {'found': False}

    # ── API: daftar kunjungan baru ────────────────────────────────────────────

    @http.route('/tahti/api/daftar_kunjungan', type='jsonrpc', auth='public', csrf=False)
    def api_daftar_kunjungan(self, token='', data=None, **kwargs):
        _check_token(token)
        data = data or {}
        try:
            tahanan_id = int(data.get('tahanan_id') or 0)
            if not tahanan_id:
                return {'error': 'Tahanan wajib dipilih'}

            tahanan = request.env['digital_kamtibmas.tahanan'].sudo().browse(tahanan_id)
            if not tahanan.exists() or tahanan.state != 'ditahan':
                return {'error': 'Data tahanan tidak valid'}

            nik = (data.get('nik') or '').strip()
            if not _NIK_RE.match(nik):
                return {'error': 'NIK harus 16 digit angka'}

            nama = (data.get('nama') or '').strip()
            if not nama:
                return {'error': 'Nama tamu wajib diisi'}

            hubungan = data.get('hubungan')
            if hubungan not in _HUBUNGAN:
                hubungan = 'lainnya'

            # Foto KTP: data URL → base64 string untuk field Image
            foto_ktp_b64 = None
            foto_raw = (data.get('foto_ktp') or '').strip()
            if foto_raw.startswith('data:'):
                try:
                    foto_ktp_b64 = foto_raw.split(',', 1)[1]
                except IndexError:
                    pass

            no_hp = (data.get('no_hp') or '').strip()

            # Cari atau buat data tamu
            Tamu = request.env['digital_kamtibmas.tahti_tamu'].sudo()
            tamu = Tamu.search([('nik', '=', nik)], limit=1)
            if not tamu:
                create_vals = {'nik': nik, 'nama': nama, 'no_hp': no_hp}
                if foto_ktp_b64:
                    create_vals['foto_ktp'] = foto_ktp_b64
                tamu = Tamu.create(create_vals)
            else:
                # Kiosk tidak boleh menimpa data tamu yang sudah ada (siapa pun
                # bisa mengetik NIK orang lain); hanya mengisi yang masih kosong.
                # Perubahan data dilakukan petugas di backend.
                update_vals = {}
                if no_hp and not tamu.no_hp:
                    update_vals['no_hp'] = no_hp
                if foto_ktp_b64 and not tamu.foto_ktp:
                    update_vals['foto_ktp'] = foto_ktp_b64
                if update_vals:
                    tamu.write(update_vals)

            # Buat kunjungan
            kunjungan = request.env['digital_kamtibmas.tahti_kunjungan'].sudo().create({
                'tamu_id':     tamu.id,
                'tahanan_id':  tahanan_id,
                'hubungan':    hubungan,
                'keperluan':   (data.get('keperluan') or '').strip(),
                'waktu_masuk': fields.Datetime.now(),
                'state':       'berlangsung',
                # Default petugas = user saat ini, yang di kiosk adalah Public user.
                'petugas_id':  False,
            })
            return {
                'success': True,
                'code': kunjungan.code,
                'tamu_nama': tamu.nama,
                'tahanan_nama': tahanan.nama,
            }
        except Exception as e:
            _logger.error('daftar_kunjungan error: %s', e, exc_info=True)
            return {'error': 'Terjadi kesalahan. Silakan coba lagi.'}
