GNOME App Folders Manager [![Build Status](https://travis-ci.org/muflone/gnome-appfolders-manager.svg?branch=master)](https://travis-ci.org/muflone/gnome-appfolders-manager)
=========================
**Descrizione:** Gestisci le cartelle delle applicazioni su GNOME Shell.

**Copyright:** 2016 Fabio Castelli (Muflone) <muflone(at)vbsimple.net>

**Licenza:** GPL-2+

**Codice sorgente:** https://github.com/muflone/gnome-appfolders-manager

**Documentazione:** http://www.muflone.com/gnome-appfolders-manager/

Utilizzo
--------

Dalla finestra principale di *GNOME App Folders Manager* è possibile definire
le cartelle personalizzate per raggruppare le applicazioni cliccando il pulsante
**Crea cartella** sulla barra di intestazione.

![Finestra principale](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/italian/main.png)

Definire il nome della cartella e il titolo da mostrare nella shell di GNOME e
confermare la nuova cartella cliccando il pulsante **Crea cartella**.

![Nuova cartella](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/italian/create-folder.png)

Aggiungere le applicazioni desiderate alla nuova cartella cliccando il pulsante
**Nuovo file** sulla barra di intestazione, selezionare le applicazioni da
includere (la selezione multipla è anche possibile) e cliccare il pulsante
**Aggiungi applicazioni**.

![Application picker](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/italian/add-applications.png)

Salvare la cartella cliccando il pulsante **Salva cartella** nella finestra
principale di GNOME App Folders Manager.

![Finestra principale con una nuova cartella](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/english/main-with-new-appfolder.png)

Aprire la finestra delle attività di GNOME Shell per utilizzare la nuova
cartella delle applicazioni.

![GNOME Shell overview](http://www.muflone.com/resources/gnome-appfolders-manager/archive/latest/italian/gnome-shell-appfolder.png)

Requisiti di sistema
--------------------

* Python 2.x (sviluppato e testato per Python 2.7.5)
* Libreria GTK+ 3.0 per Python 2.x
* Libreria GObject per Python 2.x
* Libreria XDG per Python 2.x
* Libreria Distutils per Python 2.x (generalmente fornita col pacchetto Python)

Installazione
-------------

E' disponibile uno script di installazione distutils per installare da sorgenti.

Per installare nel tuo sistema utilizzare:

    cd /percorso/alla/cartella
    python2 setup.py install

Per installare i files in un altro percorso invece del prefisso /usr standard
usare:

    cd /percorso/alla/cartella
    python2 setup.py install --root NUOVO_PERCORSO

Utilizzo
--------

Se l'applicazione non è stata installata utilizzare:

    cd /path/to/folder
    python2 gnome-appfolders-manager.py

Se l'applicazione è stata installata utilizzare semplicemente il comando
gnome-appfolders-manager.
