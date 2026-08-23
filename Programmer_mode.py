import tkinter as tk
from tkinter import messagebox

class ProgrammerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Programmer Calculator")
        self.root.geometry("760x650")
        self.root.minsize(700, 600)
        self.mode = "DEC"
        self.current_value = "0"
        self.first_value = None
        self.operator = None
        self.setup_colors()
        self.create_interface()

# COLORS
    def setup_colors(self):
        self.colors = {
            "BG": "#202124",
            "DISPLAY": "#303134",
            "NUMBER": "#3C4043",
            "FUNCTION": "#5F6368",
            "OPERATOR": "#3C78D8",
            "EQUAL": "#34A853",
            "TEXT": "#FFFFFF",
            "MUTED": "#BDC1C6",
            "BORDER": "#5F6368",
            "HOVER": "#4A4C50",
        }

# INTERFACE
    def create_interface(self):

# Main container
        self.main_frame = tk.Frame(
            self.root,
            bg=self.colors["BG"]
        )
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )
# HEADER
        header = tk.Frame(
            self.main_frame,
            bg=self.colors["BG"]
        )
        header.pack(fill="x", pady=(0, 10))
        title = tk.Label(
            header,
            text="PROGRAMMER CALCULATOR",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["BG"],
            fg=self.colors["TEXT"]
        )
        title.pack(side="left")
        self.mode_label = tk.Label(
            header,
            text="DEC",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["OPERATOR"],
            fg="white",
            padx=12,
            pady=5
        )
        self.mode_label.pack(side="right")

# DISPLAY
        display_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["DISPLAY"],
            bd=1,
            relief="solid"
        )
        display_frame.pack(
            fill="x",
            pady=(0, 12)
        )
        self.display = tk.Entry(
            display_frame,
            font=("Consolas", 30, "bold"),
            justify="right",
            bg=self.colors["DISPLAY"],
            fg=self.colors["TEXT"],
            insertbackground=self.colors["TEXT"],
            relief="flat",
            bd=0
        )
        self.display.pack(
            fill="x",
            padx=15,
            pady=(15, 8),
            ipady=8
        )
        self.display.insert(0, "0")
        self.status_label = tk.Label(
            display_frame,
            text="Ready",
            font=("Segoe UI", 10),
            anchor="e",
            bg=self.colors["DISPLAY"],
            fg=self.colors["MUTED"]
        )
        self.status_label.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )
# BASE CONVERSION PANEL
        conversion_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["BG"]
        )
        conversion_frame.pack(
            fill="x",
            pady=(0, 12)
        )
        self.dec_label = self.create_value_label(
            conversion_frame,
            "DEC"
        )
        self.bin_label = self.create_value_label(
            conversion_frame,
            "BIN"
        )
        self.oct_label = self.create_value_label(
            conversion_frame,
            "OCT"
        )
        self.hex_label = self.create_value_label(
            conversion_frame,
            "HEX"
        )
# MODE BUTTONS
        mode_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["BG"]
        )
        mode_frame.pack(
            fill="x",
            pady=(0, 12)
        )
        for mode in ["DEC", "BIN", "OCT", "HEX"]:
            button = tk.Button(
                mode_frame,
                text=mode,
                font=("Segoe UI", 11, "bold"),
                bg=self.colors["OPERATOR"],
                fg="white",
                activebackground=self.colors["HOVER"],
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda m=mode: self.change_mode(m)
            )
            button.pack(
                side="left",
                fill="x",
                expand=True,
                padx=3
            )
# BUTTON AREA
        self.button_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["BG"]
        )
        self.button_frame.pack(
            fill="both",
            expand=True
        )
        self.create_buttons()

# Keyboard support
        self.root.bind("<Key>", self.keyboard_input)
        self.update_conversion()

# VALUE LABEL
    def create_value_label(self, parent, title):
        frame = tk.Frame(
            parent,
            bg=self.colors["DISPLAY"],
            bd=1,
            relief="solid"
        )
        frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=3
        )
        label = tk.Label(
            frame,
            text=f"{title}\n0",
            font=("Consolas", 10, "bold"),
            bg=self.colors["DISPLAY"],
            fg=self.colors["TEXT"],
            justify="left",
            anchor="w"
        )
        label.pack(
            fill="both",
            padx=8,
            pady=6
        )
        return label

# BUTTONS
    def create_buttons(self):
        buttons = [
            ["MC", "MR", "AND", "OR", "XOR", "NOT"],
            ["7", "8", "9", "HEX", "<<", ">>"],
            ["4", "5", "6", "OCT", "(", ")"],
            ["1", "2", "3", "BIN", "+", "-"],
            ["0", "A", "B", "C", "×", "÷"],
            ["D", "E", "F", "CLR", "⌫", "="],
        ]
        for row_index, row in enumerate(buttons):
            self.button_frame.rowconfigure(
                row_index,
                weight=1
            )
            for column_index, value in enumerate(row):
                self.button_frame.columnconfigure(
                    column_index,
                    weight=1
                )
                if value == "=":
                    bg = self.colors["EQUAL"]
                elif value in [
                    "+",
                    "-",
                    "×",
                    "÷",
                    "AND",
                    "OR",
                    "XOR",
                    "<<",
                    ">>"
                ]:
                    bg = self.colors["OPERATOR"]
                elif value in [
                    "CLR",
                    "⌫",
                    "MC",
                    "MR",
                    "NOT"
                ]:
                    bg = self.colors["FUNCTION"]
                else:
                    bg = self.colors["NUMBER"]
                button = tk.Button(
                    self.button_frame,
                    text=value,
                    font=("Segoe UI", 13, "bold"),
                    bg=bg,
                    fg=self.colors["TEXT"],
                    activebackground=self.colors["HOVER"],
                    activeforeground=self.colors["TEXT"],
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda v=value: self.button_click(v)
                )
                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )
# BUTTON HANDLER
    def button_click(self, value):
        if value == "CLR":
            self.clear()
            return
        if value == "⌫":
            self.backspace()
            return
        if value == "=":
            self.calculate()
            return
        if value in ["+", "-", "×", "÷", "AND", "OR", "XOR", "<<", ">>"]:
            self.set_operator(value)
            return
        if value == "NOT":
            self.bitwise_not()
            return
        if value in ["MC", "MR"]:
            self.status_label.config(
                text=f"{value} is reserved for future memory support."
            )
            return
        if value in ["BIN", "OCT", "HEX"]:
            self.change_mode(value)
            return
        self.insert_value(value)

# MODE
    def change_mode(self, mode):
        try:
            current = self.get_current_integer()
            self.mode = mode
            self.mode_label.config(text=mode)
            self.set_display(
                self.convert_from_decimal(current, mode)
            )
            self.status_label.config(
                text=f"Programmer mode: {mode}"
            )
            self.update_conversion()
        except ValueError:
            messagebox.showerror(
                "Invalid Value",
                f"The current value cannot be converted to {mode}."
            )
# INSERT VALUE
    def insert_value(self, value):
        allowed = {
            "DEC": "0123456789",
            "BIN": "01",
            "OCT": "01234567",
            "HEX": "0123456789ABCDEF"
        }
        if value not in allowed[self.mode]:
            self.status_label.config(
                text=f"{value} is not valid in {self.mode} mode."
            )
            return
        current = self.display.get()
        if current == "0":
            current = ""
        self.set_display(current + value)
        self.update_conversion()
# DISPLAY
    def set_display(self, value):
        self.display.delete(0, tk.END)
        self.display.insert(0, str(value))
    def get_display(self):
        return self.display.get()
# CLEAR
    def clear(self):
        self.set_display("0")
        self.first_value = None
        self.operator = None
        self.status_label.config(
            text="Cleared"
        )
        self.update_conversion()

# BACKSPACE
    def backspace(self):
        value = self.get_display()
        if len(value) <= 1:
            self.set_display("0")
        else:
            self.set_display(value[:-1])
        self.update_conversion()

# CONVERSION
    def get_current_integer(self):
        value = self.get_display().strip().upper()
        if not value:
            return 0
        base = {
            "DEC": 10,
            "BIN": 2,
            "OCT": 8,
            "HEX": 16
        }[self.mode]
        return int(value, base)
    def convert_from_decimal(self, value, mode):
        if mode == "DEC":
            return str(value)
        if mode == "BIN":
            return bin(value)[2:].upper()
        if mode == "OCT":
            return oct(value)[2:].upper()
        if mode == "HEX":
            return hex(value)[2:].upper()
        return str(value)
    def update_conversion(self):
        try:
            decimal = self.get_current_integer()
            self.dec_label.config(
                text=f"DEC\n{decimal}"
            )
            self.bin_label.config(
                text=f"BIN\n{self.convert_from_decimal(decimal, 'BIN')}"
            )
            self.oct_label.config(
                text=f"OCT\n{self.convert_from_decimal(decimal, 'OCT')}"
            )
            self.hex_label.config(
                text=f"HEX\n{self.convert_from_decimal(decimal, 'HEX')}"
            )
        except ValueError:
            self.dec_label.config(text="DEC\nInvalid")
            self.bin_label.config(text="BIN\nInvalid")
            self.oct_label.config(text="OCT\nInvalid")
            self.hex_label.config(text="HEX\nInvalid")

# OPERATORS
    def set_operator(self, operator):
        try:
            self.first_value = self.get_current_integer()
            self.operator = operator
            self.set_display("0")
            self.status_label.config(
                text=f"{self.first_value} {operator}"
            )
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid number."
            )
# CALCULATE
    def calculate(self):
        if self.first_value is None or self.operator is None:
            return
        try:
            second_value = self.get_current_integer()
            a = self.first_value
            b = second_value
            op = self.operator
            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "×":
                result = a * b
            elif op == "÷":
                if b == 0:
                    raise ZeroDivisionError
                result = a // b
            elif op == "AND":
                result = a & b
            elif op == "OR":
                result = a | b
            elif op == "XOR":
                result = a ^ b
            elif op == "<<":
                result = a << b
            elif op == ">>":
                result = a >> b
            else:
                result = 0
            self.set_display(
                self.convert_from_decimal(
                    result,
                    self.mode
                )
            )
            self.status_label.config(
                text=f"{a} {op} {b} = {result}"
            )
            self.first_value = None
            self.operator = None
            self.update_conversion()
        except ZeroDivisionError:
            messagebox.showerror(
                "Math Error",
                "Division by zero is not allowed."
            )
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Invalid number for the selected mode."
            )
        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error)
            )
# BITWISE NOT
    def bitwise_not(self):
        try:
            value = self.get_current_integer()
            result = ~value
            self.set_display(
                self.convert_from_decimal(
                    result,
                    self.mode
                )
            )
            self.status_label.config(
                text=f"NOT {value} = {result}"
            )
            self.update_conversion()
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid number."
            )
# KEYBOARD SUPPORT
    def keyboard_input(self, event):
        key = event.keysym.upper()
        if event.char:
            char = event.char.upper()
            if char in "0123456789ABCDEF":
                self.insert_value(char)
                return
            if char == "+":
                self.set_operator("+")
                return
            if char == "-":
                self.set_operator("-")
                return
            if char == "*":
                self.set_operator("×")
                return
            if char == "/":
                self.set_operator("÷")
                return
            if char == "&":
                self.set_operator("AND")
                return
            if char == "|":
                self.set_operator("OR")
                return
            if char == "^":
                self.set_operator("XOR")
                return
        if key == "RETURN":
            self.calculate()
        elif key == "BACKSPACE":
            self.backspace()
        elif key == "ESCAPE":
            self.clear()

# RUN PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    app = ProgrammerCalculator(root)
    root.mainloop()