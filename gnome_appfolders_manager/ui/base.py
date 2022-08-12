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

import pathlib
from typing import Iterable

from gi.repository import Gtk

from gnome_appfolders_manager.constants import DIR_ICONS
from gnome_appfolders_manager.functions import get_ui_file
from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader
from gnome_appfolders_manager.localize import text


class UIBase(object):
    def __init__(self, filename):
        self.ui = GtkBuilderLoader(get_ui_file(filename))

    def set_buttons_icons(self, buttons: Iterable) -> None:
        """
        Set icons for buttons

        :param buttons: tuple or list of buttons to customize
        :return: None
        """
        for button in buttons:
            action = button.get_related_action()
            button.set_image(Gtk.Image.new_from_icon_name(
                icon_name=action.get_icon_name(),
                size=Gtk.IconSize.BUTTON))
            # Remove the button label for not important buttons
            if not action.get_is_important():
                button.props.label = None

    def set_titles(self) -> None:
        """
        Set titles and tooltips for Actions, Labels and Buttons
        :return: None
        """
        # Set Actions labels and short labels
        for widget in self.ui.get_objects_by_type(Gtk.Action):
            # Connect the actions accelerators
            widget.connect_accelerator()
            # Set labels
            label = widget.get_label()
            if not label:
                label = widget.get_short_label()
            widget.set_label(text(label))
            widget.set_short_label(text(label))
        # Set Labels captions
        for widget in self.ui.get_objects_by_type(Gtk.Label):
            widget.set_label(text(widget.get_label()))
        # Initialize tooltips
        for widget in self.ui.get_objects_by_type(Gtk.Button):
            action = widget.get_related_action()
            if action:
                widget.set_tooltip_text(action.get_label().replace('_', ''))

    def load_image_file(self, image: Gtk.Image) -> bool:
        """
        Load an icon from filesystem if existing
        """
        icon_name, _ = image.get_icon_name()
        icon_path = pathlib.Path(DIR_ICONS / f'{icon_name}.png')
        if icon_path.is_file():
            image.set_from_file(str(icon_path))
        return icon_path.is_file()

    def set_buttons_style_suggested_action(self, buttons: Iterable):
        """Add the suggested-action style to a widget"""
        for button in buttons:
            button.get_style_context().add_class('suggested-action')

    def set_buttons_style_destructive_action(self, buttons: Iterable):
        """Add the destructive-action style to a widget"""
        for button in buttons:
            button.get_style_context().add_class('destructive-action')

    def show_popup_menu(self, menu: Gtk.Menu):
        """Show a popup menu at the current position"""
        if not Gtk.check_version(3, 22, 0):
            menu.popup_at_pointer(trigger_event=None)
        else:
            menu.popup(parent_menu_shell=None,
                       parent_menu_item=None,
                       func=None,
                       data=0,
                       button=0,
                       activate_time=Gtk.get_current_event_time())
