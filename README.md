GNOME App Folders Manager [![Build Status](https://travis-ci.org/muflone/gnome-appfolders-manager.svg?branch=master)](https://travis-ci.org/muflone/gnome-appfolders-manager)
=========================
**Description:** Manage GNOME Shell applications folders.

**Copyright:** 2016 Fabio Castelli (Muflone) <muflone(at)vbsimple.net>

**License:** GPL-2+

**Source code:** https://github.com/muflone/gnome-appfolders-manager

**Documentation:** http://www.muflone.com/gnome-appfolders-manager/

Usage
-----

From the *GNOME App Folders Manager* main window you can define your custom folders
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

System Requirements
-------------------

* Python 2.x (developed and tested for Python 2.7.5)
* GTK+ 3.0 libraries for Python 2.x
* GObject libraries for Python 2.x
* XDG library for Python 2.x
* Distutils library for Python 2.x (usually shipped with Python distribution)

Installation
------------

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python2 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python2 setup.py install --root NEW_PATH

Usage
-----

If the application is not installed please use:

    cd /path/to/folder
    python2 gnome-appfolders-manager.py

If the application was installed simply use the gnome-appfolders-manager
command.
