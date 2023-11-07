from customtkinter import *

from src.lexer import Token
from .code_view import Remote, Tags


class LexerTable(CTkFrame):
    def __init__(self, master, tokens: list[Token], **kwargs):
        super().__init__(master, **kwargs)
        self.tokens = tokens
        self.columns = (0, 1)
        self.rows = tuple([i for i in range(len(self.tokens))]) if len(self.tokens) > 0 else (0, 1, 2, 3, 4)

        self.grid_columnconfigure(self.columns, weight=1)
        self.grid_rowconfigure(self.rows, weight=1)

        code_editor = Remote.code_editor_instance
        self.lexemes_labels = []
        self.token_labels = []
        for i, token in enumerate(self.tokens):
            lexeme_label = CTkLabel(master=self, text=token.lexeme, fg_color='transparent', text_color='#FFFFFF')
            token_label = CTkLabel(master=self, text=token.token, fg_color='transparent', text_color='#FFFFFF')

            lexeme_label.grid(row=i, column=0, sticky='ew')
            token_label.grid(row=i, column=1, sticky='ew')

            # Bind callbacks for token highlighting
            lexeme_label.bind("<Enter>", lambda ev, t=token: code_editor.format(Tags.TOKEN_HIGHLIGHT.name,
                                                                                tuple(t.position),
                                                                                tuple(t.end_position)))
            token_label.bind("<Enter>", lambda ev, t=token: code_editor.format(Tags.TOKEN_HIGHLIGHT.name,
                                                                               tuple(t.position),
                                                                               tuple(t.end_position)))
            lexeme_label.bind("<Leave>", lambda ev: code_editor.clear_format())
            token_label.bind("<Leave>", lambda ev: code_editor.clear_format())

            self.lexemes_labels.append(lexeme_label)
            self.token_labels.append(token_label)


class LexerCanvas(CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0, highlightthickness=0, bg='#1A1B26')

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.render_table()

    def render_table(self, tokens: list[Token] = []):
        self.lexer_table = LexerTable(
            master=self,
            fg_color='transparent',
            tokens=tokens
        )
        self.lexer_table.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

    def update_lexer(self, tokens: list[Token]):
        self.delete('all')
        self.render_table(tokens=tokens)
