PARAM_PUBLIC_BASE_URL = 'digital_kamtibmas.public_base_url'


def public_base_url(env):
    """Domain untuk link publik (sertifikasi, display antrian).

    Pakai parameter khusus, bukan web.base.url: Odoo menimpa web.base.url
    dengan domain tempat admin terakhir login, sehingga link bisa kembali ke
    domain lama (palembang.polisibaik.id). web.base.url hanya jadi cadangan.
    """
    icp = env['ir.config_parameter'].sudo()
    base = icp.get_param(PARAM_PUBLIC_BASE_URL) or icp.get_param('web.base.url', 'http://localhost:8069')
    return base.rstrip('/')
