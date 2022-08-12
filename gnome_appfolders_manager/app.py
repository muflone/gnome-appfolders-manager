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

from gi.repository import Gtk

from gnome_appfolders_manager.constants import APP_ID
from gnome_appfolders_manager.ui.main import UIMain


class Application(Gtk.Application):
    def __init__(self, options):
        """Prepare the GtkApplication"""
        super(self.__class__, self).__init__(application_id=APP_ID)
        self.options = options
        self.ui = None
        self.connect('activate', self.activate)
        self.connect('startup', self.startup)

    # noinspection PyUnusedLocal
    def startup(self, application):
        """Configure the application during the startup"""
        self.ui = UIMain(application=self,
                         options=self.options)

    # noinspection PyMethodOverriding
    def activate(self, application):
        """Execute the application"""
        self.ui.run()
