# Made by cvristophecvr
# Have quit nautilus on right click menu
# Terminates all nautilus sessions of current-user.
# This is missing on macos cause we do not have a menu for it.
# Minimum python version 3.X
# Tested on python 3.12, gtk3 with nautilus 3.38.2
# Should still work the day we merge to Gtk4 nautilus 4.x


import os
import subprocess
from urllib.parse import unquote
from gi.repository import Nautilus, Gtk, GObject
from typing import List
# version used to make it compatible with nautilus 3.x (gtk 3) and nautilus 4.x (gtk 4)
version = Nautilus._version

class QuitNautilus(GObject.GObject, Nautilus.MenuProvider):
    def _quit_nautilus(self, file: Nautilus.FileInfo) -> None:
        current_user = os.environ["USER"]
        os.system("killall -u " + current_user + " nautilus")

    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._quit_nautilus(file)

    def menu_background_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._quit_nautilus(file)
    
    if version == "3.0":
        def get_file_items(
            self,
            # added window, needed for gtk-3 version nautilus versions 3.x
            window,
            files: List[Nautilus.FileInfo],
        ) -> List[Nautilus.MenuItem]:
            item = Nautilus.MenuItem(
                name="QuitNautilus::quit_nautilus",
                label="QUIT NAUTILUS",
                tip="")
            item.connect("activate", self.menu_activate_cb, files)

            return [item]
    else:
        # for gtk-4 version nautilus versions 4.x
        def get_file_items(
            self,
            files: List[Nautilus.FileInfo],
        ) -> List[Nautilus.MenuItem]:
            item = Nautilus.MenuItem(
                name="QuitNautilus::quit_nautilus",
                label="QUIT NAUTILUS",
                tip="")
            item.connect("activate", self.menu_activate_cb, files)

            return [item]

    if version == "3.0":
        def get_background_items(
            self,
            # added window, needed for gtk-3 nautilus 3.x versions
            window,
            current_folder: Nautilus.FileInfo,
        ) -> List[Nautilus.MenuItem]:
            item = Nautilus.MenuItem(
                name="QuitNautilus::quit_nautilus2",
                label="QUIT NAUTILUS",
                tip="")
            item.connect("activate", self.menu_background_activate_cb, current_folder)

            return [item]
    else:
        # for gtk-4 version nautilus ver 4.x versions
        def get_background_items(
            self,
            current_folder: Nautilus.FileInfo,
        ) -> List[Nautilus.MenuItem]:
            item = Nautilus.MenuItem(
                name="QuitNautilus::quit_nautilus2",
                label="QUIT NAUTILUS",
                tip="")
            item.connect("activate", self.menu_background_activate_cb, current_folder)

            return [item]

