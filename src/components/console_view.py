from customtkinter import *
from .logs_table import LogsCanvas
from PIL import Image, ImageTk
from constants.path import *
from src.components.code_view import CodeEditor

class GeneratedLogFrame(CTkFrame):
    def __init__(self, master, generated_log: dict, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.generated_log = generated_log
        print(self.generated_log)
        for i, (k, v) in enumerate(self.generated_log.items()):
            if(v):
                self.generated_log_label = CTkLabel(master=self, text=v if not v else f">\t{k}: {v}", text_color='#FFFFFF', font=('JetBrains Mono', 10))
                self.generated_log_label.grid(row=i, column=0, sticky="nw")
        
class CompilerLogsCanvas(CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0,bg='#16161E', highlightthickness=0)
        self.grid_columnconfigure((0,1), weight=1)

        self.intro_label = CTkLabel(master=self, text=">\tWelcome to UwU++ IDE! Start cowding ^_^", text_color='#FFFFFF', font=('JetBrains Mono', 10))
        self.intro_label.grid(row=0, column=0, sticky="nw")

    def generate_log(self, lx_errors: list, p_errors: list) -> dict:
        return {
            "Status": "Compiler compiled successfully" if len(lx_errors) == 0 and len(p_errors) == 0 else "Compiler compiled with errors",
            "Lexical Errors": len(lx_errors) if len(lx_errors) > 0 else None,
            "Syntax Errors": len(p_errors) if len(p_errors) > 0 else None
        }
    
    def render_logs(self, lx_errors: list, p_errors: list):
        generated_log = self.generate_log(lx_errors=lx_errors, p_errors=p_errors)

        self.generated_log_frame = GeneratedLogFrame(master=self, fg_color='transparent', generated_log=generated_log)
        self.generated_log_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

    def update_logs(self, editor: CodeEditor):
        self.delete('all')
        self.render_logs(lx_errors=editor.lx_errors,p_errors=editor.p_errors)

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
        