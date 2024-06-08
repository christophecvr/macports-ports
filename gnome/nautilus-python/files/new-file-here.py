# Made by christophecvr
# Plugin to open new file at current location
# Or selected map
# For python 3.10 or higher
# Nautilus 3.38.2 (gtk3). Should work on nautilus 4.x (Gtk4)

#import os, subprocess
from pathlib import Path
from urllib.parse import unquote
from gi.repository import Nautilus, Gtk, GObject
from typing import List
# version used to make it compatible with nautilus 3.x (gtk 3) and nautilus 4.x (gtk 4)
version = Nautilus._version

class NewFileHereExtension(GObject.GObject, Nautilus.MenuProvider):
# Actions to perform on activate
    def _new_empty_file(self, file) -> None:
        filename = Path(unquote(file.get_uri()[7:])).joinpath("new-empty-file.txt")
        if not filename.is_file():
            #print("file " + str(filename) + " will be made")
            file_open = open(filename, "a")
            file_open.close()
        #else:
           # print("we do not make file " + str(filename))


# menu activate.
    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file) -> None:
        self._new_empty_file(file)

    def menu_background_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file) -> None:
        self._new_empty_file(file)

# Menu's defines
    if version == "3.0":
        def get_file_items(
            self,
            # added window, needed for gtk-3 version nautilus versions 3.x
            window,
            files: List[Nautilus.FileInfo]
            ) -> List[Nautilus.MenuItem]:
            # Only one item maybe selected.
            if len(files) != 1:
                return []

            file = files[0]
            # Selection can only be a map.
            if not file.is_directory() or file.get_uri_scheme() != "file":
                return []

            top_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewFileInMap",
                label="New File In Selected Map",
                tip="",
                icon="")

            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)

            sub_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewEmptyFile",
                label="New Empty File",
                tip="",
                icon="")
            submenu.append_item(sub_menuitem)
            sub_menuitem.connect("activate", self.menu_activate_cb, file)

            return [top_menuitem]

        def get_background_items(
            self,
            # added window, needed for gtk-3 version nautilus versions 3.x
            window,
            current_folder: Nautilus.FileInfo
            ) -> List[Nautilus.MenuItem]:
            top_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewFileHere",
                label="New File Here",
                tip="",
                icon="")

            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)

            sub_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewEmptyFile",
                label="New Empty File",
                tip="",
                icon="")
            submenu.append_item(sub_menuitem)
            sub_menuitem.connect("activate", self.menu_background_activate_cb, current_folder)

            return [top_menuitem]
    else:
        # for gtk-4 version nautilus versions 4.x
        def get_file_items(
            self,
            files: List[Nautilus.FileInfo]
            ) -> List[Nautilus.MenuItem]:
            # Only one item can be selected
            if len(files) != 1:
                return []

            file = files[0]
            # Selection must be a map.
            if not file.is_directory() or file.get_uri_scheme() != "file":
                return []

            top_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewFileInMap",
                label="New File In Selected Map",
                tip="",
                icon="")

            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)

            sub_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewEmptyFile",
                label="New Empty File",
                tip="",
                icon="")
            submenu.append_item(sub_menuitem)
            sub_menuitem.connect("activate", self.menu_activate_cb, file)

            return [top_menuitem]

        def get_background_items(
            self,
            current_folder: Nautilus.FileInfo
            ) -> List[Nautilus.MenuItem]:
            top_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewFileHere",
                label="New File Here",
                tip="",
                icon="")

            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)

            sub_menuitem = Nautilus.MenuItem(
                name="NewFileHereExtension::NewEmptyFile",
                label="New Empty File",
                tip="",
                icon="")
            submenu.append_item(sub_menuitem)
            sub_menuitem.connect("activate", self.menu_background_activate_cb, current_folder)

            return [top_menuitem]







