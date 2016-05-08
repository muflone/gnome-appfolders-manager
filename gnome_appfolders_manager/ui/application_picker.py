##
#     Project: GNOME App Folders Manager
# Description: Manage GNOME Shell applications folders
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2016 Fabio Castelli
#     License: GPL-2+
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
from gi.repository import Gio
from gi.repository import GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

import gnome_appfolders_manager.preferences as preferences
from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader
from gnome_appfolders_manager.functions import get_ui_file

from gnome_appfolders_manager.models.application_info import ApplicationInfo
from gnome_appfolders_manager.models.applications import ModelApplications

SECTION_WINDOW_NAME = 'application picker'


class UIApplicationPicker(object):
    def __init__(self, parent):
        """Prepare the application picker dialog"""
        # Load the user interface
        self.ui = GtkBuilderLoader(get_ui_file('application_picker.ui'))
        self.ui.dialog_application_picker.set_titlebar(self.ui.header_bar)
        # Prepares the models for the applications
        self.model_applications = ModelApplications(self.ui.store_applications)
        self.model_applications.model.set_sort_column_id(
            self.ui.column_applications.get_sort_column_id(),
            Gtk.SortType.ASCENDING)
        # Set various properties
        self.ui.dialog_application_picker.set_transient_for(parent)
        # Prepares the applications list
        for desktop_entry in Gio.app_info_get_all():
            try:
                icon_name = None
                if isinstance(desktop_entry.get_icon(), Gio.ThemedIcon):
                    icons = desktop_entry.get_icon().get_names()
                    icon_name = icons[0] if icons else None
                description = (desktop_entry.get_description()
                               if desktop_entry.get_description() else '')
                application = ApplicationInfo(desktop_entry.get_id(),
                                              desktop_entry.get_name(),
                                              description,
                                              icon_name)
                self.model_applications.add_data(application)
            except Exception as e:
                print 'error for', desktop_entry.get_id(), e
        # Connect signals from the glade file to the module functions
        self.ui.connect_signals(self)

    def show(self):
        """Show the application picker dialog"""
        self.ui.dialog_application_picker.run()
        self.ui.dialog_application_picker.hide()

    def destroy(self):
        """Destroy the application picker dialog"""
        self.ui.dialog_application_picker.destroy()
        self.ui.dialog_application_picker = None

    def on_action_close_activate(self, action):
        """Close the application picker dialog"""
        self.ui.dialog_application_picker.response(Gtk.ResponseType.CLOSE)
