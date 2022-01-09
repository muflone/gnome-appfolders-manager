##
#     Project: GNOME App Folders Manager
# Description: Manage GNOME Shell applications folders
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2016-2022 Fabio Castelli
#     License: GPL-3+
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

import logging

from gnome_appfolders_manager.app import Application
from gnome_appfolders_manager.command_line_options import CommandLineOptions
from gnome_appfolders_manager.constants import (DIR_DATA,
                                                DIR_DOCS,
                                                DIR_LOCALE,
                                                DIR_PREFIX,
                                                DIR_SETTINGS,
                                                DIR_UI)


def main():
    command_line_options = CommandLineOptions()
    options = command_line_options.parse_options()
    # Set logging level
    verbose_levels = {0: logging.ERROR,
                      1: logging.INFO,
                      2: logging.DEBUG}
    logging.getLogger().setLevel(verbose_levels[options.verbose_level])
    # Log paths for debug purposes
    logging.debug(f'{DIR_PREFIX=}')
    logging.debug(f'{DIR_LOCALE=}')
    logging.debug(f'{DIR_DOCS=}')
    logging.debug(f'{DIR_DATA=}')
    logging.debug(f'{DIR_UI=}')
    logging.debug(f'{DIR_SETTINGS=}')
    # Start the application
    app = Application()
    app.run(None)
