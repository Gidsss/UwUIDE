from customtkinter import *

class LogsTable(CTkFrame):
    def __init__(self, master, logs: list[dict], **kwargs):
        super().__init__(master, **kwargs)

        self.logs: list[dict] = logs
        
        self.rows = tuple([v for v in range(len(self.logs))])
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.grid_rowconfigure(self.rows, weight=1)

        for row in range(len(self.logs)):
            # TODO: Change render on Integ
            self.line_label = CTkLabel(master=self, text=self.logs[row]["line"], fg_color='transparent', text_color='#FFFFFF')

            self.log_message_label = CTkLabel(master=self, text=self.logs[row]["log_message"], fg_color='transparent', text_color='#FFFFFF', anchor='w')

            self.line_label.grid(row=row, column=0, sticky='nsew', padx=12)
            self.log_message_label.grid(row=row, column=1, columnspan=9, sticky='nsew', padx=1)