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

import os
import os.path
import fnmatch
from gettext import gettext, dgettext

from gi.repository import Gtk

from gnome_appfolders_manager.constants import DIR_UI

localized_messages = {}


def readlines(filename, empty_lines=False):
    """Read all the lines of a filename, optionally skipping empty lines"""
    result = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line or empty_lines:
                result.append(line)
        f.close()
    return result


def text(message, gtk30=False, context=None):
    """Return a translated message and cache it for reuse"""
    if message not in localized_messages:
        if gtk30:
            # Get a message translated from GTK+ 3 domain
            full_message = message if not context else '%s\04%s' % (
                context, message)
            localized_messages[message] = dgettext('gtk30', full_message)
        else:
            localized_messages[message] = gettext(message)
    return localized_messages[message]


def get_ui_file(filename):
    """Return the full path of a Glade/UI file"""
    return os.path.join(DIR_UI, filename)


def recursive_glob(starting_path, pattern):
    """Return a list of all the matching files recursively"""
    result = []
    for root, dirnames, filenames in os.walk(starting_path):
        for filename in fnmatch.filter(filenames, pattern):
            result.append(os.path.join(root, filename))
    return result


def add_separator_listboxrow(row, before, user_data):
    """Add a horizontal Gtk.Separator to a Gtk.ListBoxRow header"""
    if before and not row.get_header():
        row.set_header(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))


# This special alias is used to track localization requests to catch
# by xgettext. The text() calls aren't tracked by xgettext
_ = text

__all__ = [
    'readlines',
    'text',
    '_',
    'localized_messages',
    'get_ui_file',
    'recursive_glob',
    'add_separator_listboxrow'
]
