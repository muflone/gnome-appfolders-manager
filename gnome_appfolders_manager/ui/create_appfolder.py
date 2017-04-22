##
#     Project: GNOME App Folders Manager
# Description: Manage GNOME Shell applications folders
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2016-2017 Fabio Castelli
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

import gnome_appfolders_manager.settings as settings
import gnome_appfolders_manager.preferences as preferences
from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader
from gnome_appfolders_manager.functions import (
    get_ui_file, set_style_suggested_action, _, text)

SECTION_WINDOW_NAME = 'create folder'


class UICreateAppFolder(object):
    def __init__(self, parent, existing_folders):
        """Prepare the AppFolder creation dialog"""
        # Load the user interface
        self.ui = GtkBuilderLoader(get_ui_file('create_appfolder.ui'))
        self.ui.dialog_create_appfolder.set_titlebar(self.ui.header_bar)
        # Initialize actions
        for widget in self.ui.get_objects_by_type(Gtk.Action):
            # Connect the actions accelerators
            widget.connect_accelerator()
            # Set labels
            label = widget.get_label()
            if not label:
                label = widget.get_short_label()
            widget.set_short_label(text(label))
            widget.set_label(text(label))
        # Initialize labels
        for widget in self.ui.get_objects_by_type(Gtk.Label):
            widget.set_label(text(widget.get_label()))
        # Initialize tooltips
        for widget in self.ui.get_objects_by_type(Gtk.Button):
            action = widget.get_related_action()
            if action:
                widget.set_tooltip_text(action.get_label().replace('_', ''))
        # Set various properties
        self.ui.dialog_create_appfolder.set_transient_for(parent)
        set_style_suggested_action(self.ui.button_ok)
        self.existing_folders = existing_folders
        self.ui.button_ok.grab_default()
        self.folder_name = ''
        self.folder_title = ''
        # Connect signals from the glade file to the module functions
        self.ui.connect_signals(self)

    def show(self, name, title):
        """Show the dialog"""
        settings.positions.restore_window_position(
            self.ui.dialog_create_appfolder, SECTION_WINDOW_NAME)
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
                self.ui.action_save.get_label().replace('_', ''))
        response = self.ui.dialog_create_appfolder.run()
        self.ui.dialog_create_appfolder.hide()
        return response

    def destroy(self):
        """Destroy the dialog"""
        settings.positions.save_window_position(
            self.ui.dialog_create_appfolder, SECTION_WINDOW_NAME)
        self.ui.dialog_create_appfolder.destroy()
        self.ui.dialog_create_appfolder = None

    def on_action_close_activate(self, action):
        """Close the dialog"""
        self.ui.dialog_create_appfolder.response(Gtk.ResponseType.CLOSE)

    def on_action_confirm_activate(self, action):
        """Accept the folder name and title and close the dialog"""
        self.folder_name = self.ui.entry_name.get_text().strip()
        self.folder_title = self.ui.entry_title.get_text().strip()
        self.ui.dialog_create_appfolder.response(Gtk.ResponseType.OK)

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
