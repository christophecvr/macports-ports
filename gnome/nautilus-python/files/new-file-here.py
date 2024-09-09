# Made by christophecvr
# Plugin to open new file at current location
# Or selected map
# For python 3.12 or higher
# Nautilus 3.38.2 (gtk3).
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Nautilus", "3.0")
import os, subprocess, sys, distutils.spawn
from sys import platform
from pathlib import Path
from urllib.parse import unquote
from gi.repository import GObject, GLib
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from gi.repository import Nautilus
from typing import List

# Not really required in python but so can be easely seen
# What type of variables the globals are. And to remind
# Other developpers or myself the day Extra changes are made
# To always reset the globals. The base plugin is loaded on start
# Of nautilus.
######## Some globals #############
# - File names or paths
global_entered_filename = ""
global_full_filename = Path("")
# - Gtk window Widgets
global_window = None
global_window_default_widget = None
######### End globals #############


class Entry(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Enter desired filename and press enter")  
        self.set_default_size(500, 50)
        self.set_border_width(10)
        self.connect("destroy", Gtk.main_quit)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Entry text here...")
        entry.connect("activate", self.on_entry_activated)
        self.add(entry)

    def on_entry_activated(self, entry):
        global global_entered_filename
        global_entered_filename = entry.get_text()
        self.destroy()

class SelectionMenu(Gtk.Window):
    # if connected closing of this menu is possible with esc key
    def on_esc_key_press(self, widget, ev):
        if ev.keyval == Gdk.KEY_Escape:
            self.destroy()

    def __init__(self, file):
        # get posix form of file in Path form if needed we always can 
        # cast is to string with str() .
        file_path = Path(unquote(file.get_uri()[7:]))
        Gtk.Window.__init__(self)
        self.set_title("Select File Extention")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_decorated(True)
        self.set_default_size(500, 300)
        self.connect("destroy", self.destroy_SelectionMenu)
        # main box will expand vertical for labels and parent(childs)
        main_box = Gtk.Box()
        main_box.set_orientation(Gtk.Orientation.VERTICAL)
        main_box.set_homogeneous(False)
        main_box.set_spacing(10)
        self.add(main_box)
        startlabel = Gtk.Label()
        # Below how to change text with pango markups
        startlabel.set_markup(
        "<span foreground='blue' size='x-large' weight='bold' underline='single'>"
        "File will be created in path:\n\n" 
        + str(file_path) + 
        "\n\nwith the selected extention."
        "</span>")
        main_box.pack_start(startlabel, True, True, 0)
        # row 1 will expand horizontal and is child1 of main_box
        row_1 = Gtk.Box()
        row_1.set_orientation(Gtk.Orientation.HORIZONTAL)
        row_1.set_homogeneous(True)
        row_1.set_spacing(5)
        main_box.add(row_1)
        button_none = Gtk.Button(label="NONE")
        row_1.pack_start(button_none, True, True, 0)
        button_txt = Gtk.Button(label=".txt")
        row_1.pack_start(button_txt, True, True, 0)
        button_sh = Gtk.Button(label=".sh")
        row_1.pack_start(button_sh, True, True, 0)
        # row 2 will expand horizontal and is child2 of main_box        
        row_2 = Gtk.Box()
        row_2.set_orientation(Gtk.Orientation.HORIZONTAL)
        row_2.set_homogeneous(True)
        row_2.set_spacing(5)
        main_box.add(row_2)
        button_py = Gtk.Button(label=".py")
        row_2.pack_start(button_py, True, True, 0)
        button_odt = Gtk.Button(label=".odt")
        row_2.pack_start(button_odt, True, True, 0)
        button_ods = Gtk.Button(label=".ods")
        row_2.pack_start(button_ods, True, True, 0)
        # row 3 will expand horizontal and is child3 of main_box        
        row_3 = Gtk.Box()
        row_3.set_orientation(Gtk.Orientation.HORIZONTAL)
        row_3.set_homogeneous(True)
        row_3.set_spacing(5)
        main_box.add(row_3)
        button_portfile = Gtk.Button(label="Portfile")
        row_3.pack_start(button_portfile, True, True, 0)
        button_c = Gtk.Button(label=".c")
        row_3.pack_start(button_c, True, True, 0)
        button_h = Gtk.Button(label=".h")
        row_3.pack_start(button_h, True, True, 0)
        # row last with one button close and is last child of main_box
        row_last = Gtk.Box()
        row_last.set_orientation(Gtk.Orientation.HORIZONTAL)
        row_last.set_homogeneous(True)
        row_last.set_spacing(5)
        main_box.add(row_last)
        button_close = Gtk.Button(label="CLOSE MENU")
        row_last.pack_start(button_close, True, True, 0)
        
        


        # connects to function windows and actions
        button_none.connect("clicked", self.on_none_clicked, file_path)
        button_txt.connect("clicked", self.on_txt_clicked, file_path)
        button_sh.connect("clicked", self.on_sh_clicked, file_path)
        button_py.connect("clicked", self.on_py_clicked, file_path)
        button_odt.connect("clicked", self.on_odt_clicked, file_path)
        button_ods.connect("clicked", self.on_ods_clicked, file_path)
        button_portfile.connect("clicked", self.on_portfile_clicked, file_path)
        button_c.connect("clicked", self.on_c_clicked, file_path)
        button_h.connect("clicked", self.on_h_clicked, file_path)
        button_close.connect("clicked", self.on_close_clicked)

    def destroy_SelectionMenu(self, widget):
        global global_entered_filename
        global global_full_filename
        global global_window
        global global_window_default_widget
        global_entered_filename = ""
        global_full_filename = Path("")
        global_window = None
        global_window_default_widget = None
        Gtk.main_quit()

    def on_none_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty file without extention",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            #entry_window.destroy()
            if not global_entered_filename == "":
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                else:
                    file_open = open(global_full_filename, "a")
                    file_open.close()
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()

        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_txt_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty .txt file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog and get the response wait for max 10 seconds
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            if not global_entered_filename == "":
                global_entered_filename = global_entered_filename + ".txt"
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                rc = 0
                rcmac = 0
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with gedit"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build gedit version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit ... Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with Gedit"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                        global_entered_filename = ""
                        global_full_filename = Path("")
                        self.destroy()
                else:
                    file_open = open(global_full_filename, "a")
                    file_open.close()
                    rc = 0
                    rcmac = 0
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit ...  Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with Gedit"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_sh_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty .sh file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog and get the response wait for max 10 seconds
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            if not global_entered_filename == "":
                global_entered_filename = global_entered_filename + ".sh"
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                rc = 0
                rcmac = 0
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with Gedit"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build gedit version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit-Teksteditor Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit-Teksteditor Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with Gedit "
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                        global_entered_filename = ""
                        global_full_filename = Path("")
                        self.destroy()
                else:
                    file_open = open(global_full_filename, "w")
                    # adding #!/bin/sh at start of script
                    file_open.write("#!/bin/sh\n ")
                    file_open.close()
                    # making this file executable.
                    os.system("chmod +x " + str(global_full_filename))
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build gedit version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app " +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit-Teksteditor Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit-Teksteditor Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with Gedit"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_py_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty .py file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog and get the response wait for max 10 seconds
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            if not global_entered_filename == "":
                global_entered_filename = global_entered_filename + ".py"
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                rc = 0
                rcmac = 0
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with Gedit"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build gedit version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit-Teksteditor Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit-Teksteditor Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with Gedit-Teksteditor"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                        global_entered_filename = ""
                        global_full_filename = Path("")
                        self.destroy()
                else:
                    file_open = open(global_full_filename, "a")
                    file_open.close()
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build gedit version was found
                            if platform == "darwin":
                                #print("Try to open file Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("LibreOffice Not Found her comes msg box and menu destroy")
                            primary_msg = "LibreOffice Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with Gedit-Teksteditor"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_odt_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty .odt file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            if not global_entered_filename == "":
                global_entered_filename = global_entered_filename + ".odt"
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                rc = 0
                rcmac = 0
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with libreoffice"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'libreoffice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'libreoffice']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                            if platform == "darwin":
                                #print("Try to open file with LibreOffice.app" +str(global_full_filename))
                                rcmac = os.system("open -a LibreOffice '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("LibreOffice Not Found her comes msg box and menu destroy")
                            primary_msg = "LibreOffice Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with LibreOffice"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                        global_entered_filename = ""
                        global_full_filename = Path("")
                        self.destroy()
                else:
                    file_open = open(global_full_filename, "a")
                    file_open.close()
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'libreoffice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'libreoffice']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                            if platform == "darwin":
                                #print("Try to open file with LibreOffice.app" +str(global_full_filename))
                                rcmac = os.system("open -a LibreOffice '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("LibreOffice Not Found her comes msg box and menu destroy")
                            primary_msg = "LibreOffice Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with LibreOffice"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()
            global_entered_filename = ""
            global_full_filename = Path("")
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_ods_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty .ods file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            if not global_entered_filename == "":
                global_entered_filename = global_entered_filename + ".ods"
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                rc = 0
                rcmac =0
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with libreoffice"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'libreoffice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'libreoffice']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                            if platform == "darwin":
                                #print("Try to open file with LibreOffice.app" +str(global_full_filename))
                                rcmac = os.system("open -a LibreOffice '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("LibreOffice Not Found her comes msg box and menu destroy")
                            primary_msg = "LibreOffice Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with LibreOffice"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                        global_entered_filename = ""
                        global_full_filename = Path("")
                        self.destroy()
                else:
                    file_open = open(global_full_filename, "a")
                    file_open.close()
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'libreoffice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'libreoffice']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                            if platform == "darwin":
                                #print("Try to open file with LibreOffice.app" +str(global_full_filename))
                                rcmac = os.system("open -a LibreOffice '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("LibreOffice Not Found her comes msg box and menu destroy")
                            primary_msg = "LibreOffice Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with LibreOffice"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_portfile_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty Portfile file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog and get the response wait for max 10 seconds
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            #print("file_path is : " + str(file_path))
            global_full_filename = file_path.joinpath("Portfile")
            if global_full_filename.exists():
                primary_msg = "File Already Exists \n" + str(global_full_filename)
                secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with gedit"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                if platform == "linux" or platform == "darwin":
                    rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if rc == 0:
                        app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                        os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                    else:
                        # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                        if platform == "darwin":
                            #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                            rcmac = os.system("open -a Gedit-Teksteditor " + str(global_full_filename) + "&> /dev/null")
                    if (rc != 0 and rcmac != 0):
                        #print("Gedit Not Found her comes msg box and menu destroy")
                        primary_msg = "Gedit ... Application Not Found on You're System"
                        secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with Gedit"
                        self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                global_entered_filename = ""
                global_full_filename = Path("")
                self.destroy()
            else:
                file_open = open(global_full_filename, "a")
                file_open.write("# -*- coding: utf-8; mode: tcl; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- vim:fenc=utf-8:ft=tcl:et:sw=4:ts=4:sts=4\n")
                file_open.write("\n")
                file_open.close()
                rc = 0
                rcmac = 0
                # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                if platform == "linux" or platform == "darwin":
                    rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if rc == 0:
                        app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                        os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                    else:
                        # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                        if platform == "darwin":
                            #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                            rcmac = os.system("open -a Gedit-Teksteditor " + str(global_full_filename) + "&> /dev/null")
                    if (rc != 0 and rcmac != 0):
                        #print("Gedit Not Found her comes msg box and menu destroy")
                        primary_msg = "Gedit ...  Application Not Found on You're System"
                        secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with Gedit"
                        self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                global_entered_filename = ""
                global_full_filename = Path("")
                self.destroy()               
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_c_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty .c file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog and get the response wait for max 10 seconds
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            if not global_entered_filename == "":
                global_entered_filename = global_entered_filename + ".c"
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                rc = 0
                rcmac = 0
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with gedit"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build gedit version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit ... Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with Gedit"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                        global_entered_filename = ""
                        global_full_filename = Path("")
                        self.destroy()
                else:
                    file_open = open(global_full_filename, "a")
                    file_open.close()
                    rc = 0
                    rcmac = 0
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit ...  Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with Gedit"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")

    def on_h_clicked(self, widget, file_path):
        global global_entered_filename
        global global_full_filename
        dialog = Gtk.MessageDialog(
            self,
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK_CANCEL,
            "To create empty .h file",
        )
        dialog.format_secondary_text(
            "Click OK to continu or CANCEL to abort)"
        )
        image = Gtk.Image()
        # still works but is deprecated
        #image.set_from_stock(Gtk.STOCK_DIALOG_INFO, Gtk.IconSize.DIALOG)
        # using linux icons adwaita theme instead of icons from stock
        image.set_from_icon_name ("dialog-information-symbolic", Gtk.IconSize.DIALOG)
        image.show()
        dialog.set_image(image)
        GLib.timeout_add_seconds(10,dialog.destroy)
        # run/show the messagedialog and get the response wait for max 10 seconds
        dialog_response = dialog.run()
        if dialog_response == Gtk.ResponseType.OK:
            dialog.destroy()
            entry_window = Entry()
            entry_window.show_all()
            Gtk.main()
            if not global_entered_filename == "":
                global_entered_filename = global_entered_filename + ".h"
                #print("Entered file name is: " + global_entered_filename)
                global_full_filename = file_path.joinpath(global_entered_filename)
                rc = 0
                rcmac = 0
                if global_full_filename.exists():
                    #print("SORRY FILE ALREADY EXISTS MSG ERROR BOX HERE AND BACK TO MENU")
                    primary_msg = "File Already Exists"
                    secondary_msg = "File :\n" + str(global_full_filename) + "\nNot Made !\nTry opening existing file with gedit"
                    self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build libreoffice version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit ... Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nExists but not opened with Gedit"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                        global_entered_filename = ""
                        global_full_filename = Path("")
                        self.destroy()
                else:
                    file_open = open(global_full_filename, "a")
                    file_open.close()
                    rc = 0
                    rcmac = 0
                    # for linux or "darwin (mac ports,homebrew,fink or self build versions)"
                    if platform == "linux" or platform == "darwin":
                        rc = subprocess.call(['which', 'gedit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if rc == 0:
                            app_command = unquote(subprocess.check_output(['which', 'gedit']).decode('utf-8').rstrip('\n'))
                            os.system(app_command + " '" + str(global_full_filename) + "' &> /dev/null &")
                        else:
                            # for darwin if no macports,homebrew,fink or self build gedit version was found
                            if platform == "darwin":
                                #print("Try to open file with Gedit-Teksteditor.app" +str(global_full_filename))
                                rcmac = os.system("open -a Gedit-Teksteditor '" + str(global_full_filename) + "' &> /dev/null")
                        if (rc != 0 and rcmac != 0):
                            #print("Gedit Not Found her comes msg box and menu destroy")
                            primary_msg = "Gedit ...  Application Not Found on You're System"
                            secondary_msg = "File:\n" + str(global_full_filename) + "\nCreated but not opened with Gedit"
                            self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                    global_entered_filename = ""
                    global_full_filename = Path("")
                    self.destroy()
            else:
                #print("SORRY YOU DID NOT ENTERED A FILENAME")
                primary_msg = "NO FILE NAME WAS GIVEN"
                secondary_msg = "Return to menu after 10 seconds or OK press"
                self.on_message_box(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
                dialog.destroy()
        elif dialog_response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            #print("Response CANCEL back to menu")
        else:
            dialog.destroy()
            #print("Time Out,keyb esc button pushed or window closed back to menu")
        global_entered_filename = ""
        global_full_filename = Path("")
    def on_close_clicked(self, widget):
        self.destroy()     

    def on_message_box(self, msg_type, msg_button_type, primary_msg, secondary_msg):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=msg_type,
            buttons=msg_button_type,
            text=primary_msg,
        )
        dialog.set_position(Gtk.WindowPosition.CENTER)
        dialog.format_secondary_text(secondary_msg)
        if msg_type == Gtk.MessageType.ERROR:
            image = Gtk.Image()
            # still works but is deprecated
            #image.set_from_stock(Gtk.STOCK_DIALOG_ERROR, Gtk.IconSize.DIALOG)
            # using linux icons adwaita theme on macports.
            image.set_from_icon_name ("dialog-error-symbolic", Gtk.IconSize.DIALOG)
            image.show()
            dialog.set_image(image)
        GLib.timeout_add_seconds(5,dialog.destroy)
        dialog.run()
        dialog.destroy()

class NewFileHereExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        pass

# Actions to perform on activate
    def _new_empty_file(self, file) -> None:
        win = SelectionMenu(file)
        global global_full_filename 
        global_full_filename = Path(unquote(file.get_uri()[7:])).joinpath("new-empty-file")
        if not global_full_filename.is_file():
            #print("\nfile " + str(global_full_filename) + " will on OK click")
            file_open = open(global_full_filename, "a")
            file_open.close()
            global_full_filename = Path("")
        else:
            primary_msg = "File Already Exists !"
            secondary_msg = "The File :\n" + str(global_full_filename) + "\nIs not made !"
            window = win.on_message_box
            window(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
            global_full_filename = Path("")

    def _new_txt_file(self, file) -> None:
        win = SelectionMenu(file)
        global global_full_filename
        global_full_filename = Path(unquote(file.get_uri()[7:])).joinpath("new-empty-file.txt")
        if not global_full_filename.is_file():
            file_open = open(global_full_filename, "a")
            file_open.close()
            global_full_filename = Path("")
        else:
            primary_msg = "File Already Exists !"
            secondary_msg = "The File :\n" + str(global_full_filename) + "\nIs not made !"
            window = win.on_message_box
            window(Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, primary_msg, secondary_msg)
            global_full_filename = Path("")
# menu activate.
    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file) -> None:
        self._new_empty_file(file)

    def menu_txt_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file) -> None:
        self._new_txt_file(file)

    def menu_interactive_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file) -> None:
        global global_window
        global global_window_default_widget
        # Only one menu instance at a time is allowed.
        if global_window == None:
            global_window = SelectionMenu(file)
            global_window.connect("key-press-event", global_window.on_esc_key_press)
            global_window.connect("destroy", global_window.destroy_SelectionMenu)
            global_window.show_all()
            global_window_default_widget = global_window.get_focus()
            Gtk.main()
        else:
            #print("SelectionMenu already running bring it back on top")
            global_window.present()
            global_window.set_focus(global_window_default_widget)

# Menu's defines
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


        # on selected map only the interactif menu item is avbl.
        sub_menuitem = Nautilus.MenuItem(
            name="NewFileHereExtension::InterActifMenu",
            label="Interactive Menu",
            tip="",
            icon="")
        submenu.append_item(sub_menuitem)
        sub_menuitem.connect("activate", self.menu_interactive_activate_cb, file)


        return [top_menuitem]

    def get_background_items(
        self,
        # added window, needed for gtk-3 version nautilus versions 3.x
        window,
        file: Nautilus.FileInfo
        ) -> List[Nautilus.MenuItem]:
        top_menuitem = Nautilus.MenuItem(
            name="NewFileHereExtension::NewFileHere",
            label="New File Here",
            tip="",
            icon="")

        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        # submenu item 1 new-empty-file
        sub_menuitem = Nautilus.MenuItem(
            name="NewFileHereExtension::InterActifMenu",
            label="Interactive Menu",
            tip="",
            icon="")
        submenu.append_item(sub_menuitem)
        sub_menuitem.connect("activate", self.menu_interactive_activate_cb, file)

        # submenu item 2 new-empty-file
        sub_menuitem = Nautilus.MenuItem(
            name="NewFileHereExtension::NewEmptyFile",
            label="New Empty File Here",
            tip="",
            icon="")
        submenu.append_item(sub_menuitem)
        sub_menuitem.connect("activate", self.menu_activate_cb, file)

        # submenu item 3 new-empty-txt-file
        sub_menuitem = Nautilus.MenuItem(
            name="NewFileHereExtension::NewEmptyTxtFile",
            label="New Empty .txt File Here",
            tip="",
            icon="")
        submenu.append_item(sub_menuitem)
        sub_menuitem.connect("activate", self.menu_txt_activate_cb, file)

        return [top_menuitem]
