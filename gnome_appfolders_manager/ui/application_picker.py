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

import logging

from gi.repository import Gio
from gi.repository import Gtk

from gnome_appfolders_manager.functions import (set_style_suggested_action,
                                                get_treeview_selected_rows)
from gnome_appfolders_manager.models.application_info import ApplicationInfo
from gnome_appfolders_manager.models.applications import ModelApplications
import gnome_appfolders_manager.preferences as preferences
import gnome_appfolders_manager.settings as settings
from gnome_appfolders_manager.ui.base import UIBase

SECTION_WINDOW_NAME = 'application picker'


class UIApplicationPicker(UIBase):
    def __init__(self, parent, existing_files):
        """Prepare the application picker dialog"""
        super().__init__(filename='application_picker.ui')
        # Load the user interface
        self.ui.dialog.set_titlebar(self.ui.header_bar)
        # Prepares the models for the applications
        self.model_applications = ModelApplications(self.ui.store_applications)
        self.model_applications.model.set_sort_column_id(
            self.ui.treeview_column_applications.get_sort_column_id(),
            Gtk.SortType.ASCENDING)
        self.ui.filter_applications.set_visible_column(
            ModelApplications.COL_VISIBLE)
        # Initialize titles and tooltips
        self.initialize_titles()
        # Set various properties
        self.ui.dialog.set_transient_for(parent)
        set_style_suggested_action(self.ui.button_add)
        self.selected_applications = None
        # Initialize Gtk.HeaderBar
        for button in (self.ui.button_search, ):
            action = button.get_related_action()
            button.set_image(Gtk.Image.new_from_icon_name(
                icon_name=action.get_icon_name(),
                size=Gtk.IconSize.BUTTON))
            if not action.get_is_important():
                # Remove the button label
                button.props.label = None
            # Set the tooltip from the action label
            button.set_tooltip_text(action.get_label().replace('_', ''))
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
                if application.filename not in existing_files:
                    self.model_applications.add_data(application)
            except Exception as e:
                logging.error(f'{desktop_entry.get_id()}: {e}')
        self.model_applications.set_all_rows_visibility(
            preferences.get(preferences.APP_PICKER_SHOW_HIDDEN))
        # Connect signals from the UI file to the module functions
        self.ui.connect_signals(self)

    def show(self):
        """Show the application picker dialog"""
        settings.positions.restore_window_position(window=self.ui.dialog,
                                                   section=SECTION_WINDOW_NAME)
        response = self.ui.dialog.run()
        self.ui.dialog.hide()
        return response

    def destroy(self):
        """Destroy the application picker dialog"""
        settings.positions.save_window_position(window=self.ui.dialog,
                                                section=SECTION_WINDOW_NAME)
        self.ui.dialog.destroy()
        self.ui.dialog = None

    def on_action_close_activate(self, action):
        """Close the application picker dialog"""
        self.ui.dialog.response(Gtk.ResponseType.CLOSE)

    def on_action_add_activate(self, action):
        """Add the selected application to the current AppFolder"""
        self.selected_applications = []
        for row in get_treeview_selected_rows(self.ui.treeview_applications):
            application = self.model_applications.get_key(
                self.ui.filter_applications.convert_path_to_child_path(row))
            self.selected_applications.append(application)
        self.ui.dialog.response(Gtk.ResponseType.OK)

    def on_treeview_applications_row_activated(self, widget, path, column):
        """Add the selected application on row activation"""
        self.ui.action_add.activate()

    def on_treeview_selection_applications_changed(self, widget):
        """Set action sensitiveness on selection change"""
        selected_rows = get_treeview_selected_rows(
            self.ui.treeview_applications)
        self.ui.action_add.set_sensitive(bool(selected_rows))

    def on_action_search_activate(self, action):
        """Start interactive files search"""
        self.ui.treeview_applications.grab_focus()
        self.ui.treeview_applications.emit('start-interactive-search')
