from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess
import threading
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

window = Tk()
window.title("ViperCode - The Python IDE")
window.configure(bg='#1E1E1E')

gpath = ''

def openShell():
    def runShellCommand():
        code = shellInput.get('1.0', END).strip()
        try:
            result = subprocess.run(code, shell=True, capture_output=True, text=True)
            output = result.stdout
            error = result.stderr
            shellOutput.delete('1.0', END)
            shellOutput.insert('1.0', output + error)
        except Exception as e:
            shellOutput.delete('1.0', END)
            shellOutput.insert('1.0', str(e))

    shellWindow = Toplevel(window)
    shellWindow.title("Shell")

    shellInput = Text(shellWindow, height=10, bg='#000008', fg='white', insertbackground='white')
    shellInput.pack(expand=True, fill=BOTH)

    shellOutput = Text(shellWindow, height=10, bg='#000003', fg='white', insertbackground='white')
    shellOutput.pack(expand=True, fill=BOTH)

    runButton = Button(shellWindow, text="Run Command", command=runShellCommand, bg='#000020', fg='white')
    runButton.pack()

def runMycode():
    global gpath
    if not gpath:
        saveMsg = Toplevel()
        saveMsg.configure(bg='black')
        msg = Label(saveMsg, text="Please save file before running Debug", fg="white", bg='black')
        msg.pack()
        return
    command = f'python "{gpath}"'
    def execute_code():
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        outputResult, error = process.communicate()
        output.delete('1.0', END)
        output.insert('1.0', outputResult.decode())
        output.insert('1.0', error.decode())
    threading.Thread(target=execute_code).start()

def openMyFile():
    global gpath
    path = askopenfilename(filetypes=[('Python Files', '*.py'), ('All Files', '*.*')])
    if path:
        with open(path, 'r') as file:
            code = file.read()
            textEditor.delete('1.0', END)
            textEditor.insert('1.0', code)
            gpath = path

def saveMyFile():
    global gpath
    if not gpath:
        saveMyFileAs()
    else:
        with open(gpath, 'w') as file:
            code = textEditor.get('1.0', END)
            file.write(code)

def saveMyFileAs():
    global gpath
    path = asksaveasfilename(filetypes=[('Python Files', '*.py'), ('All Files', '*.*')], defaultextension='.py')
    if path:
        with open(path, 'w') as file:
            code = textEditor.get('1.0', END)
            file.write(code)
        gpath = path

textEditor = Text(window, bg='#000009', fg='white', insertbackground='white')
textEditor.pack(expand=True, fill=BOTH)

output = Text(window, height=10, bg='#000003', fg='white', insertbackground='white')
output.pack(expand=True, fill=BOTH)

menuBar = Menu(window)

fileBar = Menu(menuBar, tearoff=0)
fileBar.add_command(label='Open', command=openMyFile)
fileBar.add_command(label='Save', command=saveMyFile)
fileBar.add_command(label='Save As', command=saveMyFileAs)
fileBar.add_command(label='Exit', command=window.destroy)
menuBar.add_cascade(label='File', menu=fileBar)

runBar = Menu(menuBar, tearoff=0)
runBar.add_command(label='Run', command=runMycode)
menuBar.add_cascade(label='Run', menu=runBar)

shell = Menu(menuBar, tearoff=0)
shell.add_command(label='REPL', command=openShell)
menuBar.add_cascade(label='Shell', menu=shell)

textEditor.insert(END, "# Welcome!\n# Please go to file and click save every time before Running!")

window.config(menu=menuBar)
window.mainloop()
