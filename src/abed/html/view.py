"""
This starts up a simple http server and launches the browser

"""

import errno
import os
import SimpleHTTPServer
import SocketServer
import webbrowser

from socket import error as socket_error

from abed.conf import settings
from abed.utils import warning

def view_html():
    port = settings.HTML_PORT
    os.chdir('%s%s%s' % (settings.OUTPUT_DIR, os.sep, 'html'))
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    while True:
        try:
            httpd = SocketServer.TCPServer(('', port), handler)
            break
        except socket_error as err:
            if not err.errno == errno.EADDRINUSE:
                raise err
            warning("Port already in use, trying %i" % (port + 1))
            port += 1

    webbrowser.open('http://localhost:%i' % port, autoraise=True)
    httpd.serve_forever()

