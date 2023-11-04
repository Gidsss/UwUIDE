from customtkinter import *

from .components.code_view import CodeView
from .components.console_view import ConsoleView
from .components.command_menu import CommandMenu
from .components.analyzer_tabs import UwULexerTab, UwUParserTab

class UwUCodePanel(CTkFrame):
    def __init__(self, master, on_compiler_run, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1,2,3,4,5), weight=4)
        
        self.code_view = CodeView(
            master=self,
            corner_radius=8,
            anchor='nw',
            fg_color='#1A1B26',
            segmented_button_fg_color='#1A1B26',
            segmented_button_selected_color='#333652',
            segmented_button_selected_hover_color='gray',
            segmented_button_unselected_color='#1A1B26',segmented_button_unselected_hover_color='gray'
        )
        self.code_view.grid(row=1, rowspan=5, columnspan=4, sticky='nsew', padx=12)
        
        self.console_view = ConsoleView(
            master=self,
            fg_color='#1A1B26',
            corner_radius=8,
            anchor='nw',
            segmented_button_fg_color='#1A1B26',
            segmented_button_selected_color='#333652',
            segmented_button_selected_hover_color='gray',
            segmented_button_unselected_color='#1A1B26',segmented_button_unselected_hover_color='gray'
        )
        self.console_view.grid(row=6, rowspan=1, columnspan=4, stick='nsew', padx=12, pady=12)
        self.update_logs = self.console_view.update_logs
        
        self.command_menu = CommandMenu(
            master=self,
            fg_color='transparent',
            on_compiler_run=on_compiler_run
        )
        self.command_menu.grid(row=0, columnspan=4, sticky='nsew', pady=8)
    # Initially, associate the first CodeEditor with the CommandMenu 
        first_code_editor = self.code_view.code_editors['Untitled.uwu']
        self.command_menu.set_code_editor(first_code_editor)

    # When you switch tabs in your CodeView class, call this method to update the CodeEditor reference:
    def switch_tab(self):
        current_tab = self.code_view.get()
        current_code_editor = self.code_view.code_editors[current_tab]
        self.command_menu.set_code_editor(current_code_editor)
        # Update the current_filename based on the tab name
        self.command_menu.current_filename = current_tab
    
    @property
    def editor(self):
        return self.code_view.editor()

class UwuAnalyzerPanel(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.lexer_tab = self.add('Lexer')
        self.parser_tab = self.add('Parser')

        self.lexer_tab.grid_columnconfigure((0,1), weight=1)
        self.lexer_tab.grid_rowconfigure((0,1), weight=1)

        self.parser_tab.grid_columnconfigure((0,1), weight=1)
        self.parser_tab.grid_rowconfigure((0,1), weight=1)

        self.lexer_tab_content = UwULexerTab(self.lexer_tab, fg_color='transparent')
        self.lexer_tab_content.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.parser_tab_content = UwUParserTab(self.parser_tab, fg_color='transparent')
        self.parser_tab_content.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.update_lexer = self.lexer_tab_content.update_lexer

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
        self.code_panel = UwUCodePanel(
            master=self,
            fg_color='transparent',
            on_compiler_run=self.on_compiler_run
        )
        self.code_panel.grid(row=0, column=0, rowspan=5, columnspan=4, sticky='nsew')

        self.analyzer_panel = UwuAnalyzerPanel(
            master=self,
            fg_color='#1A1B26',
            corner_radius=8,
            anchor='nw',
            segmented_button_fg_color='#1A1B26',
            segmented_button_selected_color='#333652',
            segmented_button_selected_hover_color='gray',
            segmented_button_unselected_color='#1A1B26',segmented_button_unselected_hover_color='gray'
        )
        self.analyzer_panel.grid(row=0, column=4, rowspan=5, columnspan=2, sticky='nsew')

    def on_compiler_run(self):
        code_editor = self.code_panel.editor 
        code_editor.run_lexer()
        self.analyzer_panel.update_lexer(tokens=code_editor.tokens)
        self.code_panel.update_logs(errors=code_editor.errors)
        # print("========== Tokens ==========",code_editor.tokens)
        # print("========== Errors ==========", code_editor.errors[0].position)
        

if __name__ == "__main__":
    app = UwU()
    app.mainloop()