#!/usr/bin/python
# -*- coding: utf-8 -*-

###########################################################################
#   Project TUPI: Magia 2D                                                #
#   Project Contact: info@maefloresta.com                                 #
#   Project Website: http://www.maefloresta.com                           #
#   Project Leader: Gustav Gonzalez <info@maefloresta.com>                #
#                                                                         #
#   Developers:                                                           #
#     Gustavo Gonzalez @xtingray                                          #
#     Andres Calderon @andresfcalderon                                    #
#     Antonio Vanegas @hpsaturn                                           #
#                                                                         #
#   Copyright (C) 2010 Gustav Gonzalez - http://www.maefloresta.com       #
#   License:                                                              #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 3 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#   This program is distributed in the hope that it will be useful,       #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#   GNU General Public License for more details.                          #
#                                                                         #
#   You should have received a copy of the GNU General Public License     #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>. #
###########################################################################

import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib
import urllib2
import webbrowser

from gimpfu import *

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return
    
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return
    
    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.  
        parts = []
        part_boundary = '--' + self.boundary
        
        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )
        
        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )
        
        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)

def plugin_main(timg, tdrawable, title, topics, description):
    tf = tempfile.NamedTemporaryFile() 
    xcf = tf.name+".xcf"
    pdb.gimp_file_save(timg, tdrawable, xcf, xcf)
    version = "1.0"

    # Create the form with the basic fields
    form = MultiPartForm()
    form.add_field('title', title)
    form.add_field('tags', topics)
    form.add_field('description', description)
    form.add_file('xcf', xcf, fileHandle=StringIO('Gimp File'))

    # Build the request
    request = urllib2.Request('http://tupitu.be/g/upload/file')
    request.add_header('User-agent', 'Tupitu.be Python Client')
    body = str(form)
    request.add_header('Content-type', form.get_content_type())
    request.add_header('Content-length', len(body))
    request.add_data(body)

    f = urllib2.urlopen(request)
    url = f.read()
    f.close()

    print "URL: " + url

    if url.startswith('http:\/\/'):
       webbrowser.open(url)

register(
        "tupitube",
        "Posts this image at http://tupitu.be",
        "Posts this image at http://tupitu.be",
        "Gustav Gonzalez",
        "Gustav Gonzalez",
        "2010",
        "<Image>/Tools/Post at tupitu.be",
        "RGB*, GRAY*",
        [
                (PF_STRING, "title", "Title", "My Picture"),
                (PF_STRING, "topics", "Topics", "#tupitube #gimp #desktop"),
                (PF_STRING, "description", "Description", "Just a little taste of my style :)"),
        ],
        [],
        plugin_main)

main()
