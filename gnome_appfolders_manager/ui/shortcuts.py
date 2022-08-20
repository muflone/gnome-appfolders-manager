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

import logging

from gnome_appfolders_manager.ui.base import UIBase


class UIShortcuts(UIBase):
    def __init__(self, parent, settings, options):
        """Prepare the dialog"""
        logging.debug(f'{self.__class__.__name__} init')
        super().__init__(filename='shortcuts.ui')
        # Initialize members
        self.settings = settings
        self.options = options
        # Initialize titles and tooltips
        self.set_titles()
        # Load the user interface
        self.ui.shortcuts.set_transient_for(parent)

    def show(self):
        """Show the dialog"""
        logging.debug(f'{self.__class__.__name__} show')
        self.ui.shortcuts.show()

    def destroy(self):
        """Destroy the dialog"""
        logging.debug(f'{self.__class__.__name__} destroy')
        self.ui.shortcuts.destroy()
        self.ui.shortcuts = None
