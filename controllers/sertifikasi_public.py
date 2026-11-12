import random
from datetime import datetime, timedelta
from odoo import http, fields
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)
_WIB = timedelta(hours=7)
GRACE_MENIT = 2  # toleransi keterlambatan submit (menit)


def _today_wib():
    return (datetime.utcnow() + _WIB).date()


class SertifikasiPublicController(http.Controller):

    # ── Halaman kiosk ─────────────────────────────────────────────────────────

    @http.route('/sertifikasi/<string:token>', type='http', auth='public', csrf=False, website=False)
    def kiosk_index(self, token, **kwargs):
        return request.render('digital_kamtibmas.sertifikasi_kiosk_template', {
            'company_logo_url': '/digital_kamtibmas/static/img/logo_app.png',
        })

    # ── API: info sertifikasi ─────────────────────────────────────────────────

    @http.route('/sertifikasi/api/info', type='jsonrpc', auth='public', csrf=False)
    def api_info(self, token='', **kwargs):
        token = (token or '').strip()
        if not token:
            return {'error': 'Token tidak valid'}

        s = request.env['digital_kamtibmas.sertifikasi'].sudo().search(
            [('access_token', '=', token)], limit=1)
        if not s:
            return {'error': 'Link ujian tidak ditemukan'}

        today = _today_wib()
        if s.state != 'aktif':
            return {'error': 'Ujian ini tidak aktif saat ini'}
        if s.tanggal_expired and today > s.tanggal_expired:
            return {'error': 'Ujian ini sudah berakhir'}
        if s.tanggal_aktif and today < s.tanggal_aktif:
            return {'error': f'Ujian belum dibuka. Mulai tanggal {s.tanggal_aktif.strftime("%d/%m/%Y")}'}

        total_soal_tersedia = request.env['digital_kamtibmas.sertifikasi.soal'].sudo().search_count(
            [('active', '=', True), ('has_kunci', '=', True)])

        return {
            'id':              s.id,
            'name':            s.name,
            'jumlah_soal':     min(s.jumlah_soal, total_soal_tersedia),
            'waktu_menit':     s.waktu_menit,
            'nilai_kelulusan': s.nilai_kelulusan,
            'tanggal_expired': s.tanggal_expired.strftime('%d/%m/%Y') if s.tanggal_expired else '',
        }

    def _finalize(self, peserta, pilih):
        """Nilai percobaan memakai soal yang DILAYANI server (bukan klien).
        pilih: {soal_id: pilihan_id}. Soal tanpa jawaban sah dihitung salah."""
        Pilihan = request.env['digital_kamtibmas.sertifikasi.pilihan'].sudo()
        total_benar = 0
        for jw in peserta.jawaban_ids:
            pid = pilih.get(jw.soal_id.id, 0)
            pil = Pilihan.browse(pid) if pid else Pilihan
            # pilihan harus milik soal tsb
            ok = bool(pil.exists() and pil.soal_id.id == jw.soal_id.id)
            correct = ok and bool(pil.is_correct)
            jw.write({'pilihan_id': pil.id if ok else False, 'is_correct': correct})
            total_benar += 1 if correct else 0
        total_soal = len(peserta.jawaban_ids)
        nilai = round(total_benar / total_soal * 100, 1) if total_soal else 0.0
        peserta.write({
            'total_benar':   total_benar,
            'total_soal':    total_soal,
            'nilai':         nilai,
            'lulus':         nilai >= peserta.sertifikasi_id.nilai_kelulusan,
            'waktu_selesai': fields.Datetime.now(),
            'state':         'selesai',
        })

    # ── API: cek NIK (auto-fill identitas) ───────────────────────────────────

    @http.route('/sertifikasi/api/cek_nik', type='jsonrpc', auth='public', csrf=False)
    def api_cek_nik(self, token='', nik='', **kwargs):
        token = (token or '').strip()
        nik   = (nik   or '').strip()

        if len(nik) < 16:
            return {'found': False}

        s = request.env['digital_kamtibmas.sertifikasi'].sudo().search(
            [('access_token', '=', token), ('state', '=', 'aktif')], limit=1)
        if not s:
            return {'found': False}

        profil = request.env['digital_kamtibmas.sertifikasi.profil'].sudo().search(
            [('nik', '=', nik)], limit=1)
        if not profil:
            return {'found': False}

        # Jangan kembalikan data pribadi (nama, lahir, HP, alamat) ke klien publik.
        return {'found': True}

    # ── API: mulai ujian ──────────────────────────────────────────────────────

    @http.route('/sertifikasi/api/mulai', type='jsonrpc', auth='public', csrf=False)
    def api_mulai(self, token='', data=None, **kwargs):
        data  = data or {}
        token = (token or '').strip()

        s = request.env['digital_kamtibmas.sertifikasi'].sudo().search(
            [('access_token', '=', token), ('state', '=', 'aktif')], limit=1)
        if not s:
            return {'error': 'Sertifikasi tidak valid atau tidak aktif'}

        today = _today_wib()
        if s.tanggal_expired and today > s.tanggal_expired:
            return {'error': 'Ujian sudah berakhir'}

        # Validasi identitas
        nik  = (data.get('nik')  or '').strip()
        nama = (data.get('nama') or '').strip()
        if not nik:
            return {'error': 'NIK wajib diisi'}
        if len(nik) < 16:
            return {'error': 'NIK harus 16 digit'}
        if not nama:
            return {'error': 'Nama lengkap wajib diisi'}

        Peserta = request.env['digital_kamtibmas.sertifikasi.peserta'].sudo()
        Profil  = request.env['digital_kamtibmas.sertifikasi.profil'].sudo()

        # Get or create profil terlebih dahulu
        profil = Profil.search([('nik', '=', nik)], limit=1)
        if profil:
            # Update data kontak yang mungkin berubah (no_hp, alamat)
            update_vals = {}
            if data.get('no_hp') and profil.no_hp != (data['no_hp'] or '').strip():
                update_vals['no_hp'] = (data['no_hp'] or '').strip()
            if data.get('alamat') and profil.alamat != (data['alamat'] or '').strip():
                update_vals['alamat'] = (data['alamat'] or '').strip()
            if update_vals:
                profil.write(update_vals)
        else:
            profil = Profil.create({
                'nik':           nik,
                'nama':          nama,
                'tempat_lahir':  (data.get('tempat_lahir') or '').strip(),
                'tanggal_lahir': data.get('tanggal_lahir') or False,
                'jenis_kelamin': data.get('jenis_kelamin') or False,
                'no_hp':         (data.get('no_hp') or '').strip(),
                'alamat':        (data.get('alamat') or '').strip(),
            })

        # Cegah mengerjakan ulang sertifikasi yang sama
        done = Peserta.search([
            ('sertifikasi_id', '=', s.id),
            ('profil_id', '=', profil.id),
            ('state', '=', 'selesai'),
        ], limit=1)
        if done:
            return {
                'error': f'NIK {nik} sudah menyelesaikan ujian ini sebelumnya. '
                         f'Nilai: {done.nilai:.1f} — '
                         f'{"LULUS" if done.lulus else "TIDAK LULUS"}.'
            }

        Jawaban = request.env['digital_kamtibmas.sertifikasi.jawaban'].sudo()
        batas = timedelta(minutes=s.waktu_menit + GRACE_MENIT)

        # Satu percobaan per NIK: lanjutkan percobaan yang masih berjalan
        # (soal yang sama), jangan buat set soal baru (mencegah panen bank soal).
        peserta = Peserta.search([
            ('sertifikasi_id', '=', s.id),
            ('profil_id', '=', profil.id),
            ('state', '=', 'mengerjakan'),
        ], order='id desc', limit=1)
        if peserta and peserta.waktu_mulai and fields.Datetime.now() > peserta.waktu_mulai + batas:
            self._finalize(peserta, {})
            return {
                'error': f'Waktu ujian untuk NIK {nik} sudah habis. '
                         f'Nilai: {peserta.nilai:.1f} - '
                         f'{"LULUS" if peserta.lulus else "TIDAK LULUS"}.'
            }

        if not peserta:
            peserta = Peserta.create({
                'sertifikasi_id': s.id,
                'profil_id':      profil.id,
                'waktu_mulai':    fields.Datetime.now(),
                'state':          'mengerjakan',
            })
            all_soal = request.env['digital_kamtibmas.sertifikasi.soal'].sudo().search(
                [('active', '=', True), ('has_kunci', '=', True)])
            n = min(s.jumlah_soal, len(all_soal))
            for soal in random.sample(list(all_soal), n):
                Jawaban.create({'peserta_id': peserta.id, 'soal_id': soal.id})

        soal_list = []
        for i, jw in enumerate(peserta.jawaban_ids.sorted('id')):
            soal = jw.soal_id
            pilihan = [{'id': p.id, 'name': p.name}
                       for p in soal.pilihan_ids.sorted('sequence')]
            random.shuffle(pilihan)
            soal_list.append({
                'id':      soal.id,
                'no':      i + 1,
                'name':    soal.name,
                'pilihan': pilihan,
            })

        return {
            'peserta_id':      peserta.id,
            'nama':            nama,
            'waktu_menit':     s.waktu_menit,
            'nilai_kelulusan': s.nilai_kelulusan,
            'soal':            soal_list,
        }

    # ── API: submit jawaban ───────────────────────────────────────────────────

    @http.route('/sertifikasi/api/submit', type='jsonrpc', auth='public', csrf=False)
    def api_submit(self, token='', data=None, **kwargs):
        data = data or {}
        try:
            peserta_id   = int(data.get('peserta_id') or 0)
            jawaban_list = data.get('jawaban') or []
        except (ValueError, TypeError):
            return {'error': 'Data tidak valid'}

        Peserta = request.env['digital_kamtibmas.sertifikasi.peserta'].sudo()
        peserta = Peserta.browse(peserta_id)
        if not peserta.exists():
            return {'error': 'Data peserta tidak ditemukan'}
        if peserta.state == 'selesai':
            return {'error': 'Ujian sudah pernah disubmit'}

        if peserta.sertifikasi_id.access_token != (token or '').strip():
            return {'error': 'Token tidak cocok'}

        # Waktu pengerjaan dicek di server (+ toleransi jaringan)
        batas = timedelta(minutes=peserta.sertifikasi_id.waktu_menit + GRACE_MENIT)
        terlambat = bool(peserta.waktu_mulai and
                         fields.Datetime.now() > peserta.waktu_mulai + batas)
        pilih = {}
        if not terlambat:
            for j in jawaban_list:
                try:
                    pilih[int(j.get('soal_id') or 0)] = int(j.get('pilihan_id') or 0)
                except (ValueError, TypeError, AttributeError):
                    continue
        self._finalize(peserta, pilih)
        nilai_lulus = peserta.sertifikasi_id.nilai_kelulusan
        total_benar, total_soal, nilai, lulus = (
            peserta.total_benar, peserta.total_soal, peserta.nilai, peserta.lulus)

        return {
            'nama':        peserta.nama,
            'total_benar': total_benar,
            'total_soal':  total_soal,
            'nilai':       nilai,
            'nilai_lulus': nilai_lulus,
            'lulus':       lulus,
        }
