#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import itertools
import pathlib
import setuptools
import setuptools.command.install_scripts
import subprocess

# Importing distutils after setuptools uses the setuptools' distutils
from distutils.command.install_data import install_data

from gnome_appfolders_manager.constants import (APP_NAME,
                                                APP_VERSION,
                                                APP_DESCRIPTION,
                                                APP_AUTHOR,
                                                APP_AUTHOR_EMAIL,
                                                APP_URL,
                                                DOMAIN_NAME)


class Install_Scripts(setuptools.command.install_scripts.install_scripts):
    def run(self):
        setuptools.command.install_scripts.install_scripts.run(self)
        self.rename_python_scripts()

    def rename_python_scripts(self):
        "Rename main executable python script without .py extension"
        for script in self.get_outputs():
            path_file_script = pathlib.Path(script)
            path_destination = path_file_script.with_suffix(suffix='')
            if path_file_script.suffix == '.py':
                setuptools.distutils.log.info(
                    'renaming the python script '
                    f'{path_file_script.name} -> '
                    f'{path_destination.stem}')
                path_file_script.rename(path_destination)


class Install_Data(install_data):
    def run(self):
        self.install_icons()
        self.install_translations()
        install_data.run(self)

    def install_icons(self):
        setuptools.distutils.log.info('Installing icons...')
        DIR_ICONS = 'icons'
        path_icons = pathlib.Path('share') / 'icons' / 'hicolor'
        for path_format in pathlib.Path(DIR_ICONS).iterdir():
            self.data_files.append((path_icons / path_format.name / 'apps',
                                    list(map(str, path_format.glob('*')))))

    def install_translations(self):
        setuptools.distutils.log.info('Installing translations...')
        path_base = pathlib.Path(__file__).parent.absolute()
        path_build = pathlib.Path('build')
        path_locale = pathlib.Path('share') / 'locale'
        for path_file_po in pathlib.Path('po').glob('*.po'):
            path_destination = path_build / 'mo' / path_file_po.stem
            path_file_mo = path_destination / f'{DOMAIN_NAME}.mo'

            if not path_destination.exists():
                setuptools.distutils.log.info(f'creating {path_destination}')
                path_destination.mkdir(parents=True)

            setuptools.distutils.log.info(f'compiling {path_file_po} -> '
                                          f'{path_file_mo}')
            subprocess.call(
                args=('msgfmt',
                      f'--o={path_file_mo}',
                      path_file_po),
                cwd=path_base)

            path_destination = path_locale / path_file_po.stem / 'LC_MESSAGES'
            self.data_files.append((path_destination,
                                    [str(path_file_mo)]))


class Command_CreatePOT(setuptools.Command):
    description = "create base POT file"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.path_base = pathlib.Path(__file__).parent.absolute()
        self.path_po = self.path_base / 'po'

    def run(self):
        path_ui = self.path_base / 'ui'
        path_pot = self.path_po / f'{DOMAIN_NAME}.pot'
        list_files_process = []
        # Add *.ui files to list of files to process
        for filename in path_ui.glob('*.ui'):
            list_files_process.append(filename.relative_to(self.path_base))
        # Add *.py files to list of files to process
        for filename in self.path_base.rglob('*.py'):
            list_files_process.append(filename.relative_to(self.path_base))
        # Sort the files to process them always in the same order (hopefully)
        list_files_process.sort()
        # Extract messages from the files to process
        subprocess.call(
            args=itertools.chain(('xgettext',
                                  '--keyword=_',
                                  '--keyword=N_',
                                  f'--output={path_pot}',
                                  '--add-location',
                                  f'--package-name={APP_NAME}',
                                  f'--package-version={APP_VERSION}',
                                  f'--copyright-holder={APP_AUTHOR}',
                                  f'--msgid-bugs-address={APP_AUTHOR_EMAIL}'),
                                 list_files_process),
            cwd=self.path_base)


class Command_CreatePO(setuptools.Command):
    description = "create translation PO file"
    user_options = [
        ('locale=', None, 'Define locale'),
        ('output=', None, 'Define output file'),
        ]

    def initialize_options(self):
        self.locale = None
        self.output = None

    def finalize_options(self):
        self.path_base = pathlib.Path(__file__).parent.absolute()
        self.path_po = self.path_base / 'po'
        assert (self.locale), 'Missing locale'
        assert (self.output), 'Missing output file'

    def run(self):
        path_file_pot = self.path_po / f'{DOMAIN_NAME}.pot'
        path_file_po = self.path_po / f'{self.output}.po'
        # Create PO file
        subprocess.call(
            args=('msginit',
                  f'--input={path_file_pot}',
                  '--no-translator',
                  f'--output-file={path_file_po}',
                  f'--locale={self.locale}'),
            cwd=self.path_base)


class Command_Translations(setuptools.Command):
    description = "build translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.path_base = pathlib.Path(__file__).parent.absolute()
        self.path_po = self.path_base / 'po'
        self.path_mo = self.path_base / 'locale'

    def run(self):
        path_pot = self.path_po / f'{DOMAIN_NAME}.pot'
        for file_po in self.path_po.glob('*.po'):
            subprocess.call(('msgmerge',
                             '--update',
                             '--backup=off',
                             file_po,
                             path_pot))
            path_directory = self.path_mo / file_po.stem / 'LC_MESSAGES'
            file_mo = path_directory / f'{DOMAIN_NAME}.mo'
            if not path_directory.exists():
                path_directory.mkdir(parents=True)
            subprocess.call(('msgfmt',
                             '--output-file',
                             file_mo,
                             file_po))


setuptools.setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=APP_AUTHOR,
    author_email=APP_AUTHOR_EMAIL,
    maintainer=APP_AUTHOR,
    maintainer_email=APP_AUTHOR_EMAIL,
    url=APP_URL,
    description=APP_DESCRIPTION,
    license='GPL v3',
    scripts=['gnome-appfolders-manager.py'],
    packages=['gnome_appfolders_manager',
              'gnome_appfolders_manager.models',
              'gnome_appfolders_manager.ui'],
    data_files=[
        (f'share/{DOMAIN_NAME}/data',
            ['data/gnome-appfolders-manager.png']),
        ('share/applications',
            ['data/gnome-appfolders-manager.desktop']),
        (f'share/doc/{DOMAIN_NAME}',
            list(itertools.chain(
                list(map(str, pathlib.Path('doc').glob('*'))),
                list(map(str, pathlib.Path('.').glob('*.md')))))),
        (f'share/{DOMAIN_NAME}/ui', [str(file)
                                     for file
                                     in pathlib.Path('ui').glob('*')
                                     if not file.name.endswith('~')]),
    ],
    cmdclass={
        'install_scripts': Install_Scripts,
        'install_data': Install_Data,
        'create_pot': Command_CreatePOT,
        'create_po': Command_CreatePO,
        'translations': Command_Translations
    }
)
