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

from gi.repository import Gtk

from gnome_appfolders_manager.localize import strip_underline, text
from gnome_appfolders_manager.ui.base import UIBase

SECTION_WINDOW_NAME = 'create folder'


class UICreateAppFolder(UIBase):
    def __init__(self, parent, settings, options, existing_folders):
        """Prepare the dialog"""
        logging.debug(f'{self.__class__.__name__} init')
        super().__init__(filename='create_appfolder.ui')
        # Initialize members
        self.parent = parent
        self.settings = settings
        self.options = options
        self.existing_folders = existing_folders
        self.folder_name = ''
        self.folder_title = ''
        # Load UI
        self.load_ui()
        # Complete initialization
        self.startup()

    def load_ui(self):
        """Load the interface UI"""
        logging.debug(f'{self.__class__.__name__} load UI')
        # Initialize titles and tooltips
        self.set_titles()
        # Initialize Gtk.HeaderBar
        self.ui.dialog.set_titlebar(self.ui.header_bar)
        # Set buttons as suggested
        self.set_buttons_style_suggested_action(
            buttons=[self.ui.button_ok])
        # Set various properties
        self.ui.dialog.set_transient_for(self.parent)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def startup(self):
        """Complete initialization"""
        logging.debug(f'{self.__class__.__name__} startup')
        self.ui.button_ok.grab_default()
        # Restore the saved size and position
        self.settings.restore_window_position(window=self.ui.dialog,
                                              section=SECTION_WINDOW_NAME)

    def show(self, name, title):
        """Show the dialog"""
        logging.debug(f'{self.__class__.__name__} show')
        # Set initial values
        self.folder_name = name
        self.ui.entry_name.set_text(name)
        self.folder_title = title
        self.ui.entry_title.set_text(title)
        # Change label from Create folder to Save if a folder name was provided
        if name:
            self.ui.entry_name.set_sensitive(False)
            self.ui.button_ok.set_related_action(self.ui.action_save)
            self.ui.button_ok.set_tooltip_text(
                strip_underline(self.ui.action_save.get_label()))
        response = self.ui.dialog.run()
        self.ui.dialog.hide()
        return response

    def destroy(self):
        """Destroy the dialog"""
        logging.debug(f'{self.__class__.__name__} destroy')
        self.settings.save_window_position(window=self.ui.dialog,
                                           section=SECTION_WINDOW_NAME)
        self.ui.dialog.destroy()
        self.ui.dialog = None

    def on_action_close_activate(self, widget):
        """Close the dialog"""
        self.ui.dialog.response(Gtk.ResponseType.CLOSE)

    def on_action_confirm_activate(self, widget):
        """Accept the folder name and title and close the dialog"""
        self.folder_name = self.ui.entry_name.get_text().strip()
        self.folder_title = self.ui.entry_title.get_text().strip()
        self.ui.dialog.response(Gtk.ResponseType.OK)

    def on_entry_name_changed(self, widget):
        """Check if the folder already exists"""
        name = self.ui.entry_name.get_text().strip()
        existing = (name in self.existing_folders and name != self.folder_name)
        # If a folder with the specified name already exists
        # then disable the creation and show an icon
        self.ui.action_create.set_sensitive(bool(name) and not existing)
        self.ui.entry_name.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY,
            'dialog-error' if existing else None)
        self.ui.entry_name.set_icon_tooltip_text(
            Gtk.EntryIconPosition.SECONDARY,
            text('A folder with that name already exists')
            if existing else None)
