from customtkinter import *
from constants.path import *
from PIL import Image, ImageTk

from tkinter import filedialog

class CommandMenu(CTkFrame):
    def __init__(self, master, on_compiler_run, **kwargs):
        super().__init__(master, **kwargs)
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
            command=on_compiler_run
        )
        self.runButton.grid(row=0, column=13, sticky='', columnspan=1)

        self.saveBgImage = CTkImage(light_image=Image.open(f"{SAVE_ASSET}"))
        self.saveButton = CTkButton(master=self, image=self.saveBgImage, fg_color='#1A1B26', text='', width=99, height=30)
        self.saveButton.grid(row=0, column=14, sticky='', columnspan=1)
        self.saveButton.configure(command=self.save_file)  # Set the command to trigger file saving

        self.loadBgImage = CTkImage(light_image=Image.open(f"{LOAD_ASSET}"))
        self.loadButton = CTkButton(master=self, image=self.loadBgImage, fg_color='#1A1B26', text='', width=99, height=30)
        self.loadButton.grid(row=0, column=15, sticky='', columnspan=1)
        self.loadButton.configure(command=self.load_file)  # Set the command to trigger file loading

        # Create a reference to the code_editor
        self.code_editor = None

    def set_code_editor(self, code_editor):
            self.code_editor = code_editor

    def save_file(self):
        if self.code_editor:
            file_content = self.code_editor.text.get('1.0', 'end-1c')
            file_name = filedialog.asksaveasfilename(defaultextension=".uwu", filetypes=[("UwU Files", "*.uwu")])
            if file_name:
                with open(file_name, "w") as file:
                    file.write(file_content)

    def load_file(self):
        if self.code_editor:
            file_name = filedialog.askopenfilename(filetypes=[("UwU Files", "*.uwu")])
            if file_name:
                with open(file_name, "r") as file:
                    file_content = file.read()
                    self.code_editor.text.delete('1.0', 'end-1c')
                    self.code_editor.text.insert('1.0', file_content)
                self.current_filename = file_name  # Update current_filename