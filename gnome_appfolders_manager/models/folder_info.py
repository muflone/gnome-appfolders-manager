##
#     Project: GNOME App Folders Manager
# Description: Manage GNOME Shell applications folders
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2016-2022 Fabio Castelli
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

import os.path

from gi.repository import Gio

from xdg import BaseDirectory, DesktopEntry

from gnome_appfolders_manager.constants import SCHEMA_FOLDER

PATH_FOLDER = '/org/gnome/desktop/app-folders/folders/{folder}/'

OPTION_FOLDER_NAME = 'name'
OPTION_FOLDER_TRANSLATE = 'translate'
OPTION_FOLDER_APPS = 'apps'
OPTION_FOLDER_CATEGORIES = 'categories'


class FolderInfo(object):
    def __init__(self, folder):
        """Find a folder from the settings"""
        self.folder = folder
        # Get info from the settings schema
        folder_path = PATH_FOLDER.format(folder=folder)
        self.settings = Gio.Settings.new_with_path(schema_id=SCHEMA_FOLDER,
                                                   path=folder_path)
        self.name = self.settings.get_string(OPTION_FOLDER_NAME)
        self.translate = self.settings.get_boolean(OPTION_FOLDER_TRANSLATE)
        self.apps = self.settings.get_strv(OPTION_FOLDER_APPS)
        self.categories = self.settings.get_strv(OPTION_FOLDER_CATEGORIES)
        self.desktop_entry = None
        # Find desktop directory file
        if self.name.endswith('.directory'):
            datadirs = BaseDirectory.load_data_paths('desktop-directories')
            for datadir in datadirs:
                filename = os.path.join(datadir, self.name)
                if os.path.exists(filename):
                    self.desktop_entry = DesktopEntry.DesktopEntry(filename)
                    break

    def get_applications(self):
        """Returns a dictionary object for each application"""
        result = {}
        datadirs = list(BaseDirectory.load_data_paths('applications'))
        for application in self.apps:
            for datadir in datadirs:
                filename = os.path.join(datadir, application)
                if os.path.exists(filename):
                    desktop_entry = DesktopEntry.DesktopEntry(filename)
                    break
            else:
                desktop_entry = None
            result[application] = desktop_entry
        return result

    def set_applications(self, applications):
        """Set the applications list"""
        self.apps = applications
        self.settings.set_strv(OPTION_FOLDER_APPS, self.apps)

    def get_name(self):
        """Return the AppFolder name"""
        return (self.desktop_entry.getName() if self.desktop_entry
                else self.name)

    def get_comment(self):
        """Return the AppFolder comment"""
        return self.desktop_entry.getComment() if self.desktop_entry else ''

    def set_title(self, title):
        """Set the AppFolder title"""
        self.settings.set_string(OPTION_FOLDER_NAME, title)

    def get_icon_name(self):
        """Return the AppFolder icon name"""
        return self.desktop_entry.getIcon() if self.desktop_entry else ''

    def remove(self):
        """Remove the AppFolder by resetting all the children keys"""
        for key in self.settings.keys():
            self.settings.reset(key)

    def get_readonly(self):
        """Check if the folder name is read-only (its name is got from
        desktop-directories)"""
        return self.name.endswith('.directory')
