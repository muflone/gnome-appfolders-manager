#!/usr/bin/env python3
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

import itertools
import pathlib
import setuptools
import setuptools.command.install_scripts
import subprocess

# Importing distutils after setuptools uses the setuptools' distutils
from distutils.command.install_data import install_data

from gnome_appfolders_manager.constants import (APP_AUTHOR,
                                                APP_AUTHOR_EMAIL,
                                                APP_DESCRIPTION,
                                                APP_NAME,
                                                APP_URL,
                                                APP_VERSION,
                                                DOMAIN_NAME,
                                                SOURCES_URL)


class InstallScripts(setuptools.command.install_scripts.install_scripts):
    def run(self):
        setuptools.command.install_scripts.install_scripts.run(self)
        self.rename_python_scripts()

    def rename_python_scripts(self):
        """Rename main executable python script without .py extension"""
        for script in self.get_outputs():
            path_file_script = pathlib.Path(script)
            path_destination = path_file_script.with_suffix(suffix='')
            if path_file_script.suffix == '.py':
                # noinspection PyUnresolvedReferences
                setuptools.distutils.log.info(
                    'renaming the python script '
                    f'{path_file_script.name} -> '
                    f'{path_destination.stem}')
                path_file_script.rename(path_destination)


class InstallData(install_data):
    def run(self):
        self.install_icons()
        self.install_translations()
        install_data.run(self)

    def install_icons(self):
        # noinspection PyUnresolvedReferences
        setuptools.distutils.log.info('Installing icons...')
        path_icons = pathlib.Path('share') / 'icons' / 'hicolor'
        for path_format in pathlib.Path('icons').iterdir():
            self.data_files.append((path_icons / path_format.name / 'apps',
                                    list(map(str, path_format.glob('*')))))

    def install_translations(self):
        # noinspection PyUnresolvedReferences
        setuptools.distutils.log.info('Installing translations...')
        path_base = pathlib.Path(__file__).parent.absolute()
        # Find where to save the compiled translations
        try:
            # Use the install_data (when using "setup.py install --user")
            # noinspection PyUnresolvedReferences
            path_install = pathlib.Path(self.install_data)
        except AttributeError:
            # Use the install_dir (when using "setup.py install")
            path_install = pathlib.Path(self.install_dir)
        path_locale = path_install / 'share' / 'locale'
        for path_file_po in pathlib.Path('po').glob('*.po'):
            path_destination = path_locale / path_file_po.stem / 'LC_MESSAGES'
            path_file_mo = path_destination / f'{DOMAIN_NAME}.mo'

            if not path_destination.exists():
                # noinspection PyUnresolvedReferences
                setuptools.distutils.log.info(f'creating {path_destination}')
                path_destination.mkdir(parents=True)

            # noinspection PyUnresolvedReferences
            setuptools.distutils.log.info(f'compiling {path_file_po} -> '
                                          f'{path_file_mo}')
            subprocess.call(
                args=('msgfmt',
                      f'--output-file={path_file_mo}',
                      path_file_po),
                cwd=path_base)


class CommandCreatePOT(setuptools.Command):
    description = "create base POT file"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path_base = pathlib.Path(__file__).parent.absolute()
        path_po = path_base / 'po'
        path_ui = path_base / 'ui'
        path_pot = path_po / f'{DOMAIN_NAME}.pot'
        list_files_process = []
        # Add *.ui files to list of files to process
        for filename in path_ui.glob('*.ui'):
            list_files_process.append(filename.relative_to(path_base))
        # Add *.py files to list of files to process
        for filename in path_base.rglob('*.py'):
            list_files_process.append(filename.relative_to(path_base))
        # Sort the files to process them always in the same order (hopefully)
        list_files_process.sort()
        # Extract messages from the files to process
        # noinspection PyTypeChecker
        subprocess.call(
            args=itertools.chain((
                'xgettext',
                '--keyword=_',
                '--keyword=N_',
                f'--output={path_pot}',
                '--add-location',
                f'--package-name={APP_NAME}',
                f'--copyright-holder={APP_AUTHOR}',
                f'--msgid-bugs-address={SOURCES_URL}/issues'),
                list_files_process),
            cwd=path_base)


class CommandCreatePO(setuptools.Command):
    description = "create translation PO file"
    user_options = [
        ('locale=', None, 'Define locale'),
        ('output=', None, 'Define output file'),
        ]

    # noinspection PyUnusedLocal
    def __init__(self, dist, **kw):
        super().__init__(dist)
        self.locale = None
        self.output = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        assert self.locale, 'Missing locale'
        assert self.output, 'Missing output file'

    def run(self):
        path_base = pathlib.Path(__file__).parent.absolute()
        path_file_pot = path_base / 'po' / f'{DOMAIN_NAME}.pot'
        path_file_po = path_base / 'po' / f'{self.output}.po'
        # Create PO file
        subprocess.call(
            args=('msginit',
                  f'--input={path_file_pot}',
                  '--no-translator',
                  f'--output-file={path_file_po}',
                  f'--locale={self.locale}'),
            cwd=path_base)


class CommandTranslations(setuptools.Command):
    description = "build translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        path_base = pathlib.Path(__file__).parent.absolute()
        path_po = path_base / 'po'
        for file_po in path_po.glob('*.po'):
            subprocess.call(('msgmerge',
                             '--update',
                             '--backup=off',
                             file_po,
                             path_po / f'{DOMAIN_NAME}.pot'))
            path_mo = path_base / 'locale' / file_po.stem / 'LC_MESSAGES'
            if not path_mo.exists():
                path_mo.mkdir(parents=True)
            file_mo = path_mo / f'{DOMAIN_NAME}.mo'
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
        ('share/metainfo',
         ['data/com.muflone.gnome-appfolders-manager.metainfo.xml']),
    ],
    cmdclass={
        'install_scripts': InstallScripts,
        'install_data': InstallData,
        'create_pot': CommandCreatePOT,
        'create_po': CommandCreatePO,
        'translations': CommandTranslations
    }
)
