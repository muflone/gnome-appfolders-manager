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
from gi.repository import Gio
from gi.repository import GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

import gnome_appfolders_manager.settings as settings
import gnome_appfolders_manager.preferences as preferences
from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader
from gnome_appfolders_manager.functions import (
    get_ui_file, set_style_suggested_action, get_treeview_selected_row,
    get_treeview_selected_rows, text)

from gnome_appfolders_manager.models.application_info import ApplicationInfo
from gnome_appfolders_manager.models.applications import ModelApplications

SECTION_WINDOW_NAME = 'application picker'


class UIApplicationPicker(object):
    def __init__(self, parent, existing_files):
        """Prepare the application picker dialog"""
        # Load the user interface
        self.ui = GtkBuilderLoader(get_ui_file('application_picker.ui'))
        self.ui.dialog_application_picker.set_titlebar(self.ui.header_bar)
        # Prepares the models for the applications
        self.model_applications = ModelApplications(self.ui.store_applications)
        self.model_applications.model.set_sort_column_id(
            self.ui.treeview_column_applications.get_sort_column_id(),
            Gtk.SortType.ASCENDING)
        self.ui.filter_applications.set_visible_column(
            ModelApplications.COL_VISIBLE)
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
        # Initialize tooltips
        for widget in self.ui.get_objects_by_type(Gtk.Button):
            action = widget.get_related_action()
            if action:
                widget.set_tooltip_text(action.get_label().replace('_', ''))
        # Set various properties
        self.ui.dialog_application_picker.set_transient_for(parent)
        set_style_suggested_action(self.ui.button_add)
        self.selected_applications = None
        # Set preferences button icon
        icon_name = self.ui.image_preferences.get_icon_name()[0]
        if preferences.get(preferences.HEADERBARS_SYMBOLIC_ICONS):
            icon_name += '-symbolic'
        # Get desired icon size
        icon_size = (Gtk.IconSize.BUTTON
                     if preferences.get(preferences.HEADERBARS_SMALL_ICONS)
                     else Gtk.IconSize.LARGE_TOOLBAR)
        self.ui.image_preferences.set_from_icon_name(icon_name, icon_size)
        # Load settings
        self.dict_settings_map = {
            preferences.APP_PICKER_SHOW_HIDDEN:
                self.ui.action_show_hidden
        }
        for setting_name, action in self.dict_settings_map.items():
            action.set_active(preferences.get(setting_name))
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
                print 'error for', desktop_entry.get_id(), e
        self.model_applications.set_all_rows_visibility(
            preferences.get(preferences.APP_PICKER_SHOW_HIDDEN))
        # Connect signals from the glade file to the module functions
        self.ui.connect_signals(self)

    def show(self):
        """Show the application picker dialog"""
        settings.positions.restore_window_position(
            self.ui.dialog_application_picker, SECTION_WINDOW_NAME)
        response = self.ui.dialog_application_picker.run()
        self.ui.dialog_application_picker.hide()
        return response

    def destroy(self):
        """Destroy the application picker dialog"""
        settings.positions.save_window_position(
            self.ui.dialog_application_picker, SECTION_WINDOW_NAME)
        self.ui.dialog_application_picker.destroy()
        self.ui.dialog_application_picker = None

    def on_action_close_activate(self, action):
        """Close the application picker dialog"""
        self.ui.dialog_application_picker.response(Gtk.ResponseType.CLOSE)

    def on_action_add_activate(self, action):
        """Add the selected application to the current AppFolder"""
        self.selected_applications = []
        for row in get_treeview_selected_rows(self.ui.treeview_applications):
            application = self.model_applications.get_key(
                self.ui.filter_applications.convert_path_to_child_path(row))
            self.selected_applications.append(application)
        self.ui.dialog_application_picker.response(Gtk.ResponseType.OK)

    def on_treeview_applications_row_activated(self, widget, path, column):
        """Add the selected application on row activation"""
        self.ui.action_add.activate()

    def on_treeview_selection_applications_changed(self, widget):
        """Set action sensitiveness on selection change"""
        selected_rows = get_treeview_selected_rows(
            self.ui.treeview_applications)
        self.ui.action_add.set_sensitive(bool(selected_rows))

    def on_action_preferences_toggled(self, widget):
        """Change a preference value"""
        for setting_name, action in self.dict_settings_map.items():
            if action is widget:
                preferences.set(setting_name, widget.get_active())

    def on_action_show_hidden_toggled(self, widget):
        """Set the visibility for all the Gtk.TreeModelRows"""
        self.model_applications.set_all_rows_visibility(
            self.ui.action_show_hidden.get_active())
