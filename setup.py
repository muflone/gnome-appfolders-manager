#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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

from distutils.core import setup, Command
from distutils.command.install_scripts import install_scripts
from distutils.command.install_data import install_data
from distutils.log import info

import os
import os.path
import shutil
import subprocess
from itertools import chain
from glob import glob

from gnome_appfolders_manager.functions import recursive_glob
from gnome_appfolders_manager.constants import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    APP_AUTHOR, APP_AUTHOR_EMAIL, APP_URL,
    DOMAIN_NAME)


class Install_Scripts(install_scripts):
    def run(self):
        install_scripts.run(self)
        self.rename_python_scripts()

    def rename_python_scripts(self):
        "Rename main executable python script without .py extension"
        for script in self.get_outputs():
            if script.endswith(".py"):
                info('renaming the python script %s -> %s' % (
                    script, script[:-3]))
                shutil.move(script, script[:-3])


class Install_Data(install_data):
    def run(self):
        self.install_icons()
        self.install_translations()
        install_data.run(self)

    def install_icons(self):
        info('Installing icons...')
        DIR_ICONS = 'icons'
        for icon_format in os.listdir(DIR_ICONS):
            icon_dir = os.path.join(DIR_ICONS, icon_format)
            self.data_files.append((
                os.path.join('share', 'icons', 'hicolor', icon_format, 'apps'),
                glob(os.path.join(icon_dir, '*'))))

    def install_translations(self):
        info('Installing translations...')
        for po in glob(os.path.join('po', '*.po')):
            lang = os.path.basename(po[:-3])
            mo = os.path.join('build', 'mo', lang, '%s.mo' % DOMAIN_NAME)

            directory = os.path.dirname(mo)
            if not os.path.exists(directory):
                info('creating %s' % directory)
                os.makedirs(directory)

            cmd = 'msgfmt -o %s %s' % (mo, po)
            info('compiling %s -> %s' % (po, mo))
            if os.system(cmd) != 0:
                raise SystemExit('Error while running msgfmt')

            dest = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            self.data_files.append((dest, [mo]))


class Command_CreatePOT(Command):
    description = "create base POT file"
    user_options = [
        ('use-intltool-extract', None, 'Use intltool-extract'),
        ('keep-headers', None, 'Do not delete header files'),
        ]
    boolean_options = ('use-intltool-extract')

    def initialize_options(self):
        self.use_intltool_extract = False
        self.keep_headers = False

    def finalize_options(self):
        self.dir_base = os.path.dirname(os.path.abspath(__file__))
        self.dir_po = os.path.join(self.dir_base, 'po')

    def run(self):
        self.dir_ui = os.path.join(self.dir_base, 'ui')
        file_pot = '%s.pot' % os.path.join(self.dir_po, DOMAIN_NAME)
        list_files_process = []
        list_files_remove = []
        if self.use_intltool_extract:
            # Scan *.ui files to extract messages
            for filename in glob(os.path.join(self.dir_ui, '*.ui')):
                header_file = '%s.h' % filename
                # Clear previous existing files
                if os.path.isfile(header_file):
                    os.unlink(header_file)
                # Extract data from the interface files
                subprocess.call(args=('intltool-extract',
                                      '--quiet',
                                      '--type=gettext/glade',
                                      os.path.basename(filename)),
                                cwd=os.path.dirname(filename))
                if os.path.getsize(header_file) > 0:
                    # Add the header files to the list of the files to process
                    list_files_process.append(os.path.relpath(header_file,
                                                              self.dir_base))
                # All the header files must be removed after the process
                list_files_remove.append(header_file)
        else:
            # Add *.ui files to list of files to process
            for filename in glob(os.path.join(self.dir_ui, '*.ui')):
                list_files_process.append(os.path.relpath(filename,
                                                          self.dir_base))
        # Add *.py files to list of files to process
        for filename in recursive_glob(self.dir_base, '*.py'):
            list_files_process.append(os.path.relpath(filename,
                                                      self.dir_base))
        # Extract messages from the files to process
        subprocess.call(
            args=chain(('xgettext',
                        '--keyword=_',
                        '--keyword=N_',
                        '--output=%s' % file_pot,
                        '--add-location',
                        '--package-name=%s' % APP_NAME,
                        '--package-version=%s' % APP_VERSION,
                        '--copyright-holder=%s' % APP_AUTHOR,
                        '--msgid-bugs-address=%s' % APP_AUTHOR_EMAIL),
                       list_files_process),
            cwd=self.dir_base)
        # Remove uneeded files if requested
        if not self.keep_headers:
            for filename in list_files_remove:
                if os.path.isfile(filename):
                    os.unlink(filename)


class Command_CreatePO(Command):
    description = "create translation PO file"
    user_options = [
        ('locale=', None, 'Define locale'),
        ('output=', None, 'Define output file'),
        ]

    def initialize_options(self):
        self.locale = None
        self.output = None

    def finalize_options(self):
        self.dir_base = os.path.dirname(os.path.abspath(__file__))
        self.dir_po = os.path.join(self.dir_base, 'po')
        assert (self.locale), 'Missing locale'
        assert (self.output), 'Missing output file'

    def run(self):
        self.dir_ui = os.path.join(self.dir_base, 'ui')
        file_pot = '%s.pot' % os.path.join(self.dir_po, DOMAIN_NAME)
        file_po = '%s.po' % os.path.join(self.dir_po, self.output)
        # Create PO file
        subprocess.call(
            args=('msginit',
                  '--input=%s' % file_pot,
                  '--no-translator',
                  '--output-file=%s' % file_po,
                  '--locale=%s' % self.locale),
            cwd=self.dir_base)


class Command_Translations(Command):
    description = "build translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.dir_base = os.path.dirname(os.path.abspath(__file__))
        self.dir_po = os.path.join(self.dir_base, 'po')
        self.dir_mo = os.path.join(self.dir_base, 'locale')

    def run(self):
        file_pot = '%s.pot' % os.path.join(self.dir_po, DOMAIN_NAME)
        for file_po in glob(os.path.join(self.dir_po, '*.po')):
            subprocess.call(('msgmerge', '--update', '--backup=off',
                             file_po, file_pot))
            lang = os.path.basename(file_po[:-3])
            file_mo = os.path.join(self.dir_mo, lang, 'LC_MESSAGES',
                                   '%s.mo' % DOMAIN_NAME)
            dir_lang = os.path.dirname(file_mo)
            if not os.path.exists(dir_lang):
                os.makedirs(dir_lang)
            subprocess.call(('msgfmt', '--output-file', file_mo, file_po))


setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=APP_AUTHOR,
    author_email=APP_AUTHOR_EMAIL,
    maintainer=APP_AUTHOR,
    maintainer_email=APP_AUTHOR_EMAIL,
    url=APP_URL,
    description=APP_DESCRIPTION,
    license='GPL v2',
    scripts=['gnome-appfolders-manager.py'],
    packages=['gnome_appfolders_manager', 'gnome_appfolders_manager.models',
              'gnome_appfolders_manager.ui'],
    data_files=[
        ('share/gnome-appfolders-manager/data',
            ['data/gnome-appfolders-manager.png']),
        ('share/applications',
            ['data/gnome-appfolders-manager.desktop']),
        ('share/doc/gnome-appfolders-manager',
            list(chain(glob('doc/*'), glob('*.md')))),
        ('share/gnome-appfolders-manager/ui',
            glob('ui/*')),
    ],
    cmdclass={
        'install_scripts': Install_Scripts,
        'install_data': Install_Data,
        'create_pot': Command_CreatePOT,
        'create_po': Command_CreatePO,
        'translations': Command_Translations
    }
)
