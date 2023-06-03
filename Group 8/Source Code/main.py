from tkinter import*
from tkinter import ttk
import re
import nltk

root = Tk()
root.title("Lexical analyzer")

label1 = Label(root, text="Source Code", font="arial 15", background="cyan", foreground="black", padx=200, pady=25)
label1.grid(row=0, column=1, padx=(20, 0))
label2 = Label(root, text="Tokenize", font="arial 15", background="cyan", foreground="black", padx=200, pady=25)
label2.grid(row=0, column=2, padx=(20, 0))

entry = Text(root,  width=60, height=26)
entry.grid(row=1, column=1, padx=(20, 0))


def clear2():
    entry.delete("1.0", "end")


tree_scroll = Scrollbar(root, orient=VERTICAL)

my_tree = ttk.Treeview(root)

my_tree.configure(yscrollcommand=tree_scroll.set)

tree_scroll.configure(command=my_tree.yview)

style1 = ttk.Style()

style1.configure("Treeview",
                foreground="black",
                rowheight=40,
                fieldbackgound="black"
                )
style1.map('Treeview',
          background=[('selected', 'cyan')])
my_tree['columns'] = ("line", "Tokens", "Analyze")

my_tree.column("#0", width=0, minwidth=NO)
my_tree.column("line", anchor=CENTER, width=50)
my_tree.column("Tokens", anchor=CENTER, width=200)
my_tree.column("Analyze", anchor=CENTER, width=200)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("line", text="Line", anchor=CENTER)
my_tree.heading("Tokens", text="Tokens", anchor=CENTER)
my_tree.heading("Analyze", text="Tokenize", anchor=CENTER)

arrId1 = []
arrId2 = []
arrId3 = []
arrId4 = []
arrId5 = []
arrVl = []

def show():

    input_program = entry.get(1.0, END)

    input_program_tokens = nltk.wordpunct_tokenize(input_program);

    RE_Datatype = "int|float|char|string|double|long"
    RE_Header = "include|stdio|h"
    RE_Keywords = "auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typeof|union|unsigned|void|while|string|class|struc"
    RE_Operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(==)|(<=)|(>=)|(<)|(>)"
    RE_Numerals = "^(\d+)$"
    RE_Special_Characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
    RE_Identifiers = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    RE_Strings = 'r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"'
    RE_mfunction = "main"
    RE_bfun = "scanf|printf"

    count = 0
    i = 1

    for token in input_program_tokens:

        if (re.findall(RE_mfunction, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "main function"))

        elif (re.findall(RE_Strings, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "String"))

        elif (re.findall(RE_bfun, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Built in Function"))

        elif (re.findall(RE_Datatype, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Data type"))
            arrId5.append(token)

        elif (re.findall(RE_Keywords, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Keyword"))

        elif (re.findall(RE_Header, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Header"))

        elif (re.findall(RE_Operators, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Operator"))

        elif (re.findall(RE_Numerals, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Number"))

        elif (re.findall(RE_Special_Characters, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Symbol"))

        elif (re.findall(RE_Identifiers, token)):
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Identifier"))
            arrId1.append(token)

        else:
            my_tree.insert(parent='', index='end', text="", values=(count, token, "Error"))

        if (token == ";"):
            count = count + 1
        if (input_program_tokens[i-1] == "{" and input_program_tokens[i-2] == ")" and input_program_tokens[i-3] == "(" and input_program_tokens[i-4] == "main") :
            count = count + 1

        if (token == "="):
            arrVl.append(input_program_tokens[i])
            arrId2.append(input_program_tokens[i-2])

        i = i + 1

        if (token == "_"):
            arrId5.append(input_program_tokens[i])
            i=i+1

    arrId3 = list(set(arrId1) - set (arrId2))

    for tok in arrId3:
        arrId4.append(tok)

def clear():

            for record in my_tree.get_children():
                my_tree.delete(record)

def symbol():
    root2 = Tk()
    root2.title("Symbol Table")

    label = Label(root2, text="Symbol Table", font="arial 15", background="black", foreground="white", padx=400, pady=20)
    label.grid(row=0, column=1, pady=(0, 0))

    tree_scroll = Scrollbar(root2, orient=VERTICAL)
    my_tree2 = ttk.Treeview(root2)

    my_tree2.configure(yscrollcommand=tree_scroll.set)
    style2 = ttk.Style()

    style2.configure("Treeview",
                    background="aqua",
                    foreground="black",
                    rowheight=40,
                    fieldbackgound="red",
                    )
    style2.map('Treeview',
              background=[('selected', 'blue')])

    my_tree2['columns'] = ("name", "value", "datatype")

    my_tree2.column("#0", width=0, minwidth=NO)
    my_tree2.column("name", anchor=CENTER, width=200)
    my_tree2.column("value", anchor=CENTER, width=200)
    my_tree2.column("datatype", anchor=CENTER, width=200)

    my_tree2.heading("#0", text="", anchor=W)
    my_tree2.heading("name", text="Indentifiers", anchor=CENTER)
    my_tree2.heading("value", text="Value", anchor=CENTER)
    my_tree2.heading("datatype", text="Datatype", anchor=CENTER)

    for token4 in arrId4:
        my_tree2.insert(parent='', index='end', text="", values=(token4, " "))
    j = 0

    for token2 in arrId2:
        my_tree2.insert(parent='', index='end', text="", values=(token2, arrVl[j]))
        j=j+1

    my_tree2.grid(row=1, column=1, padx=100, pady=30)
    tree_scroll.config(command=my_tree2.yview)

    root2.mainloop()

my_tree.grid(row=1, column=2, padx=(50, 20))

btn1 = Button(root, text="Analyze", font="arial 15", bg="skyblue", command=show)
btn1.grid(row=2, column=1, ipadx=30, pady=10, padx=(0, 320))
btn2 = Button(root, text="Clear tokenize", font="arial 15", bg="skyblue", command=clear)
btn2.grid(row=2, column=2, pady=10, padx=(0, 280))
btn4 = Button(root, text="Clear Source code", font="arial 15", bg="skyblue", command=clear2)
btn4.grid(row=2, column=1, pady=10, padx=(330,0))
btn3 = Button(root, text="Symbol Table", font="arial 15", bg="skyblue", command=symbol)
btn3.grid(row=2, column=2, ipadx=20, pady=10, padx=(310, 0))

root.mainloop()