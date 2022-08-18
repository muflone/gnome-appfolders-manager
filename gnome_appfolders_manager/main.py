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

import logging

import gnome_appfolders_manager.requires                           # noqa: F401
from gnome_appfolders_manager.app import Application
from gnome_appfolders_manager.command_line_options import CommandLineOptions
from gnome_appfolders_manager.constants import (DIR_DATA,
                                                DIR_DOCS,
                                                DIR_LOCALE,
                                                DIR_PREFIX,
                                                DIR_SETTINGS,
                                                DIR_UI)
import gnome_appfolders_manager.translations                       # noqa: F401


def main():
    command_line_options = CommandLineOptions()
    options = command_line_options.parse_options()
    # Set logging level
    verbose_levels = {0: logging.ERROR,
                      1: logging.INFO,
                      2: logging.DEBUG}
    logging.basicConfig(level=verbose_levels[options.verbose_level],
                        format='%(asctime)s '
                               '%(levelname)-8s '
                               '%(filename)-25s '
                               'line: %(lineno)-5d '
                               '%(funcName)-30s '
                               'pid: %(process)-9d '
                               '%(message)s')
    # Log paths for debug purposes
    # Not using {VARIABLE=} as it's not compatible with Python 3.6
    logging.debug(f'DIR_PREFIX={str(DIR_PREFIX)}')
    logging.debug(f'DIR_LOCALE={str(DIR_LOCALE)}')
    logging.debug(f'DIR_DOCS={str(DIR_DOCS)}')
    logging.debug(f'DIR_DATA={str(DIR_DATA)}')
    logging.debug(f'DIR_UI={str(DIR_UI)}')
    logging.debug(f'DIR_SETTINGS={str(DIR_SETTINGS)}')
    # Start the application
    app = Application(options=options)
    app.run(None)
