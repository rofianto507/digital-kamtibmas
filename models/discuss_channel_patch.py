from odoo import models, api


class DiscussChannelMasyarakat(models.Model):
    _inherit = 'discuss.channel'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, **kwargs):
        """Sembunyikan channel tipe 'chat' (OdooBot, DM) untuk user masyarakat."""
        if self.env.user.has_group('digital_kamtibmas.group_masyarakat'):
            domain = list(domain) + [('channel_type', '!=', 'chat')]
        return super()._search(domain, offset=offset, limit=limit, order=order, **kwargs)
