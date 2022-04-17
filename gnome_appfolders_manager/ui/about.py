##
#     Project: GNOME App Folders Manager
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

from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from gnome_appfolders_manager.constants import (APP_NAME,
                                                APP_VERSION,
                                                APP_URL,
                                                APP_COPYRIGHT,
                                                APP_AUTHOR,
                                                APP_AUTHOR_EMAIL,
                                                FILE_CONTRIBUTORS,
                                                FILE_LICENSE,
                                                FILE_TRANSLATORS,
                                                FILE_RESOURCES,
                                                FILE_ICON)
from gnome_appfolders_manager.functions import readlines, _
from gnome_appfolders_manager.ui.base import UIBase


class UIAbout(UIBase):
    def __init__(self, parent):
        """Prepare the about dialog"""
        super().__init__(filename='about.ui')
        # Retrieve the translators list
        translators = []
        for line in readlines(FILE_TRANSLATORS, False):
            if ':' in line:
                line = line.split(':', 1)[1]
            line = line.replace('(at)', '@').strip()
            if line not in translators:
                translators.append(line)
        # Set various properties
        self.ui.dialog.set_program_name(APP_NAME)
        self.ui.dialog.set_version(_('Version {VERSION}').format(
            VERSION=APP_VERSION))
        self.ui.dialog.set_comments(
            _('Manage GNOME Shell applications folders'))
        self.ui.dialog.set_website(APP_URL)
        self.ui.dialog.set_copyright(APP_COPYRIGHT)
        # Prepare lists for authors and contributors
        authors = [f'{APP_AUTHOR} <{APP_AUTHOR_EMAIL}>']
        contributors = []
        for line in readlines(FILE_CONTRIBUTORS, False):
            contributors.append(line)
        if len(contributors) > 0:
            contributors.insert(0, _('Contributors:'))
            authors.extend(contributors)
        self.ui.dialog.set_authors(authors)
        self.ui.dialog.set_license(
            '\n'.join(readlines(FILE_LICENSE, True)))
        self.ui.dialog.set_translator_credits('\n'.join(translators))
        # Retrieve the external resources links
        for line in readlines(FILE_RESOURCES, False):
            resource_type, resource_url = line.split(':', 1)
            self.ui.dialog.add_credit_section(
                resource_type, (resource_url,))
        icon_logo = Pixbuf.new_from_file(str(FILE_ICON))
        self.ui.dialog.set_logo(icon_logo)
        self.ui.dialog.set_transient_for(parent)

    def show(self):
        """Show the About dialog"""
        self.ui.dialog.run()
        self.ui.dialog.hide()

    def destroy(self):
        """Destroy the About dialog"""
        self.ui.dialog.destroy()
        self.ui.dialog = None
