from odoo import models, fields, api


class IntelkamResponWa(models.Model):
    _name = 'intelkam.respon.wa'
    _description = 'Respon WhatsApp Masuk'
    _order = 'tanggal desc, id desc'
    _rec_name = 'pengirim'

    group_id_wa = fields.Char('Group ID WA', readonly=True)
    wa_group_id = fields.Many2one('intelkam.wa.group', string='Group',
                                   compute='_compute_wa_group', store=True)
    pengirim = fields.Char('No. Pengirim', readonly=True)
    nama_pengirim = fields.Char('Nama Pengirim', readonly=True)
    pesan = fields.Text('Pesan', readonly=True)
    file_url = fields.Char('URL Media', readonly=True)
    mime_type = fields.Char('Tipe Media', readonly=True)
    has_media = fields.Boolean('Ada Media', compute='_compute_has_media', store=True)
    media_preview = fields.Html('Preview Media', compute='_compute_media_preview',
                                sanitize=False)
    tanggal = fields.Datetime('Waktu Masuk', readonly=True)
    wablas_message_id = fields.Char('Wablas Message ID', readonly=True)
    distribusi_id = fields.Many2one('intelkam.distribusi.info', string='Distribusi Terkait',
                                     compute='_compute_distribusi', store=True)
    raw_payload = fields.Text('Payload JSON', readonly=True)

    @api.depends('file_url', 'mime_type')
    def _compute_has_media(self):
        for rec in self:
            rec.has_media = bool(rec.file_url)

    @api.depends('file_url', 'mime_type')
    def _compute_media_preview(self):
        for rec in self:
            if not rec.file_url:
                rec.media_preview = False
                continue
            url = rec.file_url
            if rec.mime_type and 'image' in rec.mime_type:
                rec.media_preview = (
                    f'<img src="{url}" style="max-width:100%;max-height:400px;'
                    f'border-radius:8px;display:block;" alt="Gambar"/>'
                )
            else:
                rec.media_preview = (
                    f'<a href="{url}" target="_blank" rel="noopener noreferrer">'
                    f'Buka File</a>'
                )

    @api.depends('group_id_wa')
    def _compute_wa_group(self):
        for rec in self:
            raw = rec.group_id_wa or ''
            # Wablas kadang kirim group ID dengan suffix @g.us, strip sebelum lookup
            clean_id = raw.replace('@g.us', '').strip()
            if clean_id:
                grp = self.env['intelkam.wa.group'].search(
                    [('group_id', '=', clean_id)], limit=1)
                rec.wa_group_id = grp.id if grp else False
            else:
                rec.wa_group_id = False

    @api.depends('wa_group_id')
    def _compute_distribusi(self):
        for rec in self:
            if rec.wa_group_id:
                # Ambil distribusi terakhir yang pernah dikirim ke group ini (exclude draft)
                distribusi = self.env['intelkam.distribusi.info'].search(
                    [('group_ids', 'in', [rec.wa_group_id.id]),
                     ('state', 'not in', ('draft',))],
                    order='tanggal_kirim desc, id desc', limit=1)
                rec.distribusi_id = distribusi.id if distribusi else False
            else:
                rec.distribusi_id = False
