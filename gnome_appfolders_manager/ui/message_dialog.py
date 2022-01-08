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

from gi.repository import Gtk


class UIMessageDialog(Gtk.Window):
    def __init__(self, parent, message_type, title, msg1, msg2,
                 buttons, default_response_id):
        """Prepare the message dialog"""
        self.dialog = Gtk.MessageDialog(parent=parent,
                                        flags=Gtk.DialogFlags.MODAL,
                                        message_type=message_type,
                                        buttons=buttons,
                                        title=title,
                                        message_format=msg1,
                                        secondary_text=msg2)
        if default_response_id:
            self.dialog.set_default_response(default_response_id)

    def show(self):
        """Show the dialog"""
        result = self.dialog.run()
        self.dialog.hide()
        return result

    def destroy(self):
        """Destroy the dialog"""
        self.dialog.destroy()
        self.dialog = None


class UIMessageDialogOK(UIMessageDialog):
    def __init__(self, parent, message_type, title, msg1, msg2):
        """Prepare the message dialog with an OK button"""
        UIMessageDialog.__init__(self,
                                 parent=parent,
                                 message_type=message_type,
                                 title=title,
                                 msg1=msg1,
                                 msg2=msg2,
                                 buttons=Gtk.ButtonsType.OK,
                                 default_response_id=Gtk.ResponseType.OK)


class UIMessageDialogOKCancel(UIMessageDialog):
    def __init__(self, parent, message_type, title, msg1, msg2):
        """Prepare the message dialog with OK and Cancel buttons"""
        UIMessageDialog.__init__(self,
                                 parent=parent,
                                 message_type=message_type,
                                 title=title,
                                 msg1=msg1,
                                 msg2=msg2,
                                 buttons=Gtk.ButtonsType.OK_CANCEL,
                                 default_response_id=Gtk.ResponseType.OK)


class UIMessageDialogCancelOK(UIMessageDialog):
    def __init__(self, parent, message_type, title, msg1, msg2):
        """Prepare the message dialog with Cancel and OK buttons"""
        UIMessageDialog.__init__(self,
                                 parent=parent,
                                 message_type=message_type,
                                 title=title,
                                 msg1=msg1,
                                 msg2=msg2,
                                 buttons=Gtk.ButtonsType.OK_CANCEL,
                                 default_response_id=Gtk.ResponseType.CANCEL)


class UIMessageDialogClose(UIMessageDialog):
    def __init__(self, parent, message_type, title, msg1, msg2):
        """Prepare the message dialog with a Close button"""
        UIMessageDialog.__init__(self,
                                 parent=parent,
                                 message_type=message_type,
                                 title=title,
                                 msg1=msg1,
                                 msg2=msg2,
                                 buttons=Gtk.ButtonsType.CLOSE,
                                 default_response_id=Gtk.ResponseType.CLOSE)


class UIMessageDialogYesNo(UIMessageDialog):
    def __init__(self, parent, message_type, title, msg1, msg2):
        """Prepare the message dialog with Yes and No buttons"""
        UIMessageDialog.__init__(self,
                                 parent=parent,
                                 message_type=message_type,
                                 title=title,
                                 msg1=msg1,
                                 msg2=msg2,
                                 buttons=Gtk.ButtonsType.YES_NO,
                                 default_response_id=Gtk.ResponseType.YES)


class UIMessageDialogNoYes(UIMessageDialog):
    def __init__(self, parent, message_type, title, msg1, msg2):
        """Prepare the message dialog with No and Yes buttons"""
        UIMessageDialog.__init__(self,
                                 parent=parent,
                                 message_type=message_type,
                                 title=title,
                                 msg1=msg1,
                                 msg2=msg2,
                                 buttons=Gtk.ButtonsType.YES_NO,
                                 default_response_id=Gtk.ResponseType.NO)


def show_message_dialog(class_, parent, message_type, title, msg1, msg2,
                        is_response_id=None):
    """Show a message dialog from its class"""
    dialog = class_(parent, message_type, title, msg1, msg2)
    response = dialog.show()
    dialog.destroy()
    if is_response_id is None:
        return response
    else:
        return response == is_response_id
