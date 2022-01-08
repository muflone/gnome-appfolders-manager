##
#     Project: GNOME App Folders Manager
# Description: Manage GNOME Shell applications folders
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2016-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import gettext
import locale

import gnome_appfolders_manager.requires

from gnome_appfolders_manager.functions import store_message, text, _
from gnome_appfolders_manager.constants import DOMAIN_NAME, DIR_LOCALE

# Load domain for translation
for module in (gettext, locale):
    module.bindtextdomain(DOMAIN_NAME, DIR_LOCALE)
    module.textdomain(DOMAIN_NAME)

# Import some translated messages from GTK+ domain
for message in ('_Create', '_Remove', '_Save', '_Close', 'Show _Hidden Files',
                'A folder with that name already exists',
                'General', 'Preferences'):
    text(message=message, gtk30=True)
store_message('Folder Name:', '%s:' % text(message='Folder Name', gtk30=True))
store_message('_Files:', '_%s:' % text(message='Files', gtk30=True))
store_message('_Create Folder', text(message='Create Folder', gtk30=True))
store_message('_Properties', text(message='Properties', gtk30=True))

# With domain context
for message in ('_New', '_Delete', '_About', '_Close', '_Quit'):
    text(message=message, gtk30=True, context='Stock label')
store_message('Quit', text(message='_Quit', gtk30=True).replace('_', ''))
