from customtkinter import *
from src.lexer.lexer import Error, DelimError
from src.components.code_view import Tags, Remote

class LogsTable(CTkFrame):
    def __init__(self, master, logs: list[Error], **kwargs):
        super().__init__(master, **kwargs)

        self.logs: list[Error] = logs
        
        self.rows = tuple([v for v in range(len(self.logs))]) if len(self.logs) > 0 else (0,1,2,3,4)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)

        self.code_editor = Remote.code_editor_instance
        self.line_labels = []
        self.log_message_labels = []

        for row in range(len(self.logs)):
            # TODO: Change render on Integ
            start_pos = line, col = self.logs[row].position
            end_pos = None if isinstance(self.logs[row], DelimError) else self.logs[row].end_position
            line_label = CTkLabel(master=self, text=line + 1, fg_color='transparent', font=('JetBrains Mono', 13), text_color='#FFFFFF', anchor='n')

            log_message_label = CTkLabel(master=self, text=self.logs[row], fg_color='transparent', font=('JetBrains Mono', 13), text_color='#ff5349',
                                         anchor='nw')
            
             # Bind callbacks
            log_message_label.bind("<Enter>", lambda ev, sp=start_pos, ep=end_pos: self.code_editor.format(
                Tags.ERROR_HIGHLIGHT.name, sp, ep
            ))
            log_message_label.bind("<Leave>", lambda ev: self.code_editor.clear_format())
            line_label.grid(row=row, column=0, sticky='nsew', padx=32, pady=8)
            log_message_label.grid(row=row, column=1, sticky='nsew', columnspan=9, pady=8)

class LogsCanvas(CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0,highlightthickness=0, bg='#1A1B26')

        self.grid_columnconfigure((0,1), weight=1)

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