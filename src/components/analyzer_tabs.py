import uuid
from tkinter import ttk
from customtkinter import *
from .lexer_table import LexerCanvas
from src.parser import Production, Program
from .code_view import Remote, Tags

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
        self.tree.bind("<ButtonRelease-1>", self.highlight)
        self.tree.bind("<Leave>", self.clear_highlight)
        self.iid_dict = {}

        self.tree.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.code_editor = Remote.code_editor_instance
    
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
                node_id = self.tree.insert(parent, 'end', text=f"{key}: {node.header()}" if key else node.header())
                self.iid_dict.update({node_id: node})
                return
            
            node_iid = uuid.uuid4()
            self.iid_dict.update({str(node_iid): node})

            self.tree.insert(parent, 'end', iid=node_iid, text=f"{key}: {node.header()}" if key else node.header(), open=True)

            for k, v in node.child_nodes().items():
                if v and not isinstance(v, Production):
                    child_node_id = self.tree.insert(node_iid, 'end', text=f"{k}: {v}")
                    self.iid_dict.update({str(child_node_id): v})
                elif v:
                    loop_tree(node=v, parent=node_iid, key=k)

        self.clear_parser_tree()

        if(program.mainuwu):
            self.tree.insert('', 'end', text='Mainuwu', iid=0, open=True)
            self.iid_dict.update({'0': program.mainuwu})
            loop_tree(node=program.mainuwu, parent='0')
        
        if(len(program.functions) > 0):
            self.tree.insert('', 'end', text='Functions', iid=1, open=True)
            self.iid_dict.update({'1': program.functions})
            for fn in program.functions:
                loop_tree(node=fn, parent='1')
        
        if(len(program.globals) > 0):
            self.tree.insert('', 'end', text='Globals', iid=2, open=True)
            self.iid_dict.update({'2': program.globals})
            for g in program.globals:
                loop_tree(node=g, parent='2')

        if(len(program.classes) > 0):
            self.tree.insert('', 'end', text='Classes', iid=3, open=True)
            self.iid_dict.update({'3': program.classes})
            for c in program.classes:
                loop_tree(node=c, parent='3')

    def highlight(self, event):
        # Highlights the hovered node in the source code
        self.code_editor = Remote.code_editor_instance
        selected = self.tree.focus()
        if selected in self.iid_dict.keys():
            value = self.iid_dict[selected]
            if isinstance(value, Production):
                if value.start_pos and value.end_pos:
                    self.code_editor.format(Tags.TOKEN_HIGHLIGHT.name, tuple(value.start_pos), tuple(value.end_pos))
            elif isinstance(value, list):
                func_ranges = [(func.start_pos, func.end_pos) for func in value]
                self.code_editor.format_multiple(Tags.TOKEN_HIGHLIGHT.name, func_ranges)
            else:
                self.code_editor.format(Tags.TOKEN_HIGHLIGHT.name, tuple(value.position), tuple(value.end_position))

    def clear_highlight(self, event):
        self.code_editor = Remote.code_editor_instance
        if(self.code_editor):
            self.code_editor.clear_format()

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
