from customtkinter import *
from tkinter import *
from src.lexer import Lexer, Token, Error
from enum import Enum


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
    def __init__(self, master, lexer: Lexer, **kwargs):
        super().__init__(master, **kwargs)

        self.lexer = lexer
        self.tokens: list[Token] = []
        self.errors: list[Error] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=25)
        self.grid_rowconfigure(0, weight=1)


        self.text = CTkTextbox(master=self, corner_radius=0,fg_color='#1A1B26', text_color='#FFFFFF', undo=True)
        self.text.grid(row=0, column=1, sticky='nsew')

        self.text = CTkTextbox(master=self, corner_radius=0, fg_color='#1A1B26', text_color='#FFFFFF')
        self.text.grid(row=0, column=1, sticky='nsew')


        self.line_nums = Linenums(master=self, text_widget=self.text)
        self.line_nums.grid(row=0, column=0, sticky='nsew')

        self.text.bind("<Button-1>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Tab>", lambda e: self.on_tab(e))
        self.text.bind("<FocusIn>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<Return>", lambda e: self.line_nums.on_redraw(e))
        self.text.bind("<BackSpace>", lambda e: self.line_nums.on_redraw(e))


        self.copy_paste_triggered = False
        self.text.bind("<Control-c>", self.copy_text)
        self.text.bind("<Control-v>", self.paste_text)
 
        # Initialize tags
        for tag in Tags:
            self.text.tag_config(tag.name, **tag.options)

    def init_linenums(self):
        self.text.focus_set()

    def on_tab(self, e: Event):
        e.widget.insert(INSERT, " " * 6)
        return 'break'

    def run_lexer(self):
        source_code = [v + '\n' for v in self.text.get('1.0', 'end-1c').split('\n')]
        print(source_code)
        lx: Lexer = self.lexer(source_code)

        self.tokens = lx.tokens
        self.errors = lx.errors

        Remote.code_editor_instance = self

    def format(self, tag: str, start_pos: tuple[int, int], end_pos: tuple[int, int] = None):
        """
        Format a certain range of text in the textbox.
            tag is a string that determines what formatting option will be applied.
            start_pos indicates where to start applying
            end_pos indicates where to stop applying
            if start_pos and end_pos are the same, it will only format the single character in start_pos
        """

        # Set end_pos to None if it is equal to start_pos
        end_pos = None if end_pos == start_pos else end_pos

        # Set string indices
        self.clear_format()
        start_index = f"{start_pos[0]+1}.{start_pos[1]}"
        end_index = None if end_pos is None else f"{end_pos[0]+1}.{end_pos[1]+1}"

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

    def copy_text(self, event):
      if event.state == 0:  # Only trigger if no other modifiers are pressed
         self.text.clipboard_clear()
         selected_text = self.text.get("sel.first", "sel.last")
         self.text.clipboard_append(selected_text)

    def paste_text(self, event):
      if event.state == 0:  # Only trigger if no other modifiers are pressed
         text_to_paste = self.text.clipboard_get()
         self.text.insert(INSERT, text_to_paste)

class CodeView(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_names = ['Untitled.uwu']
        self.code_editors: dict[str, CodeEditor] = {}

        for file in self.file_names:
            self.create_new_tab(file)
    
    def create_new_tab(self, file_name):
        tab = self.add(file_name)
        tab.grid_columnconfigure((0, 1), weight=1)
        tab.grid_rowconfigure((0, 1), weight=1)

        code_editor = CodeEditor(master=tab, fg_color='transparent', lexer=Lexer)
        code_editor.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.code_editors[file_name] = code_editor
        
        # Pop up on right click
        test = Menu(code_editor.text, tearoff=False)
        test.add_command(label='Run Program', command=lambda : print('Hello world'))
        test.add_command(label='Save Program', command=lambda : print('Hello world'))
        test.add_separator()
        test.add_command(label='Close File', command=lambda : print('Hello world'))
        code_editor.text.bind('<Button-3>', lambda e: test.tk_popup(e.x_root, e.y_root))

    def remove_tab(self, file_name):
        pass

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
