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

from gnome_appfolders_manager.functions import get_pixbuf_from_icon_name
from gnome_appfolders_manager.models.abstract import ModelAbstract


class ModelAppFolders(ModelAbstract):
    COL_TITLE = 1
    COL_FILENAME = 2
    COL_DESCRIPTION = 3
    COL_ICON = 4

    def add_data(self, item):
        """Add a new row to the model if it doesn't exist"""
        super(self.__class__, self).add_data(item)
        if item.name not in self.rows:
            new_row = self.model.append((
                item.name,
                item.title,
                item.filename,
                f'<b>{item.title}</b>\n'
                f'<small>{item.name}\n'
                f'{item.filename}</small>',
                get_pixbuf_from_icon_name(item.icon_name, 48)
                if item.icon_name else None))
            self.rows[item.name] = new_row
            return new_row

    def get_title(self, treeiter):
        """Get the title from a TreeIter"""
        return self.get_data(treeiter, self.COL_TITLE)
