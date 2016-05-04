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


class ModelAbstract(object):
    COL_KEY = 0

    def __init__(self, model):
        self.model = model
        # Fill the rows dictionary with the model items
        self.rows = {}
        for row in self.model:
            name = row[self.COL_KEY]
            self.rows[name] = self.model.get_iter(row.path)

    def clear(self):
        """Clear the model"""
        self.rows.clear()
        return self.model.clear()

    def add_data(self, item):
        """Add a new row to the model if it doesn't exists"""
        pass

    def set_data(self, treeiter, item):
        """Update an existing TreeIter"""
        old_key = self.get_key(treeiter)
        # If the new name differs from the old name then update the
        # TreeIters map in self.rows
        if old_key != item.name:
            self.rows.pop(old_key)
            self.rows[item.name] = treeiter

    def get_key(self, treeiter):
        """Get the name from a TreeIter"""
        return self.model[treeiter][self.COL_KEY]

    def get_iter(self, name):
        """Get a TreeIter from a name"""
        return self.rows.get(name)

    def get_model_row(self, treeiter):
        """Get a TreeModelRow from a TreeIter"""
        return self.model[treeiter]

    def get_path(self, treeiter):
        """Get the path from a TreeIter"""
        return self.get_model_row(treeiter).path

    def get_path_by_name(self, name):
        """Get the path from a name"""
        return self.get_model_row(self.get_iter(name)).path

    def remove(self, treeiter):
        """Remove a TreeIter"""
        self.rows.pop(self.get_key(treeiter))
        self.model.remove(treeiter)

    def dump(self):
        """Extract the model data to a dict object"""
        pass

    def load(self, items):
        """Load the model data from a dict object"""
        for key in sorted(items.iterkeys()):
            self.add_data(items[key])

    def count(self):
        """Return the number of items in the model"""
        return len(self.model)
