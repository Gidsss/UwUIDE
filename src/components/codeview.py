from customtkinter import *
from tkinter import Event

class Linenums(CTkCanvas):
   def __init__(self, master, text_widget: CTkTextbox, **kwargs):
      super().__init__(master, **kwargs)
      CTkCanvas.__init__(self, master=master, width=1, borderwidth=0,highlightthickness=0, bg='#333652')

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

         self.create_text(12, dlineinfo[1] + 10, text=f"{lineno}", anchor='center', fill='white', font=("Montserrat", 10))
    

class CodeView(CTkFrame):
   def __init__(self, master, **kwargs):
      super().__init__(master, **kwargs)
      self.grid_columnconfigure(0, weight=1)
      self.grid_columnconfigure(1, weight=25)
      self.grid_rowconfigure(0, weight=1)

      self.text = CTkTextbox(master=self, corner_radius=0,fg_color='#1A1B26', text_color='#FFFFFF')
      self.text.grid(row=0, column=1, sticky='nsew')

      self.line_nums = Linenums(master=self, text_widget=self.text)
      self.line_nums.grid(row=0, column=0, sticky='nsew')

      self.text.bind("<Button-1>", lambda e: self.line_nums.on_redraw(e))
      
      self.text.bind("<Return>", lambda e: self.line_nums.on_redraw(e))
      self.text.bind("<BackSpace>", lambda e: self.line_nums.on_redraw(e))

        