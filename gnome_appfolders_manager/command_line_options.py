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

import argparse

from gnome_appfolders_manager.constants import (APP_NAME,
                                                APP_VERSION,
                                                VERBOSE_LEVEL_QUIET,
                                                VERBOSE_LEVEL_NORMAL,
                                                VERBOSE_LEVEL_MAX)


class CommandLineOptions(object):
    """
    Parse command line arguments
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=None,
                                              description=APP_NAME)
        self.parser.set_defaults(verbose_level=VERBOSE_LEVEL_NORMAL)
        self.parser.add_argument('-V',
                                 '--version',
                                 action='version',
                                 version=f'{APP_NAME} v{APP_VERSION}')
        self.parser.add_argument('-v', '--verbose',
                                 dest='verbose_level',
                                 action='store_const',
                                 const=VERBOSE_LEVEL_MAX,
                                 help='show error and information messages')
        self.parser.add_argument('-q', '--quiet',
                                 dest='verbose_level',
                                 action='store_const',
                                 const=VERBOSE_LEVEL_QUIET,
                                 help='hide error and information messages')
        self.options = None

    def add_group(self, name: str) -> argparse._ArgumentGroup:
        """
        Add a command-line options group

        :param name: name for the new group
        :return: _ArgumentGroup object with the new command-line options group
        """
        return self.parser.add_argument_group(name)

    def parse_options(self) -> argparse.Namespace:
        """
        Parse command-line options

        :return: command-line options
        """
        self.options = self.parser.parse_args()
        return self.options
