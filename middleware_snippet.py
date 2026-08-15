"""
REPLACE your existing PrefixMiddleware class with this version.
It fixes the case where visiting exactly /krecomstore (no trailing slash/path)
left PATH_INFO as an empty string, which Flask's router does not match to '/'.
"""
from app import app


class PrefixMiddleware:
    def __init__(self, wsgi_app, prefix=''):
        self.wsgi_app = wsgi_app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            if environ['PATH_INFO'] == '':
                environ['PATH_INFO'] = '/'
            environ['SCRIPT_NAME'] = self.prefix
            return self.wsgi_app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return [b'This path is not accessible under this prefix.']


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/krecomstore')