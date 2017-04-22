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


class GtkBuilderLoader(object):
    def __init__(self, *ui_files):
        """Load one or more ui files for GtkBuilder"""
        self.builder = Gtk.Builder()
        for ui_filename in ui_files:
            self.builder.add_from_file(ui_filename)
        self.__widgets = {}

    def __getattr__(self, key):
        """Get a widget from GtkBuilder using class member name"""
        if key not in self.__widgets:
            self.__widgets[key] = self.builder.get_object(key)
            assert self.__widgets[key], 'Missing widget: %s' % key
        return self.__widgets[key]

    def get_objects(self):
        """Get the widgets list from GtkBuilder"""
        return self.builder.get_objects()

    def get_objects_by_type(self, type):
        """Get the widgets list with a specific type from GtkBuilder"""
        return [w for w in self.get_objects() if isinstance(w, type)]

    def get_object(self, key):
        """Get a widget from GtkBuilder using a method"""
        return self.__getattr__(key)

    def connect_signals(self, handlers):
        """Connect all the Gtk signals to a group of handlers"""
        self.builder.connect_signals(handlers)
