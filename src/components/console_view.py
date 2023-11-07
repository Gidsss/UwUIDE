from customtkinter import *
from .logs_table import LogsCanvas
from PIL import Image, ImageTk
from constants.path import *


class CompilerLogs(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=10)

        self.line_label = CTkLabel(master=self, text='Line', bg_color='#333652', text_color='#FFFFFF')
        self.log_message_label = CTkLabel(master=self, text='Message', bg_color='#333652', text_color='#FFFFFF', anchor='w')

        self.line_label.grid(row=0, column=0, sticky='nsew')
        self.log_message_label.grid(row=0, column=1, columnspan=13, sticky='nsew')

        self.logs_table = LogsCanvas(master=self)
        self.logs_table.grid(row=1, column=0, columnspan=12, sticky='nsew')

        self.update_logs = self.logs_table.update_logs
        
class Console(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # TODO: Implement cursor functionality in the future
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1,2,3,4,5,6,7,8,9,10), weight=2)
        self.grid_rowconfigure((0), weight=1)
        self.console_cursor = CTkLabel(master=self, text='>', bg_color='transparent', text_color='#FFFFFF')

        self.console_cursor.grid(row=0, column=0, sticky='n')

class ConsoleView(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.compiler_logs_tab = self.add('Compiler logs')
        self.console_tab = self.add('Console')

        self.compiler_logs_tab.grid_columnconfigure((0,1), weight=1)
        self.compiler_logs_tab.grid_rowconfigure((0,1), weight=1)

        self.console_tab.grid_columnconfigure((0,1), weight=1)
        self.console_tab.grid_rowconfigure((0,1), weight=1)

        self.compiler_logs = CompilerLogs(self.compiler_logs_tab, fg_color='transparent')
        self.compiler_logs.grid(row=0,column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.console = Console(self.console_tab, fg_color='transparent')
        self.console.grid(row=0,column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.update_logs = self.compiler_logs.update_logs
        