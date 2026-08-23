import tkinter as tk
import math
import subprocess
import sys
from pathlib import Path
# BASIC CALCULATOR - caly.py
root = tk.Tk()
root.title("Basic Calculator")
root.geometry("430x650")
root.resizable(False, False)
root.configure(bg="#202124")
DISPLAY_BG = "#1E1E1E"
BUTTON_BG = "#3C4043"
OPERATOR_BG = "#8AB4F8"
TEXT = "#0F0808"
display = tk.Entry(
    root,
    font=("Segoe UI", 30, "bold"),
    bg=DISPLAY_BG,
    fg=TEXT,
    justify="right",
    relief="solid",
    bd=2,
    state="readonly"
)
display.pack(fill="x", padx=12, pady=15, ipady=15)
def get_display():
    return display.get()
def set_display(value):
    display.config(state="normal")
    display.delete(0, tk.END)
    display.insert(0, value)
    display.config(state="readonly")
def add(value):
    set_display(get_display() + value)
def clear():
    set_display("")
def backspace():
    set_display(get_display()[:-1])
def calculate():
    try:
        expression = get_display()
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")
        result = eval(expression, {"__builtins__": {}})
        set_display(str(result))
    except Exception:
        set_display("Error")
def button_click(value):
    if value == "C":
        clear()
    elif value == "⌫":
        backspace()
    elif value == "=":
        calculate()
    else:
        add(value)
# BASIC BUTTONS
buttons = [
    ["C", "⌫", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
    ["=", "", "", ""]
]
for row in buttons:
    frame = tk.Frame(root, bg="#202124")
    frame.pack(fill="both", expand=True)
    for value in row:
        if value == "":
            tk.Label(frame, text="", bg="#202124").pack(
                side="left", fill="both", expand=True,
                padx=4, pady=4
            )
            continue
        bg = OPERATOR_BG if value in ["+", "-", "×", "÷", "^"] else BUTTON_BG
        fg = "#101010" if bg == OPERATOR_BG else TEXT
        if value == "=":
            bg = "#34A853"
            fg = TEXT
        button = tk.Button(
            frame,
            text=value,
            font=("Segoe UI", 17, "bold"),
            bg=bg,
            fg=fg,
            activebackground="#70757A",
            activeforeground=TEXT,
            relief="flat",
            command=lambda v=value: button_click(v)
        )
        button.pack(
            side="left",
            fill="both",
            expand=True,
            padx=4,
            pady=4
        )
# OPEN ADVANCED CALCULATOR
def open_advanced_calculator():
    # advanced_calculator.py must be in the SAME folder as caly.py
    advanced_file = Path(__file__).resolve().parent / "Advance_Calculator.py"
    if not advanced_file.is_file():
        print("ERROR: Advanced Calculator file not found.")
        print("Expected:", advanced_file)
        set_display("File Missing")
        return
    try:
        subprocess.Popen(
            [sys.executable, str(advanced_file)],
            cwd=str(advanced_file.parent)
        )
    except Exception as error:
        print("Could not open Advanced Calculator:", error)
        set_display("Error")
advanced_button = tk.Button(
    root,
    text="ADVANCED CALCULATOR",
    font=("Segoe UI", 14, "bold"),
    bg="#8AB4F8",
    fg="#101010",
    activebackground="#669DF6",
    activeforeground="#101010",
    relief="flat",
    command=open_advanced_calculator
)
advanced_button.pack(
    fill="x",
    padx=12,
    pady=12,
    ipady=7
)
# BASIC KEYBOARD CONTROL
def keyboard_control(event):
    key = event.keysym
    char = event.char
    if char in "0123456789":
        add(char)
        return "break"
    if char == ".":
        add(".")
        return "break"
    if char == "+":
        add("+")
        return "break"
    if char == "-":
        add("-")
        return "break"
    if char == "*":
        add("×")
        return "break"
    if char == "/":
        add("÷")
        return "break"
    if char == "^":
        add("^")
        return "break"
    if char in "()":
        add(char)
        return "break"
    if key in ("Return", "KP_Enter"):
        calculate()
        return "break"
    if key == "BackSpace":
        backspace()
        return "break"
    if key == "Escape":
        clear()
        return "break"
    return "break"
root.bind("<KeyPress>", keyboard_control)
root.mainloop()
