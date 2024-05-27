from customtkinter import *
from .logs_table import LogsCanvas
from PIL import Image, ImageTk
from constants.path import *
from src.components.code_view import CodeEditor
from .util import generate_log

class GeneratedLogFrame(CTkFrame):
    def __init__(self, master, generated_log: dict, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.generated_log = generated_log
        print(self.generated_log)
        for i, (k, v) in enumerate(self.generated_log.items()):
            if(v):
                self.generated_log_label = CTkLabel(master=self, text=v if not v else f">\t{k}: {v}", text_color='#FFFFFF', font=('JetBrains Mono', 11))
                self.generated_log_label.grid(row=i, column=0, sticky="nw")
        
class CompilerLogsCanvas(CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0,bg='#16161E', highlightthickness=0)
        self.grid_columnconfigure((0,1), weight=1)

        self.init_compiler_messages = [">\tWelcome to UwU++ IDE! The IDE supports the following shortcuts:", ">\tPress F3 to auto-format the code", ">\tPress F4 to quick run the program", ">\tPress F5 to run the program", ">\tPress Ctrl+N to add a new tab", ">\tPress Ctrl+S to save the program", ">\tPress Ctrl+O to import a program", ">\tStart coding u qtpie 💖💖💖"]

        self.labels = []

        for i, message in enumerate(self.init_compiler_messages):
            intro_label = CTkLabel(master=self, text=message, text_color='#FFFFFF', font=('JetBrains Mono', 11))
            intro_label.grid(row=i, column=0, sticky="nw")
            self.labels.append(intro_label)
    
    def render_logs(self, lx_errors: list, p_errors: list, a_errors: list, is_compiling = False, is_formatting = False):
        generated_log = generate_log(lx_errors=lx_errors, p_errors=p_errors, a_errors=a_errors, is_compiling=is_compiling, is_formatting = is_formatting)

        self.generated_log_frame = GeneratedLogFrame(master=self, fg_color='transparent', generated_log=generated_log)
        self.generated_log_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

    def update_logs(self, editor: CodeEditor, is_compiling, generated_log = None, is_formatting = False):
        if len(self.labels) > 0:
            for label in self.labels:
                label.destroy()
            
            self.labels = []

        if(generated_log):
            self.generated_log_frame = GeneratedLogFrame(master=self, fg_color='transparent', generated_log=generated_log)
            self.generated_log_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        else:
            self.render_logs(lx_errors=editor.lx_errors,p_errors=editor.p_errors, a_errors=editor.a_errors, is_compiling=is_compiling, is_formatting = is_formatting)

class CompilerLogs(CTkScrollableFrame):
    def __init__(self, master, editor: CodeEditor, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.editor = editor

        self.compiler_logs_canvas = CompilerLogsCanvas(master=self)
        self.compiler_logs_canvas.grid(row=0, column=0, sticky="nsew")
        
        self.update_logs = self.compiler_logs_canvas.update_logs

class CompilerErrors(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=10)

        self.line_label = CTkLabel(master=self, text='Line', bg_color='#333652', text_color='#FFFFFF', font=('JetBrains Mono', 13))
        self.log_message_label = CTkLabel(master=self, text='Message', bg_color='#333652', text_color='#FFFFFF', anchor='w', font=('JetBrains Mono', 13))

        self.line_label.grid(row=0, column=0, sticky='nsew')
        self.log_message_label.grid(row=0, column=1, columnspan=13, sticky='nsew')

        self.logs_table = LogsCanvas(master=self)
        self.logs_table.grid(row=1, column=0, columnspan=12, sticky='nsew')

        self.update_logs = self.logs_table.update_logs

class ConsoleView(CTkTabview):
    def __init__(self, master, editor: CodeEditor, **kwargs):
        super().__init__(master, **kwargs)

        self.compiler_logs_tab = self.add('Compiler Logs')
        self.compiler_errors_tab = self.add('Compiler Errors')

        self.compiler_logs_tab.grid_columnconfigure((0,1), weight=1)
        self.compiler_errors_tab.grid_columnconfigure((0,1), weight=1)

        self.compiler_logs = CompilerLogs(self.compiler_logs_tab, editor=editor, fg_color='transparent')
        self.compiler_logs.grid(row=0,column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.compiler_errors = CompilerErrors(self.compiler_errors_tab, fg_color='transparent')
        self.compiler_errors.grid(row=0,column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.update_error_logs = self.compiler_errors.update_logs
        self.update_compiler_logs = self.compiler_logs.update_logs
        