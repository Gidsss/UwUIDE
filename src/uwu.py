from customtkinter import *
from tkinter import *
from tkinter import messagebox

from .components.code_view import CodeView, CodeEditor
from .components.console_view import ConsoleView
from .components.command_menu import CommandMenu
from .components.analyzer_tabs import UwULexerTab, UwUParserTab
from .components.welcome_window import WelcomeWindow
from constants.path import *

FontManager.load_font('./assets/font/JetBrainsMono/JetBrainsMono-Regular.ttf')

class CompilerStatus:
    is_compiling = False

compiler_status = CompilerStatus() 
class UwUCodePanel(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1,2,3,4,5), weight=4)
        self.compiler_status = CompilerStatus()  # Compiler status instance

        self.code_view = CodeView(
            master=self,
            parent=master,
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
            editor=self.code_view.editor,
            fg_color='transparent',
            bg_color='transparent',
            corner_radius=8,
            anchor='nw',
            segmented_button_fg_color='#1A1B26',
            segmented_button_selected_color='#333652',
            segmented_button_selected_hover_color='gray',
            segmented_button_unselected_color='#1A1B26',
            segmented_button_unselected_hover_color='gray'
        )
        self.console_view.grid(row=6, rowspan=1, columnspan=4, stick='nsew', padx=12, pady=12)
              
        self.command_menu = CommandMenu(
            master=self,
            parent=master,
            code_view=self.code_view,
            fg_color='transparent',
        )
        self.command_menu.grid(row=0, columnspan=4, sticky='nsew', pady=8)

        self.update_error_logs = self.console_view.update_error_logs
        self.update_compiler_logs = self.console_view.update_compiler_logs
    
    def update_logs_callback(self, editor, is_compiling):

        if hasattr(self, 'console_view'):
            self.console_view.update_compiler_logs(editor=editor, is_compiling=is_compiling)
        else:
            print("No console view to update logs.")

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
        self.update_parser_tree = self.parser_tab_content.update_parser_tree
        self.clear_parser_tree = self.parser_tab_content.clear_parser_tree

class UwU(CTk):
    def __init__(self):
        super().__init__()     
        self.geometry("1920x1080-100")
        self.resizable(True, True)
        self.title("UwU++ by SenPys")
        self.configure(fg_color='#16161E')
        self.iconbitmap(f"{ICON_BLACK_ASSET}")

        # Open top level window
        self.welcomeWindow = WelcomeWindow(self)
        
        # define grid
        self.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        # layout
        self.code_panel = UwUCodePanel(
            master=self,
            fg_color='transparent',
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

        self.fullscreen = True
        self.after(150, self.set_fullscreen) # Call set_fullscreen after 150ms

        self.bind("<KeyPress>", lambda e : self.run(e))
        self.bind("<Control-s>", lambda _ : self.code_panel.code_view.save_file())
        self.bind("<Control-o>", lambda _ : self.code_panel.code_view.load_file())
        self.bind("<Control-n>", lambda _ : self.code_panel.code_view.add_new_tab())
        self.bind("<F3>", lambda _ : self.code_panel.code_view.auto_format_code())
        self.bind("<F4>", lambda _ : self.on_compile_and_run(code_editor=self.code_panel.code_view.editor, mode='quick'))
        self.bind("<F11>", self.toggle_fullscreen)
        
    def set_fullscreen(self):
        self.state('zoomed') # Maximize the window first
        self.attributes("-fullscreen", True) # Then set it to fullscreen
        self.update_idletasks()

    def toggle_fullscreen(self, e: Event = None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        if self.fullscreen:
            self.attributes("-fullscreen", True)
        else:
            self.attributes("-fullscreen", False)

    def run(self, e: Event):
        if e.keysym != 'F5':
            return
        
        self.on_compile_and_run(code_editor=self.code_panel.code_view.editor)

    def on_compile_and_run(self, code_editor: CodeEditor, mode='normal'):
        if compiler_status.is_compiling and mode == 'normal':
            messagebox.showerror('COMPILATION ERROR', 'A compilation task is in progress, cannot run another process.')
            return

        lx_res = code_editor.run_lexer()
        p_res = code_editor.run_parser()
        a_res = code_editor.run_analyzer()

        compiler_status.is_compiling = lx_res and p_res and a_res
        self.analyzer_panel.update_lexer(tokens=code_editor.tokens)
        
        if code_editor.program:
            self.analyzer_panel.update_parser_tree(program=code_editor.program)

        self.code_panel.update_compiler_logs(editor=code_editor, is_compiling=compiler_status.is_compiling)

        if len(code_editor.lx_errors) > 0:
            self.analyzer_panel.clear_parser_tree()
            self.code_panel.update_error_logs(errors=code_editor.lx_errors)
        elif len(code_editor.p_errors) > 0:
            self.code_panel.update_error_logs(errors=code_editor.p_errors)
        elif len(code_editor.a_errors) > 0:
            self.code_panel.update_error_logs(errors=code_editor.a_errors)
        else:
            self.code_panel.update_error_logs(errors=[])
            if mode == 'quick':
                # Quick mode execution
                code_editor.quick_run()
                compiler_status.is_compiling = False
                self.code_panel.update_compiler_logs(editor=code_editor, is_compiling=False)
            else:
                # Default compiling mode execution
                code_editor.start(editor=code_editor, compiler_status=compiler_status, update_logs_callback=self.code_panel.update_compiler_logs)

if __name__ == "__main__":
    app = UwU()  
    app.mainloop()

# Version 0.3.0
# Created by SenPys