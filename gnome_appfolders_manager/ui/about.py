##
#     Project: GNOME App Folders Manager
# Description: Manage GNOME Shell applications folders
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
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

from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader
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
from gnome_appfolders_manager.functions import readlines, get_ui_file, _


class UIAbout(object):
    def __init__(self, parent):
        """Prepare the about dialog"""
        # Retrieve the translators list
        translators = []
        for line in readlines(FILE_TRANSLATORS, False):
            if ':' in line:
                line = line.split(':', 1)[1]
            line = line.replace('(at)', '@').strip()
            if line not in translators:
                translators.append(line)
        # Load the user interface
        self.ui = GtkBuilderLoader(get_ui_file('about.ui'))
        # Set various properties
        self.ui.dialog_about.set_program_name(APP_NAME)
        self.ui.dialog_about.set_version(_('Version {VERSION}').format(
            VERSION=APP_VERSION))
        self.ui.dialog_about.set_comments(
            _('Manage GNOME Shell applications folders'))
        self.ui.dialog_about.set_website(APP_URL)
        self.ui.dialog_about.set_copyright(APP_COPYRIGHT)
        # Prepare lists for authors and contributors
        authors = [f'{APP_AUTHOR} <{APP_AUTHOR_EMAIL}>']
        contributors = []
        for line in readlines(FILE_CONTRIBUTORS, False):
            contributors.append(line)
        if len(contributors) > 0:
            contributors.insert(0, _('Contributors:'))
            authors.extend(contributors)
        self.ui.dialog_about.set_authors(authors)
        self.ui.dialog_about.set_license(
            '\n'.join(readlines(FILE_LICENSE, True)))
        self.ui.dialog_about.set_translator_credits('\n'.join(translators))
        # Retrieve the external resources links
        # only for GTK+ 3.6.0 and higher
        if not Gtk.check_version(3, 6, 0):
            for line in readlines(FILE_RESOURCES, False):
                resource_type, resource_url = line.split(':', 1)
                self.ui.dialog_about.add_credit_section(
                    resource_type, (resource_url,))
        icon_logo = Pixbuf.new_from_file(str(FILE_ICON))
        self.ui.dialog_about.set_logo(icon_logo)
        self.ui.dialog_about.set_transient_for(parent)

    def show(self):
        """Show the About dialog"""
        self.ui.dialog_about.run()
        self.ui.dialog_about.hide()

    def destroy(self):
        """Destroy the About dialog"""
        self.ui.dialog_about.destroy()
        self.ui.dialog_about = None
