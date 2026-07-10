from odoo import models, fields


class YangTerlibat(models.Model):
    _name = 'digital_kamtibmas.yang_terlibat'
    _description = 'Master Data Yang Terlibat Laka'
    _rec_name = 'nama'
    _order = 'nama asc'

    nama = fields.Char('Nama', required=True)
    keterangan = fields.Char('Keterangan')
