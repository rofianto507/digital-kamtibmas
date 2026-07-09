from odoo import http, fields
from odoo.http import request
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)
_WIB = timedelta(hours=7)


def _now_wib_str():
    return (datetime.utcnow() + _WIB).strftime('%Y-%m-%d %H:%M:%S')


def _wib_to_utc(dt_str):
    if not dt_str:
        return False
    try:
        dt = datetime.strptime(dt_str.replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        return (dt - _WIB).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return False


class TahtiKioskController(http.Controller):

    # ── Halaman kiosk ─────────────────────────────────────────────────────────

    @http.route('/tahti/buku-tamu', type='http', auth='public', csrf=False, website=False)
    def kiosk_index(self, **kwargs):
        return request.render('digital_kamtibmas.tahti_kiosk_template', {})

    # ── API: cari tahanan aktif ───────────────────────────────────────────────

    @http.route('/tahti/api/cari_tahanan', type='jsonrpc', auth='public', csrf=False)
    def api_cari_tahanan(self, keyword='', **kwargs):
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
    def api_cek_nik(self, nik='', **kwargs):
        nik = (nik or '').strip()
        if not nik:
            return {'found': False}
        tamu = request.env['digital_kamtibmas.tahti_tamu'].sudo().search(
            [('nik', '=', nik)], limit=1
        )
        if tamu:
            return {
                'found': True,
                'id': tamu.id,
                'nama': tamu.nama,
                'no_hp': tamu.no_hp or '',
                'alamat': tamu.alamat or '',
            }
        return {'found': False}

    # ── API: daftar kunjungan baru ────────────────────────────────────────────

    @http.route('/tahti/api/daftar_kunjungan', type='jsonrpc', auth='public', csrf=False)
    def api_daftar_kunjungan(self, data=None, **kwargs):
        data = data or {}
        try:
            tahanan_id = int(data.get('tahanan_id') or 0)
            if not tahanan_id:
                return {'error': 'Tahanan wajib dipilih'}

            tahanan = request.env['digital_kamtibmas.tahanan'].sudo().browse(tahanan_id)
            if not tahanan.exists() or tahanan.state != 'ditahan':
                return {'error': 'Data tahanan tidak valid'}

            nik = (data.get('nik') or '').strip()
            if not nik:
                return {'error': 'NIK tamu wajib diisi'}

            nama = (data.get('nama') or '').strip()
            if not nama:
                return {'error': 'Nama tamu wajib diisi'}

            # Foto KTP: data URL → base64 string untuk field Image
            foto_ktp_b64 = None
            foto_raw = (data.get('foto_ktp') or '').strip()
            if foto_raw.startswith('data:'):
                try:
                    foto_ktp_b64 = foto_raw.split(',', 1)[1]
                except IndexError:
                    pass

            # Cari atau buat data tamu
            Tamu = request.env['digital_kamtibmas.tahti_tamu'].sudo()
            tamu = Tamu.search([('nik', '=', nik)], limit=1)
            if not tamu:
                create_vals = {
                    'nik':    nik,
                    'nama':   nama,
                    'no_hp':  (data.get('no_hp') or '').strip(),
                    'alamat': (data.get('alamat') or '').strip(),
                }
                if foto_ktp_b64:
                    create_vals['foto_ktp'] = foto_ktp_b64
                tamu = Tamu.create(create_vals)
            else:
                # Update data yang mungkin berubah
                update_vals = {}
                if nama and nama != tamu.nama:
                    update_vals['nama'] = nama
                no_hp = (data.get('no_hp') or '').strip()
                if no_hp and no_hp != (tamu.no_hp or ''):
                    update_vals['no_hp'] = no_hp
                if foto_ktp_b64:
                    update_vals['foto_ktp'] = foto_ktp_b64
                if update_vals:
                    tamu.write(update_vals)

            # Buat kunjungan
            kunjungan = request.env['digital_kamtibmas.tahti_kunjungan'].sudo().create({
                'tamu_id':    tamu.id,
                'tahanan_id': tahanan_id,
                'hubungan':   data.get('hubungan') or 'lainnya',
                'keperluan':  (data.get('keperluan') or '').strip(),
                'waktu_masuk': _wib_to_utc(_now_wib_str()) or fields.Datetime.now(),
                'state':      'berlangsung',
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
