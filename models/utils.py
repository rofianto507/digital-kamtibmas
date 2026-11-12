PARAM_PUBLIC_BASE_URL = 'digital_kamtibmas.public_base_url'


def today_local(env):
    """Tanggal hari ini menurut zona waktu pengguna (default WIB).

    `fields.Date.today` memakai tanggal UTC sehingga antara 00.00-07.00 WIB
    hasilnya tertinggal satu hari.
    """
    import pytz
    from datetime import datetime
    tz = pytz.timezone(env.context.get('tz') or env.user.tz or 'Asia/Jakarta')
    return datetime.now(pytz.utc).astimezone(tz).date()


def now_local(env):
    """Waktu sekarang menurut zona waktu pengguna (default WIB), tanpa tzinfo."""
    import pytz
    from datetime import datetime
    tz = pytz.timezone(env.context.get('tz') or env.user.tz or 'Asia/Jakarta')
    return datetime.now(pytz.utc).astimezone(tz).replace(tzinfo=None)


def public_base_url(env):
    """Domain untuk link publik (sertifikasi, display antrian).

    Pakai parameter khusus, bukan web.base.url: Odoo menimpa web.base.url
    dengan domain tempat admin terakhir login, sehingga link bisa kembali ke
    domain lama (palembang.polisibaik.id). web.base.url hanya jadi cadangan.
    """
    icp = env['ir.config_parameter'].sudo()
    base = icp.get_param(PARAM_PUBLIC_BASE_URL) or icp.get_param('web.base.url', 'http://localhost:8069')
    return base.rstrip('/')
