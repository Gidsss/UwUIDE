from customtkinter import *
from .components.lexer_table import LexerTable
from .components.codeview import CodeView
from .components.command_menu import CommandMenu
from .components.analyzer_tabs import UwULexerTab, UwUParserTab

class UwUCodePanel(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1,2,3,4), weight=4)

        command_menu = CommandMenu(master = self, fg_color = 'transparent')
        command_menu.grid(row=0, columnspan=4, sticky='nsew')

        code_editor = CodeView(master=self, fg_color='transparent')
        code_editor.grid(row=1, rowspan=2, columnspan=4, sticky='nsew', padx=12, pady=4)
        
        console = CTkLabel(master=self, text='console', bg_color='#1A1B26', text_color='#FFFFFF')
        console.grid(row=3, rowspan=2, columnspan=4, stick='nsew', padx=12, pady=12)

class UwuAnalyzerPanel(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.lexer_tab = self.add('Lexer')
        self.parser_tab = self.add('Parser')

        self.lexer_tab.grid_columnconfigure((0,1), weight=1)
        self.lexer_tab.grid_columnconfigure((0,1), weight=1)

        self.parser_tab.grid_columnconfigure((0,1), weight=1)
        self.parser_tab.grid_columnconfigure((0,1), weight=1)

        self.lexer_tab_content = UwULexerTab(self.lexer_tab, fg_color='transparent')
        self.lexer_tab_content.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.parser_tab_content = UwUParserTab(self.parser_tab, fg_color='transparent')
        self.parser_tab_content.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

class UwU(CTk):
    def __init__(self):
        super().__init__()     
        self.geometry("1280x720")
        self.resizable(False, False)
        self.title("UwU++")
        self.configure(fg_color='#16161E')

        # define grid
        self.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        # layout
        code_panel = UwUCodePanel(master=self, fg_color='transparent')
        code_panel.grid(row=0, column=0, rowspan=5, columnspan=4, sticky='nsew')

        analyzer_panel = UwuAnalyzerPanel(
            master=self,
            fg_color='#1A1B26',
            corner_radius=20,
            anchor='nw',
            segmented_button_fg_color='#1A1B26',
            segmented_button_selected_color='#333652',
            segmented_button_selected_hover_color='gray',
            segmented_button_unselected_color='#1A1B26',segmented_button_unselected_hover_color='gray'
        )
        analyzer_panel.grid(row=0, column=4, rowspan=5, columnspan=2, sticky='nsew')

if __name__ == "__main__":
    app = UwU()
    app.mainloop()