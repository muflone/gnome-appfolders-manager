##
#     Project: GNOME AppFolders Manager
# Description: Manage GNOME Shell applications folders
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2016-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import gettext
import locale

from gnome_appfolders_manager.constants import APP_DOMAIN, DIR_LOCALE
from gnome_appfolders_manager.localize import (store_message,
                                               strip_colon,
                                               strip_underline,
                                               text)


# Load domain for translation
for module in (gettext, locale):
    module.bindtextdomain(APP_DOMAIN, DIR_LOCALE)
    module.textdomain(APP_DOMAIN)

# Import some translated messages from GTK+ domain
for message in ('About', 'A folder with that name already exists',
                '_Close', '_Create', 'Create Folder', 'Files', 'General',
                'Properties', '_Remove', '_Save', 'Search',
                'Show _Hidden Files'):
    store_message(strip_colon(strip_underline(message)),
                  strip_colon(strip_underline(text(message=message,
                                                   gtk30=True))))

# Import some translated messages from GTK+ domain and context
for message in ('_Delete', '_New', '_Quit'):
    store_message(strip_colon(strip_underline(message)),
                  strip_colon(strip_underline(text(message=message,
                                                   gtk30=True,
                                                   context='Stock label'))))

# Import some variations
store_message('Files:', '%s:' % text(message='Files',
                                     gtk30=True))
store_message('Folder Name:', '%s:' % text(message='Folder Name',
                                           gtk30=True))
store_message('Folders:', '%s:' % text(message='Folders',
                                       gtk30=False))
