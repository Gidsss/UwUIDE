from customtkinter import *

class Linenums(CTkCanvas):
   def __init__(self, master, text_widget: CTkTextbox, **kwargs):
      super().__init__(master, **kwargs)
      CTkCanvas.__init__(self, master=master, width=1, borderwidth=0,highlightthickness=0, bg='#333652')

      self.text_widget = text_widget

      self.redraw()

   def redraw(self):
      print('new line')
      #   self.text_widget.edit_modified()
      #   self.create_text(10, 10, text='1', fill='white')
      self.delete('all')
      
      first_line = 1
      last_line = int(self.text_widget.index(f"@0,{self.text_widget.winfo_height()}").split('.')[0])


      print(first_line, last_line)
      # print(first_line, last_line)
      for lineno in range(first_line, last_line + 1):
         self.create_text(10,10, text=f"{lineno}", fill='white')

      pass
    

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

      self.text.bind("<Return>", lambda _: self.line_nums.redraw())
      self.text.bind("<BackSpace>", lambda _: self.line_nums.redraw())

        