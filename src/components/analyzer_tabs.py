import uuid
from tkinter import ttk
from customtkinter import *
from .lexer_table import LexerCanvas
from src.parser import Production, Program

class UwUParserTab(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)

        treestyles = ttk.Style()
        treestyles.theme_use('default')
        treestyles.configure('Treeview', background="#1A1B26", foreground="#FFFFFF", fieldbackground="#1A1B26", borderwidth=0)
        treestyles.map('Treeview', background=[('selected', "#1A1B26")], foreground=[('selected', "#89ca78")])

        self.tree = ttk.Treeview(self, height=100, show='tree')

        self.tree.grid(row=0, column=0, columnspan=2, sticky='nsew')
    
    def clear_parser_tree(self):
        if(len(self.tree.get_children()) > 0):
            for item in self.tree.get_children():
                self.tree.delete(item)

    def update_parser_tree(self, program: Program):
        def loop_tree(node, parent: str |  None = None, key: str | None = None):
            """
                Recursively loop the tree
            """
            if(node.child_nodes() == None):
                self.tree.insert(parent, 'end', text=f"{key}: {node.header()}" if key else node.header())
                return
            
            node_iid = uuid.uuid4()

            self.tree.insert(parent, 'end', iid=node_iid, text=f"{key}: {node.header()}" if key else node.header())

            for k, v in node.child_nodes().items():
                if v and not isinstance(v, Production):
                    self.tree.insert(node_iid, 'end', text=f"{k}: {v}")
                else:
                    loop_tree(node=v, parent=node_iid, key=k)

        self.clear_parser_tree()

        if(program.mainuwu):
            self.tree.insert('', 'end', text='Mainuwu', iid=0, open=False)
            loop_tree(node=program.mainuwu, parent='0')
        
        if(len(program.functions) > 0):
            self.tree.insert('', 'end', text='Functions', iid=1, open=False)
            for fn in program.functions:
                loop_tree(node=fn, parent='1')
        
        if(len(program.globals) > 0):
            self.tree.insert('', 'end', text='Globals', iid=2, open=False)
            for g in program.globals:
                loop_tree(node=g, parent='2')

        if(len(program.classes) > 0):
            self.tree.insert('', 'end', text='Classes', iid=3, open=False)
            for c in program.classes:
                loop_tree(node=c, parent='3')

class UwULexerTab(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=10)

        self.lexeme_label = CTkLabel(master=self, text='Lexeme', bg_color='#333652', font=('JetBrains Mono', 13), text_color='#FFFFFF')
        self.token_label = CTkLabel(master=self, text='Token', bg_color='#333652', font=('JetBrains Mono', 13), text_color='#FFFFFF')

        self.lexeme_label.grid(row=0, column=0, sticky='nsew')
        self.token_label.grid(row=0, column=1, sticky='nsew')

        self.lexer_table = LexerCanvas(master=self)
        self.lexer_table.grid(row=1, rowspan=2 ,columnspan=2, sticky='nsew')

        self.update_lexer = self.lexer_table.update_lexer
