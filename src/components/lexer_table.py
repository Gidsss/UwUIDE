from customtkinter import *

class LexerTable(CTkFrame):
   def __init__(self, master, data: list[tuple], **kwargs):
        super().__init__(master, **kwargs)
        self.columns = (0, 1)
        self.rows = tuple([i for i in range(len(data))])

        self.grid_columnconfigure(self.columns, weight=1)
        self.grid_rowconfigure(self.rows, weight=1)

        for row in range(len(data)):
            for col in range(2):
                self.table_content = CTkLabel(master=self, text=data[row][col], fg_color='transparent')

                self.table_content.grid(row=row, column=col, sticky='nsew')
