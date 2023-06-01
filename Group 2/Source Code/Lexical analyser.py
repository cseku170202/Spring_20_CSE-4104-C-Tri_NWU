import tkinter as tk
import re
from prettytable import PrettyTable
from tkinter.font import Font


KEYWORDS = r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long' \
           r'|register|return|short|signed|sizeof|static|switch|typedef|union|unsigned|void|volatile|while|string' \
           r'|class|struct|include)\b'
Function = r'\b(printf|main|scanf|malloc|calloc|free|strlen|strcmp|strcpy|strcat|memset|memcpy|cout|cin|new|delete|string|vector|map|sort|find)\b'
IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
OPERATOR = r'(\+\+)|(\+)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)|(\$)|(&)|(!)|(,)|(<)|(>)|(\{)|(})|(\^)|(~)|(\[)|(])'
HEADER = r'(#\s*include\s*)([<"][^"\n<>]*\.(h|hpp|H|hh|HPP|hhp|inc|INC)[>"])'
SPECIAL_CHAR = r'[;@#\'\'?:".|=(){}\[\]\\]+'
NUMERAL = r'[0-9]+'
STRING_LITERAL = r'"([^"\\]|\\.|\\\\)*"'
DATA_TYPE = r'\b(int|float|double|char|void)\b'
def extract_tokens(code: str) -> list:
    keyword_regex = re.compile(KEYWORDS)
    function_regex = re.compile(Function)
    header_regex = re.compile(HEADER)
    identifier_regex = re.compile(IDENTIFIER)
    operator_regex = re.compile(OPERATOR)
    special_character_regex = re.compile(SPECIAL_CHAR)
    numeral_regex = re.compile(NUMERAL)
    string_literal_regex = re.compile(STRING_LITERAL)
    comment_regex = re.compile('//.*?$')
    empty_line_regex = re.compile('^\s*$')

    tokens = []
    lines = code.split('\n')
    line_num = 1
    string_literals = []
    for line in lines:
        line = line.strip()
        if not line or comment_regex.match(line) or empty_line_regex.match(line):
            line_num += 1
            continue

        line_tokens = []
        words = re.findall(r'[a-zA-Z][a-zA-Z0-9]*|<\w+\.h>|[;@#?.|=(){}]+|\S', line)

        for word in words:
            if keyword_regex.match(word):
                line_tokens.append((word, 'Keyword', line_num))
            elif function_regex.match(word):
                line_tokens.append((word, 'Function', line_num))
            elif identifier_regex.match(word):
                line_tokens.append((word, 'Identifier', line_num))
            elif string_literal_regex.match(word):
                line_tokens.append((word, 'String Literal', line_num))
                string_literals.append(word)

            elif operator_regex.match(word):
                line_tokens.append((word, 'Operator', line_num))
            elif special_character_regex.match(word):
                line_tokens.append((word, 'Special Character', line_num))
            elif numeral_regex.match(word):
                line_tokens.append((word, 'Numeral', line_num))
            elif match := header_regex.match(word):
                tokens.append((match.group(2), 'Header', line_num))
                tokens.extend(line_tokens)

        tokens.extend(line_tokens)
        line_num += 1

    print("String Literals: ", "  ".join(string_literals))
    return tokens
def display_tokens():
    try:
        code = code_input.get('1.0', tk.END)
        if not code.strip():
            token_display.insert(tk.END, "Please enter some code to analise tokens.\n")
            return
        tokens = extract_tokens(code)
        token_display.delete('1.0', tk.END)
        table = PrettyTable()
        table.field_names = ['Token', 'Keyword', 'Line Number']
        table.align['Token'] = 'c'
        table.align['Keyword'] = 'c'
        table.align['Line Number'] = 'c'

        for token in tokens:
            table.add_row([token[0], token[1], token[2]])
        table_string = table.get_string()
        token_display.insert(tk.END, table_string)
        token_display.tag_configure('center', justify='center')
        token_display.tag_add('center', '1.0', 'end')
        token_display.configure(font=("Courier", 10))

    except tk.TclError as e:
        print(f"Tkinter error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


window = tk.Tk()
window.configure(bg='#ade0d9')
window.title('Lexical Analyzer')

labels = Font(
    family="Arial",
    size=12, weight="bold",slant="roman",underline=1
)

input_label = tk.Label(window, width=50, font=(labels), bg='#668ade',pady='50', text="Enter your code:")
input_label.grid(row=0, column=0, sticky=tk.W, padx=30, pady=20)
code_input = tk.Text(window, font=('Courier', 10), height=25, width=50, bg='#dae8dd', fg='black')
code_input.grid(row=1, column=0, padx=20, pady=20)
output_label = tk.Label(window, width=50, font=(labels),bg='#668ade',pady='50', text="Tokenize")
output_label.grid(row=0, column=1, sticky=tk.W, padx=20, pady=20)
token_display = tk.Text(window, font=('Courier', 10), height=25, width=50,  bg='#dae8dd', fg='black')
token_display.grid(row=1, column=1, padx=10, pady=10)
scrollbar = tk.Scrollbar(window, command=token_display.yview)
scrollbar.grid(row=1, column=2, sticky='ns')
token_display.config(yscrollcommand=scrollbar.set)

button = Font(
    family="Arial",
    size=12, weight="bold",slant="roman",underline=1
)

def clear_widgets():
    code_input.delete('1.0', 'end')
    token_display.delete('1.0', 'end')
# create a button to analyse tokens
extract_button = tk.Button(window, text="Analyze", font=(button), bg='#5f71b3',padx=50, pady= 15, fg='black',
                           command=lambda: display_tokens())
extract_button.grid(row=2, column=0, padx=25, pady=25)

def show_symbol_table():
    global symbol_display

    # create a new window for the symbol table
    symbol_window = tk.Toplevel(window)
    symbol_window.configure(bg='#bacbda')
    symbol_window.title('Symbol Table')

    # add a label and text widget to the symbol window
    symbol_label = tk.Label(symbol_window, width=50, font=(labels), bg='#668ade',pady='50', text="Symbol Table:")
    symbol_label.pack(padx=10, pady=10)

    symbol_display = tk.Text(symbol_window, font=('Courier', 10), height=15, width=50, bg='#e8dada', fg='black')
    symbol_display.pack(padx=10, pady=10)

    # change the background color of symbol_display
    symbol_display.configure(bg='#dedada')

    # extract the tokens from the code in the input field
    code = code_input.get('1.0', tk.END)
    tokens = extract_tokens(code)

    # create symbol table
    sym_table = {}
    for token in tokens:
        if token[1] == 'Identifier':
            sym_table[token[0]] = ['N/A', 'N/A']

    # update symbol table with data type and value
    for i, token in enumerate(tokens):
        if token[1] == 'Identifier':
            if i > 0 and tokens[i - 1][1] in ('Data_Type', 'Header') and tokens[i - 1][0] not in (
                    'if', 'while', 'for'):
                sym_table[token[0]][0] = tokens[i - 1][0]  # data type
            elif i > 0 and tokens[i - 1][1] == 'Operator' and tokens[i - 1][0] == '=':
                sym_table[token[0]][1] = tokens[i + 1][0]  # value

    # create a pretty table instance
    table = PrettyTable()

    # set the field names and alignment
    table.field_names = ['Identifier', 'Data_Type', 'Value']
    table.align['Identifier'] = 'c'
    table.align['Data_Type'] = 'c'
    table.align['Value'] = 'c'

    # add rows to the table
    for identifier, data in sym_table.items():
        table.add_row([identifier, data[0], data[1]])

    # display the table in the symbol_display Text widget
    table_string = table.get_string()
    symbol_display.insert(tk.END, table_string)

    # configure the tag for centering
    symbol_display.tag_configure('center', justify='center')

    # center the table
    symbol_display.tag_add('center', '1.0', 'end')

    # adjust font size
    symbol_display.configure(font=("Courier", 10))


# define symbol_display as a global variable
symbol_display: None = None


symbol_button = tk.Button(window, text="Show Symbol Table", font=(button), bg='#5f71b3', padx=50,pady=15, fg='black',
                          command=show_symbol_table)
symbol_button.grid(row=2, column=1, padx=25, pady=25)
clear_button = tk.Button(window, text="Clear", font=(button), bg='#5f71b3', padx=50,pady=15, fg='black', command=clear_widgets,
                         width=7)
clear_button.grid(row=2, column=0, padx=25, pady=25, columnspan=2)
window.mainloop()