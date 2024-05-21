import re

from customtkinter import *
from tkinter import *

from src.lexer import Token
from .code_view import Remote, Tags


class LexerTable(CTkFrame):
    def __init__(self, master, tokens: list[Token], **kwargs):
        super().__init__(master, **kwargs)
        self.tokens = tokens
        self.columns = (0, 1)
        self.grid_columnconfigure(self.columns, weight=1)

        self.code_editor = Remote.code_editor_instance
        self.lexemes_labels = []
        self.token_labels = []
        self.tooltips = []  # Store tooltip instances to avoid garbage collection

        for i, token in enumerate(self.tokens):
            # Clean up lexeme and token values, remove index hints like [1]
            lex = re.sub(r'\[\d*\]', '', token.lexeme)
            tok = re.sub(r'\[\d*\]', '', str(token.token))

            # Remove array info on lexeme
            lex = token.lexeme
            pattern = r".+\[[\d]*\]"  # Matches strings that have [] or [x] in the end
            matched = re.search(pattern, lex)
            if matched:
                lex = lex.split("[")[0]
            lexeme_label = CTkLabel(master=self, text=lex, fg_color='transparent', font=('JetBrains Mono', 13), text_color='#FFFFFF')

            token_label = None
            if(token.is_unique_type()):
                token_label = CTkLabel(master=self, text=token.token.unique_type, fg_color='transparent', font=('JetBrains Mono', 13), text_color='#FFFFFF')
            else:
                # Remove array info on lexeme
                tok = token.token.string()
                pattern = r".+\[[\d]*\]"  # Matches strings that have [] or [x] in the end
                matched = re.search(pattern, tok)
                if matched:
                    tok = tok.split("[")[0]
                token_label = CTkLabel(master=self, text=tok, fg_color='transparent', font=('JetBrains Mono', 13), text_color='#FFFFFF')

            # Check if lexeme exceeds 15 characters
            display_lex = lex if len(lex) <= 15 else lex[:12] + '...'

            # Create labels
            lexeme_label = CTkLabel(master=self, text=display_lex, fg_color='transparent', font=('JetBrains Mono', 13), text_color='#FFFFFF')
            token_label = CTkLabel(master=self, text=tok, fg_color='transparent', font=('JetBrains Mono', 13), text_color='#FFFFFF')

            lexeme_label.grid(row=i*2, column=0, sticky='ew')
            token_label.grid(row=i*2, column=1, sticky='ew')

            # Create tooltips and bind hover events to show full text
            lexeme_tooltip = ToolTip(lexeme_label)
            token_tooltip = ToolTip(token_label)
            
            # Bind combined functions for hover and tooltip display
            lexeme_label.bind("<Enter>", lambda ev, t=token, tip=lexeme_tooltip, text=lex: self.combined_enter(t, tip, text))
            token_label.bind("<Enter>", lambda ev, t=token, tip=token_tooltip, text=tok: self.combined_enter(t, tip, text))

            # Bind combined function for clicks
            lexeme_label.bind("<Button-1>", lambda ev, t=token: self.on_click(t))
            token_label.bind("<Button-1>", lambda ev, t=token: self.on_click(t))

            # Leave handlers for tooltips
            lexeme_label.bind("<Leave>", lambda ev, tip=lexeme_tooltip: tip.hide())
            token_label.bind("<Leave>", lambda ev, tip=token_tooltip: tip.hide())

            # Store tooltips to prevent garbage collection
            self.tooltips.extend([lexeme_tooltip, token_tooltip])

            # Separator line
            separator_line = CTkCanvas(master=self, height=2, bg='#16161e', highlightthickness=0)
            separator_line.grid(row=i * 2 + 1, column=0, columnspan=2, sticky='ew')

            self.lexemes_labels.append(lexeme_label)
            self.token_labels.append(token_label)
    
    def delete_labels(self):
        if(len(self.lexemes_labels) > 0 and len(self.token_labels) > 0):
            for i in range(len(self.lexemes_labels)):
                self.lexemes_labels[i].destroy()
                self.token_labels[i].destroy()
            self.lexemes_labels = []
            self.token_labels = []

    def on_hover(self, token):
        self.code_editor.format(Tags.TOKEN_HIGHLIGHT.name, tuple(token.position), tuple(token.end_position))

    def on_click(self, token):
        positions = [(_t.position, _t.end_position) for _t in self.tokens if str(_t.token) == str(token.token)]
        self.code_editor.format_multiple(Tags.TOKEN_HIGHLIGHT.name, positions)
    
    def combined_enter(self, token, tooltip, text):
        """
            Handle mouse enter event by activating hover effect and showing tooltip.
        """
        self.on_hover(token)  # Your existing hover function
        tooltip.show(text)    # Show tooltip with full text


class LexerCanvas(CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        CTkCanvas.__init__(self, master=master, width=16, borderwidth=0, highlightthickness=0, bg='#1A1B26')

        self.table: LexerTable | None = None

        self.grid_columnconfigure((0, 1), weight=1)

        self.render_table()

    def render_table(self, tokens: list[Token] = []):
        self.lexer_table = LexerTable(
            master=self,
            fg_color='transparent',
            tokens=tokens
        )
        self.lexer_table.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.table = self.lexer_table

    def update_lexer(self, tokens: list[Token]):
        if self.table:
            self.table.delete_labels()

        self.render_table(tokens=tokens)

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show(self, text):
        """
            Display text in tooltip window
        """
        if self.tip_window or not text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=text, justify=LEFT, background="#ffffe0", relief=SOLID, borderwidth=1, font=("JetBrains Mono", "10"))
        label.pack(ipadx=1)

    def hide(self):
        tw = self.tip_window
        tw.destroy() if tw else None
        self.tip_window = None