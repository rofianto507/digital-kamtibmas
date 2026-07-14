import logging
_logger = logging.getLogger(__name__)

_ALLOWED_ORIGINS = {
    'http://localhost:5500',
    'http://127.0.0.1:5500',
}

_CORS_RESPONSE_HEADERS = [
    ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
    ('Access-Control-Allow-Headers',
     'Content-Type, Authorization, X-Requested-With, Origin, X-Odoo-Database'),
    ('Access-Control-Max-Age', '86400'),
]


def apply():
    """
    Patch odoo.http.Application.__call__ to add CORS headers for allowed
    dev origins.  Patching the CLASS (not the instance) works because the
    ThreadedServer already holds a reference to the root Application()
    instance — swapping odoo.http.root would have no effect.
    """
    import odoo.http as odoo_http

    Application = odoo_http.Application

    if getattr(Application, '_cors_patched', False):
        return

    _original_call = Application.__call__

    def _cors_call(self, environ, start_response):
        origin = environ.get('HTTP_ORIGIN', '')
        allowed = origin in _ALLOWED_ORIGINS

        # Intercept CORS preflight before Odoo routing
        if environ.get('REQUEST_METHOD') == 'OPTIONS' and allowed:
            headers = [
                ('Access-Control-Allow-Origin', origin),
                ('Access-Control-Allow-Credentials', 'true'),
                *_CORS_RESPONSE_HEADERS,
                ('Content-Length', '0'),
                ('Content-Type', 'text/plain'),
            ]
            start_response('200 OK', headers)
            return [b'']

        # Inject CORS headers into every response from allowed origins
        def _cors_start_response(status, headers, exc_info=None):
            if allowed:
                headers = list(headers)
                headers.append(('Access-Control-Allow-Origin', origin))
                headers.append(('Access-Control-Allow-Credentials', 'true'))
            return start_response(status, headers, exc_info)

        return _original_call(self, environ, _cors_start_response)

    Application.__call__ = _cors_call
    Application._cors_patched = True

    _logger.info(
        'digital_kamtibmas: CORS patch applied for origins: %s',
        _ALLOWED_ORIGINS,
    )
