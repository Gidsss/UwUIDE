# import customtkinter as ctk
from customtkinter import *
from .components.lexer_table import LexerTable

class UwUCodePanel(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1,2,3,4), weight=4)
        
        # placeholder
        command_menu = CTkLabel(master=self, text='command menu')
        command_menu.grid(row=0, columnspan=4, sticky='nsew')

        code_editor = CTkTextbox(master=self, corner_radius=0)
        code_editor.grid(row=1, rowspan=2, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # placeholder
        console = CTkLabel(master=self, text='console', bg_color='gray')
        console.grid(row=3, rowspan=2, columnspan=4, stick='nsew')

class UwULexerPanel(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # TODO: Add widgets for respective frames
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=10)

        self.lexeme_label = CTkLabel(master=self, text='Lexeme', bg_color='light gray')
        self.token_label = CTkLabel(master=self, text='Token', bg_color='light gray')

        self.lexeme_label.grid(row=0, column=0, sticky='nsew')
        self.token_label.grid(row=0, column=1, sticky='nsew')

        self.lexer_table = LexerTable(master=self, fg_color='white', data=[
            ('fwunc', 'FUNCTION'),
            ('berry', 'IDENTIFIER'),
            ('fwunc', 'FUNCTION'),
        ])
        self.lexer_table.grid(row=1, rowspan=2 ,columnspan=2, sticky='nsew')

class UwU(CTk):
    def __init__(self):
        super().__init__()
        # TODO: Init window settings and display arrange different frames        
        self.geometry("1280x720")
        self.resizable(False, False)
        self.title("UwU IDE")

        # define grid
        self.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        # layout
        code_panel = UwUCodePanel(master=self, fg_color='transparent')
        code_panel.grid(row=0, column=0, rowspan=5, columnspan=4, sticky='nsew')

        lexer_panel = UwULexerPanel(master=self, fg_color='white', corner_radius=0, label_text='Lexer', label_fg_color='gray')
        lexer_panel.grid(row=0, column=4, rowspan=5, columnspan=2, sticky='nsew')

if __name__ == "__main__":
    app = UwU()
    app.mainloop()