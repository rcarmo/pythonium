#!/usr/bin/env python

"""
by http://k0s.org/

WSGI app for FileServer

Reference:
- http://docs.webob.org/en/latest/file-example.html
"""

import mimetypes
import optparse
import os
import sys
from webob import Request, Response, exc
from wsgiref.simple_server import make_server

__all__ = ['get_mimetype', 'file_response', 'FileApp', 'DirectoryServer', 'main']

### classes for iterating over files

class FileIterable(object):
    def __init__(self, filename, start=None, stop=None):
        self.filename = filename
        self.start = start
        self.stop = stop
    def __iter__(self):
        return FileIterator(self.filename, self.start, self.stop)
class FileIterator(object):
    def __init__(self, filename, start, stop, chunk_size=4096):
        self.filename = filename
        self.chunk_size = chunk_size
        self.fileobj = open(self.filename, 'rb')
        if start:
            self.fileobj.seek(start)
        if stop is not None:
            self.length = stop - start
        else:
            self.length = None
    def __iter__(self):
        return self
    def next(self):
        if self.length is not None and self.length <= 0:
             raise StopIteration
        chunk = self.fileobj.read(self.chunk_size)
        if not chunk:
            raise StopIteration
        if self.length is not None:
            self.length -= len(chunk)
            if self.length < 0:
                # Chop off the extra:
                chunk = chunk[:self.length]
        return chunk
    __next__ = next # py3 compat


### attributes for serving static files

def get_mimetype(filename):
    type, encoding = mimetypes.guess_type(filename)
     # We'll ignore encoding, even though we shouldn't really
    return type or 'application/octet-stream'

def file_response(filename):
    """return a webob response object appropriate to a file name"""
    res = Response(content_type=get_mimetype(filename),
                   conditional_response=True)
    res.app_iter = FileIterable(filename)
    res.content_length = os.path.getsize(filename)
    res.last_modified = os.path.getmtime(filename)
    res.etag = '%s-%s-%s' % (os.path.getmtime(filename),
                             os.path.getsize(filename), hash(filename))
    return res

class FileApp(object):
    """
    serve static files
    """

    def __init__(self, filename):
        self.filename = filename

    def __call__(self, environ, start_response):
        res = file_response(self.filename)
        return res(environ, start_response)


### class for serving directory indices

class DirectoryServer(object):

    def __init__(self, directory, sort=True):
        assert os.path.exists(directory), "'%s' does not exist" % directory
        assert os.path.isdir(directory), "'%s' is not a directory" % directory
        self.directory = self.normpath(directory)
        self.sort = sort

    @staticmethod
    def normpath(path):
        return os.path.normcase(os.path.abspath(path))

    def check_path(self, path):
        """
        if under the root directory, returns the full path
        otherwise, returns None
        """
        path = self.normpath(path)
        if path == self.directory or path.startswith(self.directory + os.path.sep):
            return path

    def index(self, directory):
        """
        generate a directory listing for a given directory
        """
        parts = ['<html><head><title>Simple Index</title></head><body>']
        listings = os.listdir(directory)
        if self.sort:
            listings.sort()
        listings = [(os.path.isdir(os.path.join(directory, entry)) and entry + '/' or entry, entry)
                    for entry in listings]
        for link, entry in listings:
            parts.append('<a href="%s">%s</a><br/>' % (link, entry))
        parts.append('</body></html>')
        return '\n'.join(parts)

    def __call__(self, environ, start_response):
        request = Request(environ)
        # TODO method_not_allowed: Allow: GET, HEAD
        path_info = request.path_info
        if not path_info:
            response = exc.HTTPMovedPermanently(add_slash=True)
            return response(environ, start_response)
        full = self.check_path(os.path.join(self.directory, path_info.strip('/')))

        if full is None:
            # Out of bounds
            return exc.HTTPNotFound()(environ, start_response)
        if not os.path.exists(full):
            return exc.HTTPNotFound()(environ, start_response)

        if os.path.isdir(full):
            # serve directory index
            if not path_info.endswith('/'):
                response = exc.HTTPMovedPermanently(add_slash=True)
                return response(environ, start_response)
            index = self.index(full)
            response = Response(index, content_type='text/html')
            return response(environ, start_response)

        # serve file
        if path_info.endswith('/'):
            # we create the `full` filename above by stripping off
            # '/' from both sides; so we correct here
            return exc.HTTPNotFound()(environ, start_response)
        response = file_response(full)
        return response(environ, start_response)

def main(args=sys.argv[1:]):

    # parse command line arguments
    usage = '%prog [options] directory'
    class PlainDescriptionFormatter(optparse.IndentedHelpFormatter):
        """description formatter"""
        def format_description(self, description):
            if description:
                return description + '\n'
            else:
                return ''
    parser = optparse.OptionParser(usage=usage, description=__doc__, formatter=PlainDescriptionFormatter())
    parser.add_option('-p', '--port', dest='port',
                      type='int', default=9999,
                      help='port [DEFAULT: %default]')
    parser.add_option('-H', '--host', dest='host', default='0.0.0.0',
                      help='host [DEFAULT: %default]')
    options, args = parser.parse_args(args)

    # get the directory
    if not len(args) == 1:
        parser.print_help()
        sys.exit(1)
    directory = args[0]
    if not os.path.exists(directory):
        parser.error("'%s' not found" % directory)
    if not os.path.isdir(directory):
        parser.error("'%s' not a directory" % directory)

    # serve
    app = DirectoryServer(directory)
    try:
        print('http://%s:%s/' % (options.host, options.port))
        make_server(options.host, options.port, app).serve_forever()
    except KeyboardInterrupt as ki:
        print("Cio, baby!")
    except BaseException as e:
        sys.exit("Problem initializing server: %s" % e)

if __name__ == '__main__':
    main()
