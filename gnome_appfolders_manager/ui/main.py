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

from gnome_appfolders_manager.constants import (
    APP_NAME,
    FILE_SETTINGS, FILE_WINDOWS_POSITION,
    SCHEMA_FOLDERS)
from gnome_appfolders_manager.functions import (
    get_ui_file, add_separator_listboxrow, text, _)
import gnome_appfolders_manager.preferences as preferences
import gnome_appfolders_manager.settings as settings
from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader

from gnome_appfolders_manager.ui.about import UIAbout

from gnome_appfolders_manager.models.folder_info import FolderInfo

SECTION_WINDOW_NAME = 'main'


class UIMain(object):
    def __init__(self, application):
        self.application = application
        # Load settings
        settings.settings = settings.Settings(FILE_SETTINGS, False)
        settings.positions = settings.Settings(FILE_WINDOWS_POSITION, False)
        self.desktop_entries = []
        self.folders = {}
        preferences.preferences = preferences.Preferences()
        self.loadUI()
        self.reload_folders()

        # Restore the saved size and position
        settings.positions.restore_window_position(
            self.ui.win_main, SECTION_WINDOW_NAME)

    def loadUI(self):
        """Load the interface UI"""
        self.ui = GtkBuilderLoader(get_ui_file('main.ui'))
        self.ui.win_main.set_application(self.application)
        self.ui.win_main.set_title(APP_NAME)
        # Initialize actions
        for widget in self.ui.get_objects_by_type(Gtk.Action):
            # Connect the actions accelerators
            widget.connect_accelerator()
            # Set labels
            widget.set_label(text(widget.get_label()))
        # Initialize tooltips
        for widget in self.ui.get_objects_by_type(Gtk.ToolButton):
            action = widget.get_related_action()
            if action:
                widget.set_tooltip_text(action.get_label().replace('_', ''))
        # Initialize Gtk.HeaderBar
        self.ui.header_bar.props.title = self.ui.win_main.get_title()
        self.ui.win_main.set_titlebar(self.ui.header_bar)
        for button in (self.ui.button_new, self.ui.button_edit,
                       self.ui.button_delete, self.ui.button_about):
            action = button.get_related_action()
            icon_name = action.get_icon_name()
            if preferences.get(preferences.HEADERBARS_SYMBOLIC_ICONS):
                icon_name += '-symbolic'
            # Get desired icon size
            icon_size = (Gtk.IconSize.BUTTON
                         if preferences.get(preferences.HEADERBARS_SMALL_ICONS)
                         else Gtk.IconSize.LARGE_TOOLBAR)
            button.set_image(Gtk.Image.new_from_icon_name(icon_name,
                                                          icon_size))
            # Remove the button label
            button.props.label = None
            # Set the tooltip from the action label
            button.set_tooltip_text(action.get_label().replace('_', ''))
        # Automatically add a Gtk.Separator to each Gtk.ListBoxRow
        self.ui.listbox_folders.set_header_func(add_separator_listboxrow, None)
        self.ui.listbox_files.set_header_func(add_separator_listboxrow, None)
        # Connect signals from the glade file to the module functions
        self.ui.connect_signals(self)

    def run(self):
        """Show the UI"""
        self.ui.win_main.show_all()

    def on_win_main_delete_event(self, widget, event):
        """Save the settings and close the application"""
        settings.positions.save_window_position(
            self.ui.win_main, SECTION_WINDOW_NAME)
        settings.positions.save()
        settings.settings.save()
        self.application.quit()

    def on_action_about_activate(self, action):
        """Show the about dialog"""
        dialog = UIAbout(self.ui.win_main)
        dialog.show()
        dialog.destroy()

    def on_action_quit_activate(self, action):
        """Close the application by closing the main window"""
        event = Gdk.Event()
        event.key.type = Gdk.EventType.DELETE
        self.ui.win_main.event(event)

    def reload_folders(self):
        """Reload the Application Folders"""
        self.folders = {}
        settings_folders = Gio.Settings.new(SCHEMA_FOLDERS)
        list_folders = settings_folders.get_value('folder-children')
        for folder_name in list_folders:
            folder_info = FolderInfo(folder_name)
            # New box for folder icon and description
            new_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                              spacing=5)
            new_box.add(Gtk.Image.new_from_icon_name(
                folder_info.desktop_entry.getIcon(), Gtk.IconSize.DIALOG))

            new_box_labels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                     homogeneous=True,
                                     spacing=3)
            new_box.add(new_box_labels)
            # Gtk.Label with name
            new_label = Gtk.Label()
            new_label.set_markup('<b>%s</b>' % folder_info.folder)
            new_label.set_hexpand(True)
            new_label.set_halign(Gtk.Align.START)
            new_box_labels.add(new_label)
            # Gtk.Label with title
            new_label = Gtk.Label()
            new_label.set_markup('<span size="small">%s</span>' %
                                 folder_info.desktop_entry.getName())
            new_label.set_halign(Gtk.Align.START)
            new_box_labels.add(new_label)

            new_row = Gtk.ListBoxRow(height_request=40)
            new_row.add(new_box)
            self.ui.listbox_folders.add(new_row)
            self.folders[folder_info.name] = (new_row, folder_info)

    def on_listbox_folders_row_selected(self, widget, selected_row):
        """Reload the applications for the selected AppFolder"""
        def add_new_application(filename, desktop_file):
            """Add a new application from a .desktop file"""
            self.desktop_entries.append(filename)
            # New Gtk.Box for application icon, name and description
            new_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                              spacing=5)
            new_box.show()
            # Add Gtk.Image for application icon (and resize the icon)
            new_image = Gtk.Image.new_from_icon_name(desktop_file.getIcon()
                                                     if desktop_file
                                                     else 'gtk-missing-image',
                                                     Gtk.IconSize.DIALOG)
            (status, width, height) = Gtk.IconSize.lookup(Gtk.IconSize.DIALOG)
            new_image.set_pixel_size(height)

            new_image.show()
            new_box.add(new_image)
            # Add a new Gtk.Box with name and filename
            new_box_labels = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                     homogeneous=True,
                                     spacing=3)
            new_box_labels.show()
            new_box.add(new_box_labels)
            # Add Gtk.Label for application name
            new_label = Gtk.Label()
            new_label.set_markup('<b>%s</b>' % (desktop_file.getName()
                                 if desktop_file else 'Missing desktop file'))
            new_label.set_hexpand(True)
            new_label.set_halign(Gtk.Align.START)
            new_label.show()
            new_box_labels.add(new_label)
            # Add Gtk.Label for filename
            new_label = Gtk.Label()
            new_label.set_markup(filename)
            new_label.set_halign(Gtk.Align.START)
            new_label.show()
            new_box_labels.add(new_label)
            # Add Gtk.ListBoxRow with the previous
            new_row = Gtk.ListBoxRow(height_request=40)
            new_row.show()
            new_row.add(new_box)
            self.ui.listbox_files.add(new_row)
        if selected_row:
            for key in self.folders:
                if self.folders[key][0] is selected_row:
                    folder_info = self.folders[key][1]
                    self.ui.lbl_name_text.set_label(folder_info.folder)
                    self.ui.lbl_title_text.set_label(
                        folder_info.desktop_entry.getName())
                    self.ui.lbl_description_text.set_label(
                        folder_info.desktop_entry.getComment())
                    applications = folder_info.get_applications()
                    # Clear any previous application icon
                    for row in self.ui.listbox_files:
                        row.destroy()
                    self.desktop_entries = []
                    # Add new application icons
                    for application in applications:
                        desktop_file = applications[application]
                        add_new_application(application, desktop_file)
                    break
