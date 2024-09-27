from customtkinter import *
from src.lexer.lexer import Error, DelimError
from src.components.code_view import Tags, Remote

class LogsTable(CTkFrame):
    def __init__(self, master, logs, **kwargs):
        super().__init__(master, **kwargs)
        self.logs = logs
        self.rows = tuple(range(len(self.logs))) if self.logs else (0,1,2,3,4)
        self.grid_columnconfigure(tuple(range(10)), weight=1)
        self.code_editor = Remote.code_editor_instance
        self.line_labels = []
        self.log_message_labels = []

        for row in range(len(self.logs)):
            line_label = None
            try:
                # Ensure position and end_position are fetched correctly
                if callable(self.logs[row].position):
                    start_pos = self.logs[row].position()
                else:
                    start_pos = self.logs[row].position

                if hasattr(self.logs[row], 'end_position') and not isinstance(self.logs[row], DelimError):
                    if callable(self.logs[row].end_position):
                        end_pos = self.logs[row].end_position()
                    else:
                        end_pos = self.logs[row].end_position
                else:
                    end_pos = start_pos  # Use start_pos if end_pos is not available

                line_label = CTkLabel(master=self, text=str(start_pos[0] + 1), fg_color='transparent', font=('JetBrains Mono', 10), text_color='#FFFFFF', anchor='n')
            except Exception as e:
                print(f"Error retrieving positions: {e}")
                line_label = CTkLabel(master=self, text='-', fg_color='transparent', font=('JetBrains Mono', 10), text_color='#FFFFFF', anchor='n')

            self.line_labels.append(line_label)
            line_label.grid(row=row, column=0, sticky='nsew', padx=32, pady=8)

            
            log_message_label = None
            try:
                log_message_label = CTkLabel(master=self, text=str(self.logs[row].string()), fg_color='transparent', font=('JetBrains Mono', 10), text_color='#ff5349', anchor='nw', justify="left")
            except:
                log_message_label = CTkLabel(master=self, text=str(self.logs[row]), fg_color='transparent', font=('JetBrains Mono', 10), text_color='#ff5349', anchor='nw', justify="left")
            
            self.log_message_labels.append(log_message_label)
            log_message_label.grid(row=row, column=1, sticky='nsew', columnspan=9, pady=8)

            # Bind event handlers correctly
            log_message_label.bind("<Enter>", lambda ev, sp=start_pos, ep=end_pos: self.highlight_error(ev, sp, ep))
            log_message_label.bind("<Leave>", lambda ev: self.clear_highlight(ev))

    def highlight_error(self, ev, start_pos, end_pos=None):
        """ Highlight the text in the code editor based on the error positions. """
        if not end_pos:  # Adjust if end_pos is not given
            line_content = self.code_editor.text.get(f"{start_pos[0]+1}.0", f"{start_pos[0]+1}.end")
            end_pos = self.adjust_position(start_pos, line_content)
        self.code_editor.format(Tags.ERROR_HIGHLIGHT.name, start_pos, end_pos)

    def adjust_position(self, start_pos, line_content):
        """ Adjust the end position based on line content, extending to next space or end of line. """
        # Find the next space starting from start_pos[1] within the line content
        end_index = line_content.find(' ', start_pos[1])
        if end_index == -1:
            # If no space is found, extend to the end of the line
            end_index = len(line_content)
        else:
            # Adjust end_index to be absolute position in the line, not relative to start_pos[1]
            end_index += start_pos[1]

        return (start_pos[0], end_index)
        
    def clear_highlight(self, ev):
        """ Clear any highlighting in the code editor. """
        self.code_editor.clear_format()

    def delete_labels(self):
        """ Destroy all labels when refreshing or clearing the log table. """
        for label in self.line_labels + self.log_message_labels:
            label.destroy()
        self.line_labels.clear()
        self.log_message_labels.clear()

class LogsCanvas(CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0,highlightthickness=0, bg='#16161E')

        self.table: LogsTable | None = None 
        self.grid_columnconfigure((0,1), weight=1)

        self.render_table()

    def render_table(self, errors: list[Error] = []):
        self.logs_table = LogsTable(
            master=self,
            fg_color='transparent',
            logs=errors
        )
        self.logs_table.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.table = self.logs_table

    def update_logs(self, errors: list[Error]):
        if self.table:
            self.table.delete_labels()

        self.render_table(errors=errors)