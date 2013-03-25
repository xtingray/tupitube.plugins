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

import inkex, sys, urllib, urllib2, webbrowser
sys.path.append('/usr/share/inkscape/extensions')

import gettext
_ = gettext.gettext
reload(sys)
sys.setdefaultencoding("utf-8")

class PostAtTupitube(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('', '--tupiversion', action='store', type='string', dest='version', default='1.0')
        self.OptionParser.add_option('', '--title', action='store', type='string', dest='title', default='My Picture', help='Works Title') 
        self.OptionParser.add_option('', '--tags', action='store', type='string', dest='tags', default='#tupitube #svg #desktop', help='Works Tags')
        self.OptionParser.add_option('', '--description', action='store', type='string', dest='description', default='Just a little taste of my style :)', help='Works Description')

    def effect(self):
        tupiVersion = self.options.version
        workTitle = self.options.title
        workTags = self.options.tags
        workDescription = self.options.description
        self.code = open(self.svg_file, 'r').read()

        params = urllib.urlencode(dict(version = tupiVersion, title = workTitle, tags = workTags, description = workDescription, svg = self.code))
        f = urllib2.urlopen('http://tupitu.be/svg/upload/file', params)
        url = f.read()
        f.close()

        webbrowser.open(url)

        sys.exit()

effect = PostAtTupitube()
effect.affect()
