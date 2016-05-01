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
from gi.repository import Gdk
from gi.repository import Gio

from gnome_appfolders_manager.constants import APP_ID, DIR_SETTINGS
from gnome_appfolders_manager.functions import get_ui_file
from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader

from gnome_appfolders_manager.ui.main import UIMain


class Application(Gtk.Application):
    def __init__(self):
        """Create the application object"""
        super(self.__class__, self).__init__(application_id=APP_ID)
        self.connect("activate", self.activate)
        self.connect('startup', self.startup)

    def startup(self, application):
        """Configure the application during the startup"""
        self.ui = UIMain(self)
        # Add the about action to the app menu
        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.on_app_about_activate)
        self.add_action(action)
        # Add the quit action to the app menu
        action = Gio.SimpleAction(name="quit")
        action.connect("activate", self.on_app_quit_activate)
        self.add_action(action)
        # Add the app menu
        builder_appmenu = GtkBuilderLoader(get_ui_file('appmenu.ui'))
        self.set_app_menu(builder_appmenu.app_menu)

    def activate(self, application):
        """Execute the application"""
        self.ui.run()

    def on_app_about_activate(self, action, data):
        """Show the about dialog from the app menu"""
        self.ui.on_action_about_activate(action)

    def on_app_quit_activate(self, action, data):
        """Quit the application from the app menu"""
        self.ui.on_action_quit_activate(action)
