import subprocess
import uuid
import threading

from customtkinter import *
from tkinter import *
from constants.path import *
from theme import themes

from src.lexer import Lexer, Token, Error
from src.lexer.token import UniqueTokenType
from src.parser import Parser, ErrorSrc
from src.analyzer import MemberAnalyzer, TypeChecker
from src.analyzer.error_handler import ErrorSrc as AnalyzerErrorSrc
from src.compiler import Compiler

from enum import Enum
from PIL import Image

# edit theme to change the color scheme
EDITOR_THEME = themes['tokyo']
class Linenums(CTkCanvas):
    def __init__(self, master, text_widget: CTkTextbox, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0, highlightthickness=0, bg='#1A1B26')

        self.text_widget = text_widget

    def on_redraw(self, event: Event):
        self.after(1, self.redraw, event)

    def redraw(self, event: Event):
        self.delete('all')

        first_line = 1
        last_line = int(event.widget.index(f"@0,{event.widget.winfo_height()}").split('.')[0])

        for lineno in range(first_line, last_line + 1):
            dlineinfo: tuple[int, int, int, int, int] | None = event.widget.dlineinfo(f"{lineno}.0")

            if dlineinfo is None:
                continue

            self.create_text(12, dlineinfo[1] + 10, text=f"{lineno}", anchor='center', fill='#333652',
                             font=("Montserrat", 10))


class Tags(Enum):
   """
   A tag Enum class to keep track of the different tags
   that the CodeEditor can use to format text.
       name indicates the arbitrary tag name
       options indicate the dict setting to be applied to the text when the tag is used

   Sample tag initialization
   <TAG_NAME> = (<name>,
                 {<key>: <val>,
                  <key>: <val>,
                  ... }
   """

   def __init__(self, name: str, options: dict):
      self._name = name
      self._options = options

   @property
   def name(self):
      return self._name

   @property
   def options(self):
      return self._options

   TOKEN_HIGHLIGHT = ("token_highlight",
                      {"background": "#89ca78",
                       "foreground": "#282c34"})

   ERROR_HIGHLIGHT = ("error_highlight",
                      {"background": "#971142"})


class CodeEditor(CTkFrame):
    def __init__(self, master, filename, lexer: Lexer, parser: Parser, analyzer: MemberAnalyzer, type_checker: TypeChecker, **kwargs):
        super().__init__(master, **kwargs)

        self.filename: str = filename
        self.lexer = lexer
        self.parser = parser
        self.analyzer = analyzer
        self.type_checker = type_checker
        self.tokens: list[Token] = []
        self.program = None
        self.transpiled_program = None
        self.lx_errors: list[Error] = []
        self.p_errors: list[Error] = []
        self.a_errors = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=25)
        self.grid_rowconfigure(0, weight=1)
        
        self.text = CTkTextbox(master=self, corner_radius=0,fg_color='transparent', font=('JetBrains Mono', 13), text_color='#FFFFFF', undo=True)
        self.text.grid(row=0, column=1, sticky='nsew')

        self.line_nums = Linenums(master=self, text_widget=self.text)
        self.line_nums.grid(row=0, column=0, sticky='nsew')
        
        self.text.bind("<Button-1>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Up>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Down>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Tab>", lambda e: self.on_tab(e))
        self.text.bind("<FocusIn>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Return>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<BackSpace>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Visibility>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<KeyRelease>", lambda e: self.on_idle_gui(e))

        self.text.bind("<Control-c>", lambda e: self.copy_text(e))
        self.text.bind("<Control-v>", lambda e: self.paste_text(e))
        self.text.bind("<Control-z>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Control-y>", lambda e: self.line_nums.on_redraw(e)) 
         
        # Initialize QoL text for untitled code editor
        self.init_text()
        self.syntax_highlight()
 
        # Initialize tags
        for tag in Tags:
            self.text.tag_config(tag.name, **tag.options)


    def init_text(self):
        initial_text = ">.< global declarations\n\nfwunc mainuwu-san() [[\n\n]]\n\n>.< global declarations" # For QoL Purposes
        self.text.insert('1.0', initial_text)

    def init_linenums(self):
        self.text.focus_set()

    def on_tab(self, e: Event):
        e.widget.insert(INSERT, " " * 4)
        return 'break'

    def on_idle_gui(self, event = None):
        # ignore navigation and tab keys
        if event.keysym in ['Up', 'Down', 'Left', 'Right', 'Tab']:
            return
        
        typing_timer = None
        # Cancel the previous timer
        if typing_timer:
            self.text.after_cancel(typing_timer)

        # Start a new timer
        typing_timer = self.text.after(1500, self.syntax_highlight)

    def syntax_highlight(self, event = None):
        self.source_code = [v if v else v + '\n' for v in self.text.get('1.0', 'end-1c').split('\n')]

        lx = self.lexer(self.source_code)
        self.tokens = lx.tokens
        self.lx_errors = lx.errors

        for tag in self.text.tag_names():
            if tag not in ['token_highlight', 'error_highlight']:
                self.text.tag_delete(tag)

        for i,token in enumerate(self.tokens):
            if(token.token.token == 'WHITESPACE'):
                continue
            
            row_pos,col_pos = token.position
            row_end_pos,col_end_pos = token.end_position

            token_tag_name = uuid.uuid4()
            token_start_pos = f'{row_pos+1}.{col_pos}'
            token_end_pos = f'{row_end_pos+1}.{col_end_pos+1}'
            
            self.text.tag_add(token_tag_name, token_start_pos,token_end_pos)
            try:
                tok = None
                
                if(isinstance(token.token, UniqueTokenType)):
                    tok = token.token.unique_type.split('_')[0]
                    
                    if(tok == 'IDENTIFIER' and self.tokens[i - 1].token.token == '.'):
                        tok = 'METHOD'
                else:
                    tok = token.token.token

                fg = EDITOR_THEME[tok]
                self.text.tag_config(token_tag_name, foreground=fg)
            except:
                self.text.tag_config(token_tag_name, foreground=EDITOR_THEME['default'])

    def run_lexer(self) -> bool:
        if(len(self.lx_errors) > 0 and self.program):
            self.program = None
            self.transpiled_program = None
            self.p_errors = []
            self.a_errors = []
        else:
            Remote.code_editor_instance = self
            return True
        
        return False
 
    def run_parser(self) -> bool:
        if len(self.lx_errors) > 0:
            return
        
        ErrorSrc.src = self.source_code
        p: Parser = self.parser(self.tokens)
        self.program = p.program

        if p.errors:
            self.p_errors = p.errors
        else:
            self.p_errors = []
            return True
        
        return False

    def run_analyzer(self) -> bool:
        if len(self.p_errors) > 0 or not self.program:
            return
        
        AnalyzerErrorSrc.src = self.source_code
        ma = self.analyzer(self.program)
        if ma.errors:
            self.a_errors = ma.errors
            return False
        else:
            self.a_errors = []

        tc = self.type_checker(self.program)
        if tc.errors:
            self.a_errors = tc.errors
        else:
            self.a_errors = []
        
        if len(self.a_errors) == 0:
            self.transpiled_program = self.program.python_string()
            return True
        else: 
            self.transpiled_program = None

        return False

    def compile_and_run(self, editor, compiler_status, update_logs_callback):
        filename = self.filename.split('.')[0]
        c = Compiler(py_source=self.transpiled_program, filename=self.filename)
        c.compile()

        exe_name = f"{filename}.exe"
        exe_path = Path("./dist") / exe_name
        if exe_path.exists():
            cmd = f"cmd /c start cmd.exe /k {exe_path}"
            subprocess.run([cmd], shell=True)

        compiler_status.is_compiling = False
        update_logs_callback(editor=editor, is_compiling=compiler_status.is_compiling)

    def start(self, editor, compiler_status, update_logs_callback):
        compile_thread = threading.Thread(target=lambda: self.compile_and_run(editor=editor, compiler_status=compiler_status, update_logs_callback=update_logs_callback), name="UwU Compile", daemon=True)
        compile_thread.start()

    def format(self, tag: str, start_pos: tuple[int, int], end_pos: tuple[int, int] = None):
        """
        Format a certain range of text in the textbox.
            tag is a string that determines what formatting option will be applied.
            start_pos indicates where to start applying
            end_pos indicates where to stop applying
            if start_pos and end_pos are the same, it will only format the single character in start_pos
        """
        # Validate position inputs
        if not start_pos or not isinstance(start_pos, tuple) or len(start_pos) != 2:
            print("Invalid start position")
            return

        if end_pos and (not isinstance(end_pos, tuple) or len(end_pos) != 2):
            print("Invalid end position, defaulting to start_pos")
            end_pos = start_pos
            
        # Set end_pos to None if it is equal to start_pos
        end_pos = None if end_pos == start_pos else end_pos

        # Set string indices
        self.clear_format()
        start_index = f"{start_pos[0]+1}.{start_pos[1]}"
        end_index = None if end_pos is None else f"{end_pos[0]+1}.{end_pos[1]+1}"

        # Format text in the index
        self.text.tag_add(tag, start_index, end_index)

    def format_multiple(self, tag: str, ranges: list[(tuple[int, int], tuple[int, int] | None)]):
        """
        Formats text in the given list of positions
            tag is a string that determines what formatting option will be applied.
            positions is a list of start_pos and end_pos(optional) for tokens to be formatted
        """

        for start_pos, end_pos in ranges:
            # Set end_pos to None if it is equal to start_pos
            end_pos = None if end_pos == start_pos else end_pos

            # Set string indices
            start_index = f"{start_pos[0] + 1}.{start_pos[1]}"
            end_index = None if end_pos is None else f"{end_pos[0] + 1}.{end_pos[1] + 1}"

            # Format text in the index
            self.text.tag_add(tag, start_index, end_index)

    def clear_format(self, tags_to_clear: list[Tags] = None):
        """
        Clear all tags(formatting) in the textbox
            tags_to_clear is an optional parameter to specify which tag/s to clear
            by default, clears ALL tags
        """

        tags = tags_to_clear if tags_to_clear else Tags
        for tag in tags:
            self.text.tag_remove(tag.name, "1.0", "end")

    def copy_text(self, event: Event):
        event.widget.clipboard_clear()
        selected_text = event.widget.get("sel.first", "sel.last")
        event.widget.clipboard_append(selected_text)

        return "break"

    def paste_text(self, event: Event):
        try:
            text_to_paste = event.widget.clipboard_get()
            if event.widget.tag_ranges("sel"):
                # If there is text selected, replace it with the clipboard text
                event.widget.delete("sel.first", "sel.last")
                event.widget.insert("insert", text_to_paste)
            else:
                # If there is no text selected, just insert at the cursor
                event.widget.insert(INSERT, text_to_paste)
            self.syntax_highlight()
        except TclError:
            raise ValueError('Clipboard is empty')
        finally:
            self.line_nums.on_redraw(event)
        return "break"

class CodeView(CTkTabview):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = parent
        self.file_names = ['Untitled.uwu']
        self.code_editors: dict[str, CodeEditor] = {}
        
        for file in self.file_names:
            self.create_new_tab(file)
            self.bind_esc(editor=self.code_editors[file], file_name=file)
    
    def create_new_tab(self, file_name):
        tab = self.add(file_name)
        tab.grid_columnconfigure((0, 1), weight=1)
        tab.grid_rowconfigure((0, 1), weight=1)

        code_editor = CodeEditor(master=tab, filename=file_name, fg_color='transparent', lexer=Lexer, parser=Parser, analyzer=MemberAnalyzer, type_checker=TypeChecker)
        code_editor.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')
        self.bind_esc(editor=code_editor, file_name=file_name)
        self.code_editors[file_name] = code_editor
        
        # Pop up on right click
        options_menu = Menu(code_editor.text, tearoff=False)

        options_menu.add_command(label='Run Program', command=lambda : self.parent.on_compiler_run(code_editor=code_editor))
        options_menu.add_command(label='Save Program', command=self.save_file)
        options_menu.add_command(label='Format Source Code', command=self.auto_format_code)
        options_menu.add_separator()
        options_menu.add_command(label='Close File', command=lambda : self.remove_tab(file_name))

        code_editor.text.bind('<Button-3>', lambda e: options_menu.tk_popup(e.x_root, e.y_root))

    def remove_tab(self, file_name):
        self.delete(file_name)
        code_editor = self.code_editors.pop(file_name)
        code_editor.destroy()

    def save_file(self):
        code_editor: CodeEditor = self.editor

        if code_editor:
            file_content = code_editor.text.get('1.0', 'end-1c')
            file_name = filedialog.asksaveasfilename(initialfile=self.get(),defaultextension=".uwu", filetypes=[("UwU Files", "*.uwu")])
            if file_name:
                with open(file_name, "w") as file:
                    file.write(file_content)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("UwU Files", "*.uwu")])
        file_name = os.path.basename(file_path)
        if file_path:
            if file_name not in self.code_editors:
                self.create_new_tab(file_name)
                self.set(file_name)
            with open(file_path, "r") as file:
                file_content = file.read()
                self.code_editors[file_name].text.delete('1.0', 'end-1c')
                self.code_editors[file_name].text.insert('1.0', file_content)
                self.code_editors[file_name].syntax_highlight()
            self.editor.init_linenums()

    def auto_format_code(self):

        # Validate source code
        lx_res = self.editor.run_lexer()
        p_res = self.editor.run_parser()

        self.parent.code_panel.update_compiler_logs(editor=self.editor, is_compiling=False, is_formatting=True)

        if lx_res and p_res:
            # Replace source code with formatted string
            self.editor.text.delete("1.0", END)
            self.editor.text.insert("1.0", self.editor.program.formatted_string())
            self.editor.syntax_highlight()

            # Reset states
            self.editor.lx_errors = []
            self.editor.p_errors = []
            self.editor.program = None
            self.parent.code_panel.update_error_logs(errors=[])
            return 

        # Update errors
        if self.editor.lx_errors:
            self.parent.code_panel.update_error_logs(errors=self.editor.lx_errors)
        if self.editor.p_errors:
            self.parent.code_panel.update_error_logs(errors=self.editor.p_errors)

    def bind_esc(self, editor: CodeEditor, file_name: str):
        editor.text.bind("<Escape>", lambda e: self.remove_tab(file_name))

    @property
    def editor(self) -> CodeEditor:
        try:
            tab = self.get()
            return self.code_editors[tab]
        except:
            raise KeyError('Code tab does not exist.')

class Remote:
    """
   A way for other frames to easily interact with the current code editor instance.

   This can be expanded to have other class instances in it.
   """
    code_editor_instance: CodeEditor = None
