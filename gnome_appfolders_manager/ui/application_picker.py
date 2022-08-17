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

from gi.repository import Gio
from gi.repository import Gtk

from gnome_appfolders_manager.functions import get_treeview_selected_rows
from gnome_appfolders_manager.models.application_info import ApplicationInfo
from gnome_appfolders_manager.models.applications import ModelApplications
from gnome_appfolders_manager.settings import APP_PICKER_SHOW_HIDDEN
from gnome_appfolders_manager.ui.base import UIBase

SECTION_WINDOW_NAME = 'application picker'


class UIApplicationPicker(UIBase):
    def __init__(self, parent, settings, options, existing_files):
        """Prepare the application picker dialog"""
        logging.debug(f'{self.__class__.__name__} init')
        super().__init__(filename='application_picker.ui')
        # Initialize members
        self.parent = parent
        self.settings = settings
        self.options = options
        self.existing_files = existing_files
        self.selected_applications = None
        # Load UI
        self.load_ui()
        # Prepare the models
        self.model_applications = ModelApplications(self.ui.store_applications)
        # Complete initialization
        self.startup()

    def load_ui(self):
        """Load the interface UI"""
        logging.debug(f'{self.__class__.__name__} load UI')
        # Initialize titles and tooltips
        self.set_titles()
        # Initialize Gtk.HeaderBar
        self.set_buttons_icons(buttons=[self.ui.button_search])
        self.ui.dialog.set_titlebar(self.ui.header_bar)
        # Set buttons as suggested
        self.set_buttons_style_suggested_action(
            buttons=[self.ui.button_add])
        # Set various properties
        self.ui.dialog.set_transient_for(self.parent)
        # Connect signals from the UI file to the functions with the same name
        self.ui.connect_signals(self)

    def startup(self):
        """Complete initialization"""
        logging.debug(f'{self.__class__.__name__} startup')
        # Prepares the applications list
        for desktop_entry in Gio.app_info_get_all():
            try:
                icon_name = None
                icon = desktop_entry.get_icon()
                if isinstance(icon, Gio.ThemedIcon):
                    # From Gio.ThemedIcon get the icon name only
                    icons = desktop_entry.get_icon().get_names()
                    icon_name = icons[0] if icons else None
                elif isinstance(icon, Gio.FileIcon):
                    # From Gio.FileIcon get the full file name
                    icon_name = icon.get_file().get_parse_name()
                description = (desktop_entry.get_description()
                               if desktop_entry.get_description() else '')
                application = ApplicationInfo(desktop_entry.get_id(),
                                              desktop_entry.get_name(),
                                              description,
                                              icon_name,
                                              desktop_entry.should_show())
                # Skip existing files
                if application.filename not in self.existing_files:
                    self.model_applications.add_data(application)
            except Exception as e:
                logging.error(f'{desktop_entry.get_id()}: {e}')
        self.model_applications.set_all_rows_visibility(
            self.settings.get_preference(option=APP_PICKER_SHOW_HIDDEN))
        self.model_applications.model.set_sort_column_id(
            self.ui.treeview_column_applications.get_sort_column_id(),
            Gtk.SortType.ASCENDING)
        self.ui.filter_applications.set_visible_column(
            ModelApplications.COL_VISIBLE)
        # Restore the saved size and position
        self.settings.restore_window_position(window=self.ui.dialog,
                                              section=SECTION_WINDOW_NAME)

    def show(self):
        """Show the application picker dialog"""
        response = self.ui.dialog.run()
        self.ui.dialog.hide()
        return response

    def destroy(self):
        """Destroy the application picker dialog"""
        self.settings.save_window_position(window=self.ui.dialog,
                                           section=SECTION_WINDOW_NAME)
        self.ui.dialog.destroy()
        self.ui.dialog = None

    def on_action_close_activate(self, widget):
        """Close the application picker dialog"""
        self.ui.dialog.response(Gtk.ResponseType.CLOSE)

    def on_action_add_activate(self, widget):
        """Add the selected application to the current AppFolder"""
        self.selected_applications = []
        for row in get_treeview_selected_rows(self.ui.treeview_applications):
            application = self.model_applications.get_key(
                self.ui.filter_applications.convert_path_to_child_path(row))
            self.selected_applications.append(application)
        self.ui.dialog.response(Gtk.ResponseType.OK)

    def on_action_search_activate(self, widget):
        """Start interactive files search"""
        self.ui.treeview_applications.grab_focus()
        self.ui.treeview_applications.emit('start-interactive-search')

    def on_treeview_applications_row_activated(self, widget, path, column):
        """Add the selected application on row activation"""
        self.ui.action_add.activate()

    def on_treeview_selection_applications_changed(self, widget):
        """Set action sensitiveness on selection change"""
        selected_rows = get_treeview_selected_rows(
            self.ui.treeview_applications)
        self.ui.action_add.set_sensitive(bool(selected_rows))
