from customtkinter import *
from constants.path import *

from PIL import Image

from .code_view import CodeView

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

        self.newTabBGImage = CTkImage(light_image=Image.open(f"{NEW_TAB_ASSET}"))
        self.newTabButton = CTkButton(
            master=self,
            image=self.newTabBGImage,
            fg_color='#1A1B26',
            text='New Tab',
            font=('JetBrains Mono', 12),
            width=99,
            height=30,
            command=self.code_view.add_new_tab  # Set the command to add a new tab
        )
        self.newTabButton.grid(row=0, column=10, sticky='', columnspan=1)

        self.formatBgImage = CTkImage(light_image=Image.open(f"{FORMAT_ASSET}"))
        self.formatButton = CTkButton(
            master=self,
            image=self.formatBgImage,
            fg_color='#1A1B26',
            text='Format',
            font=('JetBrains Mono', 12),
            width=99,
            height=30,
            command=self.code_view.auto_format_code  # Set the command to trigger file loading
        )
        self.formatButton.grid(row=0, column=11, sticky='', columnspan=1)

        self.quickRunButtonBgImage = CTkImage(light_image=Image.open(f"{QUICK_RUN_ASSET}")) # Change the image asset tomorrow
        self.quickRunButton = CTkButton(
            master=self,
            image=self.quickRunButtonBgImage,
            fg_color='#1A1B26',
            text='Quick Run',
            font=('JetBrains Mono', 12),
            width=99,
            height=30,
            command=lambda : self.parent.on_compile_and_run(code_editor=self.code_view.editor, mode='quick')
        )
        self.quickRunButton.grid(row=0, column=12, sticky='', columnspan=1)

        self.compileAndRunBgImage = CTkImage(light_image=Image.open(f"{RUN_ASSET}"))
        self.compileAndRunButton = CTkButton(
            master=self,
            image=self.compileAndRunBgImage,
            fg_color='#1A1B26',
            text='Compile & Run',
            font=('JetBrains Mono', 12),
            width=99,
            height=30,
            command=lambda : self.parent.on_compile_and_run(code_editor=self.code_view.editor, mode='normal')
        )
        self.compileAndRunButton.grid(row=0, column=13, sticky='', columnspan=1)

        self.saveBgImage = CTkImage(light_image=Image.open(f"{SAVE_ASSET}"))
        self.saveButton = CTkButton(
            master=self,
            image=self.saveBgImage,
            fg_color='#1A1B26',
            text='Save',
            font=('JetBrains Mono', 12),
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
            text='Import',
            font=('JetBrains Mono', 12),
            width=99,
            height=30,
            command=self.code_view.load_file # Set the command to trigger file loading
        )
        self.loadButton.grid(row=0, column=15, sticky='', columnspan=1)