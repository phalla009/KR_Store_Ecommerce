"""
ADD THIS RIGHT AFTER:
    app = Flask(__name__)
    app.config.from_object('config')
    app.secret_key = os.urandom(24)
    mail = Mail(app)

(i.e. right before your `products = [...]` list)
"""
from app import app


class PrefixMiddleware:
    def __init__(self, wsgi_app, prefix=''):
        self.wsgi_app = wsgi_app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.wsgi_app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return [b'This path is not accessible under this prefix.']


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/krecomstore')
