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
import sys

from xdg import BaseDirectory


# Application constants
APP_NAME = 'GNOME AppFolders Manager'
APP_VERSION = '0.4.6'
APP_DESCRIPTION = 'Manage GNOME Shell applications folders'
APP_ID = 'gnome-appfolders-manager.muflone.com'
APP_URL = 'https://www.muflone.com/gnome-appfolders-manager/'
APP_AUTHOR = 'Fabio Castelli'
APP_AUTHOR_EMAIL = 'muflone@muflone.com'
APP_COPYRIGHT = f'Copyright 2016-2022 {APP_AUTHOR}'
URL_SOURCES = 'https://github.com/muflone/gnome-appfolders-manager/'
# Other constants
DOMAIN_NAME = 'gnome-appfolders-manager'
VERBOSE_LEVEL_QUIET = 0
VERBOSE_LEVEL_NORMAL = 1
VERBOSE_LEVEL_MAX = 2
MISSING_ICON_NAME = 'application-x-executable'

# Paths constants
path_xdg_data_home = pathlib.Path(BaseDirectory.xdg_data_home)
icon_name = f'{DOMAIN_NAME}.png'
if (pathlib.Path('data') / icon_name).is_file():
    # Use relative paths
    DIR_PREFIX = pathlib.Path('data').parent.absolute()
    DIR_LOCALE = DIR_PREFIX / 'locale'
    DIR_DOCS = DIR_PREFIX / 'doc'
elif (path_xdg_data_home / DOMAIN_NAME / 'data' / icon_name).is_file():
    # Use local user path
    DIR_PREFIX = path_xdg_data_home / DOMAIN_NAME
    DIR_LOCALE = path_xdg_data_home / 'locale'
    DIR_DOCS = path_xdg_data_home / 'doc' / DOMAIN_NAME
elif (pathlib.Path(__file__).parent.parent / 'share' / DOMAIN_NAME / 'data' /
      icon_name).is_file():
    # Use local user path in the local Python directory
    DIR_PREFIX = pathlib.Path(__file__).parent.parent / 'share' / DOMAIN_NAME
    DIR_LOCALE = DIR_PREFIX.parent / 'locale'
    DIR_DOCS = DIR_PREFIX.parent / 'doc' / DOMAIN_NAME
else:
    # Use system path
    path_prefix = pathlib.Path(sys.prefix)
    DIR_PREFIX = path_prefix / 'share' / DOMAIN_NAME
    DIR_LOCALE = path_prefix / 'share' / 'locale'
    DIR_DOCS = path_prefix / 'share' / 'doc' / DOMAIN_NAME
# Set the paths for the folders
DIR_DATA = DIR_PREFIX / 'data'
DIR_ICONS = DIR_DATA / 'icons'
DIR_UI = DIR_PREFIX / 'ui'
try:
    # In read-only environments, the settings folder cannot be created
    # (e.g. in a Debian pbuilder fakeroot)
    DIR_SETTINGS = pathlib.Path(BaseDirectory.save_config_path(DOMAIN_NAME))
except PermissionError:
    # Get the settings path without actually creating it
    DIR_SETTINGS = pathlib.Path(BaseDirectory.xdg_config_home) / DOMAIN_NAME
# Set the paths for the data files
FILE_ICON = DIR_DATA / icon_name
FILE_CONTRIBUTORS = DIR_DOCS / 'contributors'
FILE_TRANSLATORS = DIR_DOCS / 'translators'
FILE_LICENSE = DIR_DOCS / 'license'
FILE_RESOURCES = DIR_DOCS / 'resources'
# Set the paths for configuration files
FILE_SETTINGS = DIR_SETTINGS / 'settings.conf'
# Settings schema and paths
SCHEMA_FOLDERS = 'org.gnome.desktop.app-folders'
SCHEMA_FOLDER = f'{SCHEMA_FOLDERS}.folder'
