from customtkinter import *
from constants.path import *

from tkinter import filedialog
from PIL import Image, ImageTk

from .code_view import CodeView, CodeEditor

class CommandMenu(CTkFrame):
    def __init__(self, master, parent, code_view: CodeView, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = parent
        self.code_view = code_view
        self.columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        self.rows = (0)

        self.grid_columnconfigure(self.columns, weight=1)
        self.grid_rowconfigure(self.rows, weight=1)

        self.uwuBgImage = CTkImage(light_image=Image.open(f"{LOGO_WHITE_ASSET}"), size=(100, 30))
        self.uwuLabel = CTkLabel(master=self, image=self.uwuBgImage, text='')
        self.uwuLabel.grid(row=0, column=0, sticky='nsew', columnspan=2)

        self.runBgImage = CTkImage(light_image=Image.open(f"{RUN_ASSET}"))
        self.runButton = CTkButton(
            master=self,
            image=self.runBgImage,
            fg_color='#1A1B26',
            text='',
            width=99,
            height=30,
            command=lambda : self.parent.on_compiler_run(code_editor=self.code_view.editor)
        )
        self.runButton.grid(row=0, column=13, sticky='', columnspan=1)

        self.saveBgImage = CTkImage(light_image=Image.open(f"{SAVE_ASSET}"))
        self.saveButton = CTkButton(
            master=self,
            image=self.saveBgImage,
            fg_color='#1A1B26',
            text='',
            width=99,
            height=30,
            command=self.code_view.save_file # Set the command to trigger file saving
        )
        self.saveButton.grid(row=0, column=14, sticky='', columnspan=1)

        self.loadBgImage = CTkImage(light_image=Image.open(f"{LOAD_ASSET}"))
        self.loadButton = CTkButton(
            master=self,
            image=self.loadBgImage,
            fg_color='#1A1B26',
            text='',
            width=99,
            height=30,
            command=self.code_view.load_file # Set the command to trigger file loading
        )
        self.loadButton.grid(row=0, column=15, sticky='', columnspan=1)