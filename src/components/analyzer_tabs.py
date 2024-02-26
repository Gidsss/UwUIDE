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
        self.tree_items = []
        self.tree.insert('', 'end', text='Mainuwu', iid=0, open=False)
        self.tree.insert('', 'end', text='Functions', iid=1, open=False)
        self.tree.insert('', 'end', text='Globals', iid=2, open=False)
        self.tree.insert('', 'end', text='Classes', iid=3, open=False)

        self.tree.grid(row=0, column=0, columnspan=2, sticky='nsew')
    
    def update_parser_tree(self, program: Program):
        def traverse_tree(node, parent: str | Production | None = None):
            """
                Recursively loop the tree
            """
            if(node.child_nodes() == None):
                self.tree.insert(parent, 'end', text=node.header())
                return
            
            node_iid = uuid.uuid4()
            self.tree_items.append(node_iid)

            self.tree.insert(parent, 'end', iid=node_iid, text=node.header())
            try:
                print(node.condition)
            except:
                pass
            
            for n in node.child_nodes():
                if(not isinstance(n, Production)):
                    if n:
                        if(not isinstance(n, list)):
                            self.tree.insert(node_iid, 'end', text=n)
                        else:
                            for p in n:
                                traverse_tree(node=p, parent=node_iid)
                else:
                    traverse_tree(node=n, parent=node_iid)

        if(len(self.tree_items) > 0):
            for item in self.tree_items:
                try:
                    self.tree.delete(item)
                except:
                    continue
            
            self.tree_items = []

        traverse_tree(node=program.mainuwu, parent='0')
        
        for fn in program.functions:
            traverse_tree(node=fn, parent='1')
        
        for g in program.globals:
            traverse_tree(node=g, parent='2')

        for c in program.classes:
            traverse_tree(node=c, parent='3')

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