from customtkinter import *
from src.lexer import Error

class LogsTable(CTkFrame):
    def __init__(self, master, logs: list[Error], **kwargs):
        super().__init__(master, **kwargs)

        self.logs: list[Error] = logs
        
        self.rows = tuple([v for v in range(len(self.logs))]) if len(self.logs) > 0 else (0,1,2,3,4)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.grid_rowconfigure(self.rows, weight=1)

        for row in range(len(self.logs)):
            # TODO: Change render on Integ
            line, _ = self.logs[row].position
            self.line_label = CTkLabel(master=self, text=line+1, fg_color='transparent', text_color='#FFFFFF', anchor='n')

            self.log_message_label = CTkLabel(master=self, text=self.logs[row], fg_color='transparent', text_color='#ff5349', anchor='nw')

            self.line_label.grid(row=row, column=0, sticky='nsew', padx=32, pady=8)
            self.log_message_label.grid(row=row, column=1, sticky='nsew', columnspan=9, pady=8)

class LogsCanvas(CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0,highlightthickness=0, bg='#1A1B26')

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        self.render_table()

    def render_table(self, errors: list[Error] = []):
        self.logs_table = LogsTable(
            master=self,
            fg_color='transparent',
            logs=errors
        )
        self.logs_table.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

    def update_logs(self, errors: list[Error]):
        self.delete('all')
        self.render_table(errors=errors)