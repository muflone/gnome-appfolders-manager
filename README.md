# GNOME AppFolders Manager

[![Travis CI Build Status](https://img.shields.io/travis/com/muflone/gnome-appfolders-manager/master.svg)](https://www.travis-ci.com/github/muflone/gnome-appfolders-manager)
[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/gnome-appfolders-manager/master.svg)](https://circleci.com/gh/muflone/gnome-appfolders-manager)

**Description:** Manage GNOME Shell applications folders

**Copyright:** 2016-2022 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/gnome-appfolders-manager/

**Documentation:** http://www.muflone.com/gnome-appfolders-manager/

**Translations:** https://explore.transifex.com/muflone/gnome-appfolders-manager/

# Description

From the *GNOME AppFolders Manager* main window you can define your custom folders
to group your applications by clicking the **Create folder** button on the header bar.

![Main window](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/english/main.png)

Define the folder name and the folder title to show in GNOME Shell and confirm
the new folder by clicking the **Create folder** button.

![New folder](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/english/create-folder.png)

Add your wanted applications to the new folder by clicking the**add files**
button in the header bar, select the applications you want to include (multiple 
selection is also possible) and click the **Add applications** button.

![Application picker](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/english/add-applications.png)

Save your folder by clicking the **Save folder** button in the GNOME App Folders
Manager main window.

![Main window with new AppFolder](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/english/main-with-new-appfolder.png)

Open the GNOME Shell overview to use the new Application Folder.

![GNOME Shell overview](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/english/gnome-shell-appfolder.png)

# System Requirements

* Python >= 3.6 (developed and tested for Python 3.9 and 3.10)
* GTK+ 3.0 libraries for Python 3
* GObject libraries for Python 3 ( https://pypi.org/project/PyGObject/ )
* XDG library for Python 3 ( https://pypi.org/project/pyxdg/ )

# Installation

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python3 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python3 setup.py install --root NEW_PATH

# Usage

If the application is not installed please use:

    cd /path/to/folder
    python3 gnome-appfolders-manager.py

If the application was installed simply use the gnome-appfolders-manager
command.
