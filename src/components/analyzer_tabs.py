from tkinter import ttk
from customtkinter import *
from .lexer_table import LexerCanvas

class UwUParserTab(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)

        treestyles = ttk.Style()
        treestyles.theme_use('default')
        treestyles.configure('Treeview', background="#1A1B26", foreground="#FFFFFF", fieldbackground="#1A1B26", borderwidth=0)
        treestyles.map('Treeview', background=[('selected', "#1A1B26")], foreground=[('selected', "#89ca78")])

        tree = ttk.Treeview(self, height=36, show='tree')
        tree.insert('', 'end', text='Mainuwu', iid=0, open=False)
        tree.insert('', 'end', text='Functions', iid=1, open=False)
        tree.insert('', 'end', text='Globals', iid=2, open=False)
        tree.insert('', 'end', text='Classes', iid=3, open=False)

        tree.insert('0', 'end', iid=4, text='Function')
        tree.insert('1', 'end', iid=5, text='Function')
        tree.insert('2', 'end', iid=6, text='Declare')
        tree.insert('3', 'end', iid=7, text='Class')

        # mainuwu
        tree.insert('4', 'end', 'mainuwu',text="mainuwu")
        tree.insert('mainuwu', 'end', 'mainuwu-rtype',text="rtype")
        tree.insert('mainuwu', 'end', 'mainuwu-paramters',text="parameters")
        tree.insert('mainuwu', 'end', 'mainuwu-body',text="body")

        # function
        tree.insert('5', 'end', 'subfn1',text="testfn1")
        tree.insert('subfn1', 'end', 'subfn1-rtype',text="rtype")
        tree.insert('subfn1', 'end', 'subfn1-paramters',text="parameters")
        tree.insert('subfn1', 'end', 'subfn1-body',text="body")

        tree.insert('5', 'end', 'subfn2',text="testfn2")
        tree.insert('subfn2', 'end', 'subfn2-rtype',text="rtype")
        tree.insert('subfn2', 'end', 'subfn2-paramters',text="parameters")
        tree.insert('subfn2', 'end', 'subfn2-body',text="body")

        tree.grid(row=0, column=0, columnspan=2, sticky='nsew')

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