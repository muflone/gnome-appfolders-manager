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

from gettext import gettext, dgettext

localized_messages = {}


def store_message(message, translated):
    """Store a translated message in the localized_messages list"""
    localized_messages[message] = translated


def strip_colon(message):
    """Remove the colons from the message"""
    return message.replace(':', '')


def strip_underline(message):
    """Remove the underlines from the message"""
    return message.replace('_', '')


def text(message, gtk30=False, context=None):
    """Return a translated message and cache it for reuse"""
    if message not in localized_messages:
        if gtk30:
            # Get a message translated from GTK+ 3 domain
            full_message = message if not context else f'{context}\04{message}'
            localized_messages[message] = dgettext('gtk30', full_message)
            # Fix for untranslated messages with context
            if context and localized_messages[message] == full_message:
                localized_messages[message] = dgettext('gtk30', message)
        else:
            localized_messages[message] = gettext(message)
    return localized_messages[message]


def text_gtk30(message, context=None):
    """Return a translated text from GTK+ 3.0"""
    return text(message=message, gtk30=True, context=context)


# This special alias is used to track localization requests to catch
# by xgettext. The text() calls aren't tracked by xgettext
_ = text
