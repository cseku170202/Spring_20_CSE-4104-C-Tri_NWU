import tkinter as tk
from tkinter import ttk

operators = ['+', '-', '*', '/', '=', '==', '<', '>', '<=', '>=', '!=']
separators = ['(', ')', '{', '}', ';', ',']

symbol_table = {}

def analyze_tokens():
    input_str = input_text.get("1.0", "end").strip()
    tokens = input_str.split()
    analyzed_tokens = []

    for token in tokens:
        if token in operators:
            analyzed_tokens.append(("Operator", token))
            symbol_table[token] = None  # Add the operator to the symbol table with a default value
        elif token in separators:
            analyzed_tokens.append(("Separator", token))
        elif token.isalpha():
            analyzed_tokens.append(("Letter", token))
            symbol_table[token] = None  # Add the symbol to the symbol table with a default value
        elif token.isdigit():
            analyzed_tokens.append(("Number", token))
        else:
            analyzed_tokens.append(("Unknown", token))

    for child in analyze_treeview.get_children():
        analyze_treeview.delete(child)

    for index, (token_type, token_value) in enumerate(analyzed_tokens, start=1):
        analyze_treeview.insert("", "end", values=(index, token_value, token_type))

    # Update the symbol table
    for child in symbol_table_treeview.get_children():
        symbol_table_treeview.delete(child)

    for index, (symbol, value) in enumerate(symbol_table.items(), start=1):
        symbol_table_treeview.insert("", "end", values=(index, symbol, value))

# Create the main application window
root = tk.Tk()
root.title("Token Analyzer")
root.configure(bg="light blue")

# Create headline label for the input table
headline_label = tk.Label(root, text="Input Here", font=("Arial", 14, "bold"), bg="light blue")
headline_label.pack(pady=10)

# Create input text box
input_text = tk.Text(root, height=10, width=60)
input_text.pack(padx=10, pady=5)

# Create analyze button
analyze_button = tk.Button(root, text="Analyze Tokens", command=analyze_tokens)
analyze_button.pack(pady=10)

# Create analyze table
analyze_treeview = ttk.Treeview(root, columns=("Serial No.", "Token", "Lexeme"))
analyze_treeview.heading("Serial No.", text="Serial No.")
analyze_treeview.heading("Token", text="Token")
analyze_treeview.heading("Lexeme", text="Lexeme")
analyze_treeview.pack()

# Create symbol table
symbol_table_label = tk.Label(root, text="Symbol Table", font=("Arial", 14, "bold"), bg="light blue")
symbol_table_label.pack(pady=10)

symbol_table_treeview = ttk.Treeview(root, columns=("Serial No.", "Symbol", "Value"))
symbol_table_treeview.heading("Serial No.", text="Serial No.")
symbol_table_treeview.heading("Symbol", text="Symbol")
symbol_table_treeview.heading("Value", text="Value")
symbol_table_treeview.pack()

# Start the main event loop
root.mainloop()
