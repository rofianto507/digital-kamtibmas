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
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        def _read_b64(rel_path):
            path = os.path.join(base_dir, *rel_path.split('/'))
            if os.path.exists(path):
                with open(path, 'rb') as fh:
                    return base64.b64encode(fh.read()).decode('utf-8')
            return ''

        return {
            'doc_ids':        docids,
            'doc_model':      'digital_kamtibmas.sertifikasi.peserta',
            'docs':           docs,
            'template_b64':   _read_b64('static/img/template.jpeg'),
            'format_date_id': self._format_date_id,
        }
