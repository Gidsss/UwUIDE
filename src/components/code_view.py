from customtkinter import *
from tkinter import Event
from src.lexer import Lexer,Token,Error

class Linenums(CTkCanvas):
   def __init__(self, master, text_widget: CTkTextbox, **kwargs):
      super().__init__(master, **kwargs)
      CTkCanvas.__init__(self, master=master, width=16, borderwidth=0,highlightthickness=0, bg='#1A1B26')

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

         self.create_text(12, dlineinfo[1] + 10, text=f"{lineno}", anchor='center', fill='#333652', font=("Montserrat", 10))

class CodeEditor(CTkFrame):
   def __init__(self, master, lexer: Lexer, **kwargs):
      super().__init__(master, **kwargs)

      self.lexer = lexer
      self.tokens: list[Token] = []
      self.errors: list[Error] = []

      self.grid_columnconfigure(0, weight=1)
      self.grid_columnconfigure(1, weight=25)
      self.grid_rowconfigure(0, weight=1)

      self.text = CTkTextbox(master=self, corner_radius=0,fg_color='#1A1B26', text_color='#FFFFFF')
      self.text.grid(row=0, column=1, sticky='nsew')

      self.line_nums = Linenums(master=self, text_widget=self.text)
      self.line_nums.grid(row=0, column=0, sticky='nsew')

      self.text.bind("<Button-1>", lambda e: self.line_nums.on_redraw(e))
      self.text.bind("<Tab>", lambda e: self.on_tab(e))

      self.text.bind("<Return>", lambda e: self.line_nums.on_redraw(e))
      self.text.bind("<BackSpace>", lambda e: self.line_nums.on_redraw(e))

   def on_tab(self, e: Event):
      e.widget.insert(INSERT, " " * 6)
      return  'break'

   def run_lexer(self):
      source_code = [v + '\n' if v == '' else v for v in self.text.get('1.0','end-1c').split('\n')]
      print(source_code)
      lx: Lexer = self.lexer(source_code)

      self.tokens = lx.tokens
      self.errors = lx.errors
      print(lx.errors)

class CodeView(CTkTabview):
   def __init__(self, master, **kwargs):
      super().__init__(master, **kwargs)
      # TODO: Remove on integ, filenames should be from uwu.py input
      self.file_names = ['Untitled.uwu', 'Untitled(1).uwu']
      self.code_editors: dict[str, CodeEditor] = {}

      for file in self.file_names:
         tab = self.add(file)
         tab.grid_columnconfigure((0,1), weight=1)
         tab.grid_rowconfigure((0,1), weight=1)

         code_editor = CodeEditor(master=tab, fg_color='transparent', lexer=Lexer)
         code_editor.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

         self.code_editors[file] = code_editor

   def editor(self) -> CodeEditor:
      tab = self.get()
      code_editor: CodeEditor = self.code_editors[tab]

      return code_editor