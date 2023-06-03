import re
import tkinter as tk
from tkinter import ttk


class Lexer:
    def __init__(self):
        self.keywords = ['if', 'else', 'while', 'for', 'return', 'int', 'float','null' 'double','include ', 'char', 'elseif', 'print', 'true', 'false']
        self.symbols = ['(', ')',('# '), '{', '}', '=', '+', '-', '*', '/', '<=', '>=', '==', '<', '>', '++', '--']
        self.symbol_table = {}
        self.value_table=["null"]
        self.function = ["main"]
        self.Special_Characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
        self.identifier_table = {}


    def tokenize(self, code):

        tokens = []
        pattern = re.compile(r'(\d+)|(\w+)|(\S)', re.MULTILINE)
        matches = pattern.findall(code)

        for match in matches:
            if match[0]:
                tokens.append(('NUMBER', match[0]))
            elif match[1]:
                if match[1] in self.keywords:
                    tokens.append(('keyword', match[1]))
                else:
                    if match[1] not in self.symbol_table:
                        self.symbol_table[match[1]] = None
                        self.identifier_table[match[1]] = 1
                    else:
                        self.identifier_table[match[1]] += 1
                    tokens.append(('identifier', match[1]))




            elif match[2]:
                if match[2] in self.symbols:
                    tokens.append(('operator', match[2]))
                else:
                    tokens.append(('symbol', match[2]))

        return tokens

    def get_identifier_table(self):
        return [(identifier) for identifier in self.identifier_table.items()]

    def clear(self, code):
      pass


class App:
    def __init__(self, master):

        self.master = master
        self.master.title("LEXICAL ANALYZER")
        self.create_widgets()


    def create_widgets(self):
        # Code input
        self.code_label = tk.Label(self.master, text="Code:", font=15)
        self.code_label.grid(row=0, column=0)
        self.code_text = tk.Text(self.master, width=40, height=15)
        self.code_text.grid(row=1, column=0)



            # Token output
        self.token_label = tk.Label(self.master, text="Tokens:", font=20)
        self.token_label.grid(row=0, column=1)
        self.token_tree = ttk.Treeview(self.master, columns=("Analyze name", "Tokens"), show="headings")
        self.token_tree.heading("Analyze name", text="Analyze name")
        self.token_tree.heading("Tokens", text="Tokens")

        self.token_tree.grid(row=1, column=1)

        # symbol table output
        self.id_label = tk.Label(self.master, text="Symbol table:", font=19)
        self.id_label.grid(row=0, column=2)
        self.id_tree = ttk.Treeview(self.master, columns=("indentifier name", "line","value"), show="headings")
        root.configure(background="SteelBlue")
        root.geometry("1300x500")
        self.id_tree.heading("indentifier name", text="indentifier name")
        self.id_tree.heading("line", text="line")
        self.id_tree.heading("value", text="value")
        self.id_tree.grid(row=1, column=2)


        # Tokenize button
        self.tokenize_button = tk.Button(self.master, text="Tokenize", fg='white', bg='MidnightBlue', padx=20, pady=10, command=self.tokenize)
        self.tokenize_button.grid(row=4, column=1)


    def tokenize(self):
        code = self.code_text.get("1.0", "end-1c")
        lexer = Lexer()
        tokens = lexer.tokenize(code)
        self.display_tokens(tokens)
        self.display_identifier_table(lexer.get_identifier_table())

    def display_tokens(self, tokens):
        self.token_tree.delete(*self.token_tree.get_children())
        for token in tokens:
            self.token_tree.insert("", "end", values= token ,)


    def display_identifier_table(self, id_table):
        self.id_tree.delete(*self.id_tree.get_children())
        for row in id_table:
            self.id_tree.insert("", "end", values=row)

    def display_value_table(self, value_table):
        self.value_table_tree.delete(*self.value_table_tree.get_children())
        for token in value_table:
            self.value_table_tree.insert("", "end", values=(value_table, "null"))


def clear(self):
    code = self.code_text.get("1.0", "end-1c")
    lexer = Lexer()
    tokens = lexer.clear(code)
    self.display_tokens(tokens)
    self.display_identifier_table(lexer.get_identifier_table())


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
