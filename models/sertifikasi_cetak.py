import base64
import os
from odoo import models, api


class SertifikasiCetakReport(models.AbstractModel):
    _name = 'report.digital_kamtibmas.sertifikasi_cetak_template'
    _description = 'Report Sertifikat Kelulusan'

    _MONTHS_ID = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember',
    ]

    def _format_date_id(self, dt):
        if not dt:
            return '-'
        local_dt = dt
        try:
            import pytz
            tz = pytz.timezone('Asia/Jakarta')
            local_dt = dt.astimezone(tz)
        except Exception:
            pass
        return f"{local_dt.day} {self._MONTHS_ID[local_dt.month - 1]} {local_dt.year}"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['digital_kamtibmas.sertifikasi.peserta'].browse(docids)
        img_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'static', 'img', 'logo_app.png',
        )
        logo_b64 = ''
        if os.path.exists(img_path):
            with open(img_path, 'rb') as fh:
                logo_b64 = base64.b64encode(fh.read()).decode('utf-8')
        return {
            'doc_ids': docids,
            'doc_model': 'digital_kamtibmas.sertifikasi.peserta',
            'docs': docs,
            'logo_b64': logo_b64,
            'format_date_id': self._format_date_id,
        }
