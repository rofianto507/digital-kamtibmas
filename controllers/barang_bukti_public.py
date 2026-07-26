from odoo import http
from odoo.http import request


class BarangBuktiPublicController(http.Controller):

    @http.route('/api/dkm/barang-bukti/cari', type='json', auth='public', csrf=False)
    def cari_barang_bukti(self, filter_type='nopol', query='', **kwargs):
        query = (query or '').strip()
        if not query:
            return {'ok': False, 'error': 'Query wajib diisi'}

        field_map = {
            'nopol':  'nomor_polisi',
            'rangka': 'nomor_rangka',
            'mesin':  'nomor_mesin',
        }
        field = field_map.get(filter_type, 'nomor_polisi')

        records = request.env['digital_kamtibmas.barang_bukti'].sudo().search_read(
            [[field, 'ilike', query]],
            fields=[
                'code', 'nomor_perkara', 'jenis_kendaraan',
                'merek', 'tipe', 'warna', 'tahun_kendaraan',
                'nomor_polisi', 'nomor_rangka', 'nomor_mesin',
                'nama_pelapor', 'nama_pemilik_stnk',
                'tanggal_penerimaan', 'lokasi_penyimpanan', 'state',
            ],
            order='id desc',
            limit=20,
        )

        # Konversi datetime ke string ISO agar mudah di-parse Flutter
        for r in records:
            if r.get('tanggal_penerimaan'):
                r['tanggal_penerimaan'] = str(r['tanggal_penerimaan'])

        return {'ok': True, 'data': records}
