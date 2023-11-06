from customtkinter import *
from constants.path import *

from tkinter import filedialog
from PIL import Image, ImageTk

from .code_view import CodeView, CodeEditor

class CommandMenu(CTkFrame):
    def __init__(self, master, code_view: CodeView, on_compiler_run, **kwargs):
        super().__init__(master, **kwargs)
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

    def save_file(self):
        code_editor: CodeEditor = self.code_view.editor

        if code_editor:
            file_content = code_editor.text.get('1.0', 'end-1c')
            file_name = filedialog.asksaveasfilename(initialfile=self.code_view.get(),defaultextension=".uwu", filetypes=[("UwU Files", "*.uwu")])
            if file_name:
                with open(file_name, "w") as file:
                    file.write(file_content)
    
    def load_file(self):
        if self.code_view and self.code_view.code_editors:
            file_path = filedialog.askopenfilename(filetypes=[("UwU Files", "*.uwu")])
            file_name = os.path.basename(file_path)
            if file_name:
                if file_name not in self.code_view.code_editors:
                    self.code_view.create_new_tab(file_name)
                with open(file_name, "r") as file:
                    file_content = file.read()
                    self.code_view.code_editors[file_name].text.delete('1.0', 'end-1c')
                    self.code_view.code_editors[file_name].text.insert('1.0', file_content)
                self.code_view.current_filename = file_name