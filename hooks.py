import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Copy master data wilayah Palembang dari petadigi jika tersedia."""
    if not env['ir.model'].search([('model', '=', 'petadigi.kabupaten')], limit=1):
        _logger.info('digital_kamtibmas: petadigi tidak tersedia, skip copy data wilayah.')
        return

    _logger.info('digital_kamtibmas: mulai copy data wilayah Palembang dari petadigi...')

    Kab    = env['digital_kamtibmas.kabupaten']
    Kec    = env['digital_kamtibmas.kecamatan']
    Desa   = env['digital_kamtibmas.desa']
    Polsek = env['digital_kamtibmas.polsek']

    # ── Kabupaten ─────────────────────────────────────────────────────────────
    kabs_src = env['petadigi.kabupaten'].search(
        [('polres_id.name', 'ilike', 'Palembang')]
    )
    kab_map = {}  # petadigi id → dkm id
    for src in kabs_src:
        rec = Kab.search([('name', '=', src.name)], limit=1)
        if not rec:
            rec = Kab.create({
                'name':     src.name,
                'code':     src.code or '',
                'type':     src.type or False,
                'geometry': src.geometry or False,
            })
        kab_map[src.id] = rec.id

    # ── Kecamatan ─────────────────────────────────────────────────────────────
    kecs_src = env['petadigi.kecamatan'].search(
        [('kabupaten_id', 'in', list(kab_map))]
    )
    kec_map = {}
    for src in kecs_src:
        kab_dst = kab_map.get(src.kabupaten_id.id)
        rec = Kec.search(
            [('name', '=', src.name), ('kabupaten_id', '=', kab_dst)], limit=1
        )
        if not rec:
            rec = Kec.create({
                'name':         src.name,
                'code':         src.code or '',
                'kabupaten_id': kab_dst,
                'geometry':     src.geometry or False,
            })
        kec_map[src.id] = rec.id

    # ── Desa ──────────────────────────────────────────────────────────────────
    desas_src = env['petadigi.desa'].search(
        [('kecamatan_id', 'in', list(kec_map))]
    )
    desa_count = 0
    for src in desas_src:
        kec_dst = kec_map.get(src.kecamatan_id.id)
        if not Desa.search(
            [('name', '=', src.name), ('kecamatan_id', '=', kec_dst)], limit=1
        ):
            Desa.create({
                'name':         src.name,
                'code':         src.code or '',
                'type':         src.type or False,
                'kecamatan_id': kec_dst,
                'geometry':     src.geometry or False,
            })
            desa_count += 1

    # ── Polsek ────────────────────────────────────────────────────────────────
    polseks_src = env['petadigi.polsek'].search(
        [('polres_id.name', 'ilike', 'Palembang')]
    )
    polsek_count = 0
    for src in polseks_src:
        if not Polsek.search([('name', '=', src.name)], limit=1):
            # Cari kecamatan pertama yang terkait polsek ini
            kec_dst = None
            src_kecs = getattr(src, 'kecamatan_ids', None)
            if src_kecs:
                kec_dst = kec_map.get(src_kecs[0].id)
            Polsek.create({
                'name':         src.name,
                'kecamatan_id': kec_dst,
            })
            polsek_count += 1

    _logger.info(
        'digital_kamtibmas: selesai copy — %d kabupaten, %d kecamatan, '
        '%d desa, %d polsek.',
        len(kab_map), len(kec_map), desa_count, polsek_count,
    )
