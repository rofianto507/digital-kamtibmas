from odoo import models, fields, api, exceptions
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

# Wablas status → status log Odoo
_WABLAS_STATUS_MAP = {
    'pending': 'pending',
    'process': 'pending',
    'sent': 'delivered',
    'delivered': 'delivered',
    'read': 'read',
    'failed': 'failed',
    'cancel': 'failed',
}


class IntelkamDistribusiInfo(models.Model):
    _name = 'intelkam.distribusi.info'
    _description = 'Distribusi Informasi Intelkam'
    _order = 'tanggal_kirim desc, id desc'
    _rec_name = 'perihal'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char('Nomor', readonly=True, default='/', copy=False, tracking=True)
    perihal = fields.Char('Perihal', required=True, tracking=True)
    isi_instruksi = fields.Text('Isi Instruksi / Pesan', required=True)
    group_ids = fields.Many2many(
        'intelkam.wa.group',
        'intelkam_distribusi_group_rel',
        'distribusi_id', 'group_id_rel',
        string='Tujuan Group WhatsApp',
        required=True,
    )
    pengirim_id = fields.Many2one('res.users', string='Pengirim', default=lambda s: s.env.user,
                                   tracking=True)
    tanggal_kirim = fields.Datetime('Tanggal Kirim', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('mengirim', 'Mengirim'),
        ('terkirim', 'Terkirim'),
        ('gagal', 'Gagal'),
    ], string='Status', default='draft', tracking=True, readonly=True)
    log_ids = fields.One2many('intelkam.distribusi.log', 'distribusi_id', string='Log Pengiriman')
    jumlah_terkirim = fields.Integer('Berhasil', compute='_compute_log_summary', store=False)
    jumlah_gagal = fields.Integer('Gagal', compute='_compute_log_summary', store=False)
    jumlah_pending = fields.Integer('Pending', compute='_compute_log_summary', store=False)

    @api.depends('log_ids.status')
    def _compute_log_summary(self):
        for rec in self:
            rec.jumlah_terkirim = len(rec.log_ids.filtered(lambda l: l.status in ('delivered', 'read')))
            rec.jumlah_pending = len(rec.log_ids.filtered(lambda l: l.status == 'pending'))
            rec.jumlah_gagal = len(rec.log_ids.filtered(lambda l: l.status == 'failed'))

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].next_by_code('intelkam.distribusi.info')
        for vals in vals_list:
            if vals.get('code', '/') == '/':
                vals['code'] = seq
        return super().create(vals_list)

    def action_kirim(self):
        self.ensure_one()
        if self.state not in ('draft', 'gagal'):
            raise exceptions.UserError('Hanya distribusi dengan status Draft atau Gagal yang dapat dikirim.')
        if not self.group_ids:
            raise exceptions.UserError('Pilih minimal satu group tujuan.')

        config = self.env['intelkam.wa.config'].get_config()
        self.write({'state': 'mengirim', 'tanggal_kirim': fields.Datetime.now()})
        self.env.cr.commit()

        # Hapus log lama jika retry
        self.log_ids.unlink()

        n_antri = 0
        n_gagal = 0

        for group in self.group_ids:
            result = config.send_message(
                phone=group.group_id,
                message=self._format_pesan(group),
                is_group=True,
            )
            # Wablas 'pending' = pesan sudah diantrekan, bukan gagal
            log_status = _WABLAS_STATUS_MAP.get(result.get('wablas_status', ''), 'pending') \
                if result['success'] else 'failed'

            self.env['intelkam.distribusi.log'].create({
                'distribusi_id': self.id,
                'group_id': group.id,
                'wablas_message_id': result['message_id'],
                'status': log_status,
                'error_message': result['error'],
            })
            if result['success']:
                n_antri += 1
            else:
                n_gagal += 1

        # Ada yg berhasil diantrekan Wablas → terkirim
        new_state = 'terkirim' if n_antri > 0 else 'gagal'
        self.write({'state': new_state})

        notif_type = 'success' if new_state == 'terkirim' else 'danger'
        msg = f'Pesan diantrekan ke {n_antri} group (menunggu konfirmasi Wablas)'
        if n_gagal:
            msg += f', gagal {n_gagal} group.'
        else:
            msg += '.'

        # Reload form setelah kirim agar state & button langsung terupdate di browser
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Distribusi Informasi',
                'message': msg,
                'type': notif_type,
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': self._name,
                    'res_id': self.id,
                    'view_mode': 'form',
                    'views': [[False, 'form']],
                    'target': 'current',
                },
            }
        }

    def action_refresh_status(self):
        """Polling status pengiriman ke Wablas untuk log yang masih pending."""
        self.ensure_one()
        config = self.env['intelkam.wa.config'].get_config()
        pending_logs = self.log_ids.filtered(
            lambda l: l.status == 'pending' and l.wablas_message_id
        )
        if not pending_logs:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Refresh Status',
                    'message': 'Tidak ada log pending yang perlu direfresh.',
                    'type': 'info', 'sticky': False,
                }
            }
        updated = 0
        for log in pending_logs:
            wablas_status = config.check_message_status(log.wablas_message_id)
            if wablas_status and wablas_status != 'pending':
                new_status = _WABLAS_STATUS_MAP.get(wablas_status, log.status)
                if new_status != log.status:
                    log.write({'status': new_status})
                    updated += 1
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Refresh Status',
                'message': f'{updated} status log diperbarui dari Wablas.',
                'type': 'success' if updated else 'info',
                'sticky': False,
            }
        }

    def _format_pesan(self, group):
        lines = [
            '*[DISTRIBUSI INFORMASI]*',
            f'*Nomor  :* {self.code}',
            f'*Perihal:* {self.perihal}',
            f'*Kepada :* {group.name}',
            '---',
            self.isi_instruksi,
            '---',
            f'_{self.pengirim_id.name} — {datetime.now().strftime("%d/%m/%Y %H:%M")}_',
        ]
        return '\n'.join(lines)

    def web_read(self, specification):
        """Auto-refresh status pending saat form distribusi dibuka."""
        if len(self) == 1 and self.state in ('mengirim', 'terkirim'):
            self._auto_refresh_pending()
        return super().web_read(specification)

    def _auto_refresh_pending(self):
        pending_logs = self.log_ids.filtered(
            lambda l: l.status == 'pending' and l.wablas_message_id
        )
        if not pending_logs:
            return
        try:
            config = self.env['intelkam.wa.config'].sudo().search(
                [('active', '=', True)], limit=1
            )
            if not config:
                return
            for log in pending_logs:
                wablas_status = config.check_message_status(log.wablas_message_id)
                if wablas_status and wablas_status != 'pending':
                    new_status = _WABLAS_STATUS_MAP.get(wablas_status, log.status)
                    if new_status != log.status:
                        log.write({'status': new_status})
        except Exception as e:
            _logger.warning('Auto-refresh status error: %s', e)

    def action_reset_draft(self):
        self.write({'state': 'draft'})


class IntelkamDistribusiLog(models.Model):
    _name = 'intelkam.distribusi.log'
    _description = 'Log Pengiriman Distribusi Informasi'
    _order = 'id desc'

    distribusi_id = fields.Many2one('intelkam.distribusi.info', string='Distribusi',
                                     required=True, ondelete='cascade')
    group_id = fields.Many2one('intelkam.wa.group', string='Group', required=True)
    wablas_message_id = fields.Char('Wablas Message ID')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('delivered', 'Terkirim'),
        ('read', 'Dibaca'),
        ('failed', 'Gagal'),
    ], string='Status', default='pending')
    error_message = fields.Text('Pesan Error')
    tanggal = fields.Datetime('Waktu', default=fields.Datetime.now)
