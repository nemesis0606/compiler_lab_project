from tkinter import *
from tkinter import filedialog
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")

filepath_input = ""

def read():
    global filepath_input
    filepath_input = filedialog.askopenfilename()
    x = filepath_input.rfind("/")
    inp_label.configure(text=f"File Selected: {filepath_input[x + 1:]}")

def work():
# Open and read the input file
    with open('input.txt') as file:
        lines = file.readlines()

    # Remove newline characters from each line
    lines = [line.strip() for line in lines]

    # Define a dictionary to store the variables
    variables = {}

    # Open the output file for writing
    with open('output.txt', 'w') as outfile:
        # Loop through each line and execute the corresponding command
        status_label.configure(text="output.txt created")
        for line in lines:
            tokens = line.split()

            # Variable declaration
            if tokens[0] == 'int':
                variables[tokens[1]] = None

            # Variable assignment or arithmetic expression
            elif tokens[0] == 'assign':
                if tokens[3] in variables:
                    val2 = variables[tokens[3]]
                else:
                    val2 = int(tokens[3])
                if len(tokens) == 4:
                    variables[tokens[1]] = val2
                else:
                    operator = tokens[4]
                    if operator == '+':
                        variables[tokens[1]] = variables[tokens[3]] + int(tokens[5])
                    elif operator == '-':
                        variables[tokens[1]] = variables[tokens[3]] - int(tokens[5])
                    elif operator == '*':
                        variables[tokens[1]] = variables[tokens[3]] * int(tokens[5])
                    elif operator == '/':
                        variables[tokens[1]] = variables[tokens[3]] / int(tokens[5])

            # If statement
            elif tokens[0] == 'if':
                cond = tokens[1:-2]
                if eval(" ".join(cond), variables):
                    block = lines[lines.index(line)+1:lines.index('}', lines.index(line))]
                    for command in block:
                        cmd_tokens = command.split()
                        if cmd_tokens[0] == 'display':
                            outfile.write(str(variables[cmd_tokens[1]]) + '\n')

            # Loop statement
            elif tokens[0] == 'loop':
                var_name = tokens[2]
                start = int(tokens[3])
                end = int(tokens[5])
                
                block = lines[lines.index(line)+1:lines.index('}', lines.index(line))]
                for i in range(start, end+1):
                    variables[var_name] = i
                    for command in block:
                        cmd_tokens = command.split()
                        if cmd_tokens[0] == 'display':
                            outfile.write(str(variables[cmd_tokens[1]]) + '\n')

def prev():
    with open('output.txt', 'r') as file:
        # Read the contents of the file
        contents = file.readlines()

    # Display the contents of the file line by line
    s=""
    for line in contents:
        s = s + line + "\n"
    disp_label.configure(text = s)    

    

root = customtkinter.CTk()
root.title('Compiler')
root.geometry("400x600")

# Filepath Inp Label Setup
inp_label = customtkinter.CTkLabel(root,text="No file selected.")
inp_label.pack(padx=10, pady=20)

# Browse Script Button
inp_btn = customtkinter.CTkButton(root,text='Browse Script',command=read)
inp_btn.pack(pady=10)

# Generate Button
generate = customtkinter.CTkButton(root,text='Generate',command=work)
generate.pack(pady=10)

# Status Label
status_label = customtkinter.CTkLabel(root,text="")
status_label.pack(padx=10, pady=10)

# Preview Button
preview = customtkinter.CTkButton(root,text='Preview',command = prev)
preview.pack(pady=25)

# Output Label
disp_label = customtkinter.CTkLabel(root,text="")
disp_label.pack(padx=10, pady=10)

root.mainloop()