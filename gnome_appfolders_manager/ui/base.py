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

from typing import Iterable

from gi.repository import Gtk

from gnome_appfolders_manager.gtkbuilder_loader import GtkBuilderLoader

from gnome_appfolders_manager.functions import get_ui_file
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
