import tkinter as tk
import math
from statistics import median
from collections import Counter
import subprocess
import sys
from pathlib import Path

# OPEN PROGRAMMER MODE
def open_programmer_mode():
    programmer_file = Path(__file__).parent / "programmer_mode.py"
    if programmer_file.exists():
        subprocess.Popen(
            [sys.executable, str(programmer_file)]
        )
    else:
        set_status("Programmer Mode file not found.")

# OPEN GRAPH MODE
def open_graph_mode():
    graph_file = Path(__file__).parent / "graph_mode.py"
    if graph_file.exists():
        subprocess.Popen(
            [sys.executable, str(graph_file)]
        )
    else:
        set_status("Graph Plotting Mode file not found.")

# ADVANCED SCIENTIFIC CALCULATOR
root = tk.Tk()
root.title("Advanced Scientific Calculator")
root.geometry("1100x720")
root.minsize(950, 650)

# THEMES
LIGHT_THEME = {
    "BG": "#FFFFFF",
    "DISPLAY_BG": "#F8F9FA",
    "NUMBER_BG": "#FFFFFF",
    "FUNCTION_BG": "#E8EAED",
    "OPERATOR_BG": "#D2E3FC",
    "EQUAL_BG": "#34A853",
    "MEMORY_BG": "#E8EAED",
    "TEXT": "#202124",
    "MUTED": "#6B7280",
    "HISTORY_BG": "#F1F3F4",
    "HISTORY_TEXT": "#202124",
    "BORDER": "#DADCE0"
}
DARK_THEME = {
    "BG": "#202124",
    "DISPLAY_BG": "#303134",
    "NUMBER_BG": "#3C4043",
    "FUNCTION_BG": "#5F6368",
    "OPERATOR_BG": "#3C78D8",
    "EQUAL_BG": "#34A853",
    "MEMORY_BG": "#4A4B4F",
    "TEXT": "#FFFFFF",
    "MUTED": "#BDC1C6",
    "HISTORY_BG": "#292A2D",
    "HISTORY_TEXT": "#FFFFFF",
    "BORDER": "#5F6368"
}
current_theme = "light"
theme = LIGHT_THEME

# Theme variables
BG = theme["BG"]
DISPLAY_BG = theme["DISPLAY_BG"]
NUMBER_BG = theme["NUMBER_BG"]
FUNCTION_BG = theme["FUNCTION_BG"]
OPERATOR_BG = theme["OPERATOR_BG"]
EQUAL_BG = theme["EQUAL_BG"]
MEMORY_BG = theme["MEMORY_BG"]
TEXT = theme["TEXT"]
MUTED = theme["MUTED"]
HISTORY_BG = theme["HISTORY_BG"]
HISTORY_TEXT = theme["HISTORY_TEXT"]
BORDER = theme["BORDER"]

# Hover colors
HOVER_NUMBER = "#E8EAED"
HOVER_FUNCTION = "#D2D3D7"
HOVER_OPERATOR = "#AECBF5"
HOVER_EQUAL = "#2D8D47"

# VARIABLES
memory = 0
last_answer = 0
angle_mode = "DEG"

# HELPER FUNCTIONS
def format_result(value):
    """Format calculator results neatly."""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return str(value)
        if value.is_integer():
            return str(int(value))
        return str(round(value, 12))
    return str(value)
def get_display():
    return display.get()
def set_display(value):
    display.config(state="normal")
    display.delete(0, tk.END)
    display.insert(0, value)
    display.config(state="readonly")
def set_status(message):
    display_status.config(text=message)

# BASIC CALCULATOR FUNCTIONS
def add(value):
    current = get_display()
    if current == "Error":
        current = ""
    set_display(current + value)
    set_status("Typing")
def clear():
    set_display("")
    set_status("Ready")
def backspace():
    current = get_display()
    if current == "Error":
        set_display("")
    else:
        set_display(current[:-1])
    set_status("Editing")

# COPY RESULT
def copy_result():
    try:
        result = get_display()
        if not result:
            set_status("Nothing to copy")
            return
        root.clipboard_clear()
        root.clipboard_append(result)
        root.update()
        set_status("Result copied to clipboard")
    except Exception:
        set_status("Error copying result")

# BUTTON COLORS
def get_button_color(value):
    if value == "=":
        return EQUAL_BG
    if value in [
        "+", "-", "×", "÷", "^", "%"
    ]:
        return OPERATOR_BG
    if value in [
        "MC", "MR", "M+", "M−", "DEG", "RAD"
    ]:
        return MEMORY_BG
    if value in [
        "STAT",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "log",
        "ln",
        "√",
        "x²",
        "x³",
        "x!",
        "1/x"
    ]:
        return FUNCTION_BG
    return NUMBER_BG
def get_hover_color(value):
    if value == "=":
        return HOVER_EQUAL
    if value in [
        "+", "-", "×", "÷", "^", "%"
    ]:
        return HOVER_OPERATOR
    return HOVER_FUNCTION

# MAIN SCROLLABLE LAYOUT
root.configure(bg=BG)
main_container = tk.Frame(
    root,
    bg=BG
)
main_container.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)
# Canvas
main_canvas = tk.Canvas(
    main_container,
    bg=BG,
    highlightthickness=0,
    bd=0
)
main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)
# Scrollbar
main_scrollbar = tk.Scrollbar(
    main_container,
    orient="vertical",
    command=main_canvas.yview
)
main_scrollbar.pack(
    side="right",
    fill="y"
)
main_canvas.configure(
    yscrollcommand=main_scrollbar.set
)
# Frame inside canvas
main_frame = tk.Frame(
    main_canvas,
    bg=BG
)
main_window = main_canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)
# UPDATE MAIN SCROLL REGION
def update_main_scroll_region(event=None):
    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
main_frame.bind(
    "<Configure>",
    update_main_scroll_region
)
# MAIN FRAME WIDTH MATCHES CANVAS
def update_main_width(event):
    main_canvas.itemconfigure(
        main_window,
        width=event.width
    )
main_canvas.bind(
    "<Configure>",
    update_main_width
)
# CALCULATOR AND HISTORY FRAMES
calculator_frame = tk.Frame(
    main_frame,
    bg=BG
)
calculator_frame.pack(
    side="left",
    fill="both",
    expand=True
)
history_frame = tk.Frame(
    main_frame,
    bg=HISTORY_BG,
    width=300
)
history_frame.pack(
    side="right",
    fill="y",
    padx=(15, 0)
)
history_frame.pack_propagate(False)

# MAIN PAGE KEYBOARD SCROLLING
def scroll_page_down(event=None):
    main_canvas.yview_scroll(
        1,
        "units"
    )
    return "break"
def scroll_page_up(event=None):
    main_canvas.yview_scroll(
        -1,
        "units"
    )
    return "break"
def scroll_page_down_screen(event=None):
    main_canvas.yview_scroll(
        1,
        "pages"
    )
    return "break"
def scroll_page_up_screen(event=None):
    main_canvas.yview_scroll(
        -1,
        "pages"
    )
    return "break"
def scroll_page_top(event=None):
    main_canvas.yview_moveto(0)
    return "break"
def scroll_page_bottom(event=None):
    main_canvas.yview_moveto(1)
    return "break"
root.bind(
    "<Control-Down>",
    scroll_page_down
)
root.bind(
    "<Control-Up>",
    scroll_page_up
)
root.bind(
    "<Control-Next>",
    scroll_page_down_screen
)
root.bind(
    "<Control-Prior>",
    scroll_page_up_screen
)
root.bind(
    "<Control-Home>",
    scroll_page_top
)
root.bind(
    "<Control-End>",
    scroll_page_bottom
)
# MAIN PAGE MOUSE WHEEL
def mousewheel_scroll(event):
    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )
    return "break"
root.bind(
    "<MouseWheel>",
    mousewheel_scroll
)
# HEADER
header_frame = tk.Frame(
    calculator_frame,
    bg=BG
)
header_frame.pack(
    fill="x",
    pady=(0, 8)
)
header_title = tk.Label(
    header_frame,
    text="Scientific Calculator",
    font=("Segoe UI", 20, "bold"),
    bg=BG,
    fg=TEXT
)
header_title.pack(
    side="left"
)
header_status = tk.Label(
    header_frame,
    text="Keyboard Enabled",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
)
header_status.pack(
    side="right",
    padx=10
)
# DISPLAY CARD
display_card = tk.Frame(
    calculator_frame,
    bg=DISPLAY_BG,
    highlightbackground=BORDER,
    highlightthickness=1
)
display_card.pack(
    fill="x",
    pady=(0, 5)
)
tk.Label(
    display_card,
    text="EXPRESSION",
    font=("Segoe UI", 8, "bold"),
    bg=DISPLAY_BG,
    fg=MUTED
).pack(
    anchor="w",
    padx=14,
    pady=(8, 0)
)
display = tk.Entry(
    display_card,
    font=("Segoe UI", 30, "bold"),
    bg=DISPLAY_BG,
    fg=TEXT,
    insertbackground=TEXT,
    justify="right",
    relief="flat",
    bd=0,
    state="readonly"
)
display.pack(
    fill="x",
    padx=14,
    pady=(0, 2),
    ipady=8
)
display_status = tk.Label(
    display_card,
    text="Ready",
    font=("Segoe UI", 9),
    bg=DISPLAY_BG,
    fg=MUTED
)
display_status.pack(
    anchor="e",
    padx=14,
    pady=(0, 7)
)
# DEG / RAD
mode_label = tk.Label(
    calculator_frame,
    text="DEG",
    font=("Segoe UI", 12, "bold"),
    bg=BG,
    fg="#1A73E8"
)
mode_label.pack(
    anchor="e"
)
def set_degree():
    global angle_mode
    angle_mode = "DEG"
    mode_label.config(
        text="DEG"
    )
    set_status("Degree mode")
def set_radian():
    global angle_mode
    angle_mode = "RAD"
    mode_label.config(
        text="RAD"
    )
    set_status("Radian mode")

# MEMORY DISPLAY
memory_label = tk.Label(
    calculator_frame,
    text="Memory: 0",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
)
memory_label.pack(
    anchor="w"
)
# SCIENTIFIC FUNCTIONS
def scientific(function):
    try:
        value = float(get_display())
        if function == "sin":
            result = math.sin(
                math.radians(value)
                if angle_mode == "DEG"
                else value
            )
        elif function == "cos":
            result = math.cos(
                math.radians(value)
                if angle_mode == "DEG"
                else value
            )
        elif function == "tan":
            result = math.tan(
                math.radians(value)
                if angle_mode == "DEG"
                else value
            )
        elif function == "asin":
            result = math.asin(value)
            if angle_mode == "DEG":
                result = math.degrees(result)
        elif function == "acos":
            result = math.acos(value)
            if angle_mode == "DEG":
                result = math.degrees(result)
        elif function == "atan":
            result = math.atan(value)
            if angle_mode == "DEG":
                result = math.degrees(result)
        elif function == "log":
            result = math.log10(value)
        elif function == "ln":
            result = math.log(value)
        elif function == "sqrt":
            result = math.sqrt(value)
        elif function == "square":
            result = value ** 2
        elif function == "cube":
            result = value ** 3
        elif function == "factorial":
            if value < 0 or not value.is_integer():
                raise ValueError
            result = math.factorial(int(value))
        elif function == "inverse":
            result = 1 / value
        else:
            raise ValueError
        result_text = format_result(result)
        set_display(result_text)
        set_status(
            f"{function} calculated"
        )
    except Exception:
        set_display("Error")
        set_status(
            "Invalid value"
        )
# CALCULATE
def calculate():
    global last_answer
    try:
        expression = get_display()
        if not expression:
            return
        original_expression = expression
        expression = expression.replace(
            "×",
            "*"
        )
        expression = expression.replace(
            "÷",
            "/"
        )
        expression = expression.replace(
            "^",
            "**"
        )
        expression = expression.replace(
            "%",
            "/100"
        )
        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            {
                "pi": math.pi,
                "e": math.e
            }
        )
        last_answer = result
        result_text = format_result(result)
        history_box.insert(
            tk.END,
            f"{original_expression} = {result_text}"
        )
        history_box.see(
            tk.END
        )
        set_display(
            result_text
        )
        set_status(
            "Calculation complete"
        )
    except Exception:
        set_display("Error")
        set_status(
            "Invalid expression"
        )
# NUMERIC VALUE
def numeric_value():
    try:
        expression = get_display()
        if not expression:
            return None
        expression = expression.replace(
            "×",
            "*"
        )
        expression = expression.replace(
            "÷",
            "/"
        )
        expression = expression.replace(
            "^",
            "**"
        )
        expression = expression.replace(
            "%",
            "/100"
        )
        result = eval(
            expression,
            {
                "__builtins__": {}
            },
            {
                "pi": math.pi,
                "e": math.e
            }
        )
        return float(result)
    except Exception:
        return None

# MEMORY FUNCTIONS
def memory_clear():
    global memory
    memory = 0
    memory_label.config(
        text="Memory: 0"
    )
    set_status(
        "Memory cleared"
    )
def memory_recall():
    set_display(
        format_result(memory)
    )
    set_status(
        "Memory recalled"
    )
def memory_add():
    global memory
    value = numeric_value()
    if value is not None:
        memory += value
        memory_label.config(
            text=f"Memory: {format_result(memory)}"
        )
        set_status(
            "Memory added"
        )
    else:
        set_status(
            "Invalid memory value"
        )
def memory_subtract():
    global memory
    value = numeric_value()
    if value is not None:
        memory -= value
        memory_label.config(
            text=f"Memory: {format_result(memory)}"
        )
        set_status(
            "Memory subtracted"
        )
    else:
        set_status(
            "Invalid memory value"
        )
def insert_answer():
    set_display(
        format_result(last_answer)
    )
    set_status(
        "Previous answer inserted"
    )
# STATISTICS MODE
def statistics_mode():
    stats_window = tk.Toplevel(root)
    stats_window.title(
        "Statistics Mode"
    )
    stats_window.geometry(
        "700x720"
    )
    stats_window.minsize(
        650,
        650
    )
    stats_window.configure(
        bg=BG
    )
    stats_window.transient(root)

# HEADER
    tk.Label(
        stats_window,
        text="📊 Statistics Mode",
        font=("Segoe UI", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=25,
        pady=(20, 3)
    )
    tk.Label(
        stats_window,
        text="Population statistics calculator",
        font=("Segoe UI", 10),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=25,
        pady=(0, 15)
    )
# INPUT CARD
    input_card = tk.Frame(
        stats_window,
        bg=DISPLAY_BG,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    input_card.pack(
        fill="x",
        padx=25,
        pady=(0, 15)
    )
    tk.Label(
        input_card,
        text="ENTER DATA",
        font=("Segoe UI", 9, "bold"),
        bg=DISPLAY_BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 5)
    )
    tk.Label(
        input_card,
        text="Numbers separated by commas",
        font=("Segoe UI", 10),
        bg=DISPLAY_BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=15
    )
    data_entry = tk.Entry(
        input_card,
        font=("Segoe UI", 15),
        bg=BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        bd=0
    )
    data_entry.pack(
        fill="x",
        padx=15,
        pady=(8, 5),
        ipady=8
    )
    tk.Label(
        input_card,
        text="Example: 10, 20, 20, 30, 40",
        font=("Segoe UI", 9),
        bg=DISPLAY_BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=15,
        pady=(0, 12)
    )
# RESULT CARD
    result_card = tk.Frame(
        stats_window,
        bg=DISPLAY_BG,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    result_card.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 15)
    )
    tk.Label(
        result_card,
        text="RESULTS",
        font=("Segoe UI", 9, "bold"),
        bg=DISPLAY_BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 5)
    )
    result_box = tk.Text(
        result_card,
        font=("Consolas", 11),
        bg=DISPLAY_BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        bd=0,
        wrap="word",
        state="disabled"
    )
    result_box.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )
# RESULT DISPLAY
    def show_result(text):
        result_box.config(
            state="normal"
        )
        result_box.delete(
            "1.0",
            tk.END
        )
        result_box.insert(
            "1.0",
            text
        )
        result_box.config(
            state="disabled"
        )
# CALCULATE STATISTICS
    def calculate_statistics():
        try:
            text = data_entry.get().strip()
            if not text:
                raise ValueError(
                    "Please enter some numbers."
                )
            values = []
            for item in text.split(","):
                item = item.strip()
                if not item:
                    continue
                try:
                    values.append(
                        float(item)
                    )
                except ValueError:
                    raise ValueError(
                        f"Invalid number: {item}"
                    )
            if not values:
                raise ValueError(
                    "No valid numbers found."
                )
# Basic statistics
            count = len(values)
            total = sum(values)
            mean = total / count
            median_value = median(values)
# Mode
            frequency = Counter(values)
            highest_frequency = max(
                frequency.values()
            )
            if highest_frequency == 1:
                mode_text = "No mode"
            else:
                modes = [
                    value
                    for value, freq in frequency.items()
                    if freq == highest_frequency
                ]
                modes.sort()
                mode_text = ", ".join(
                    format_result(value)
                    for value in modes
                )
# Minimum / Maximum
            minimum = min(values)
            maximum = max(values)
# Range
            data_range = maximum - minimum
# Population variance
            population_variance = sum(
                (x - mean) ** 2
                for x in values
            ) / count

 # Population standard deviation
            population_standard_deviation = math.sqrt(
                population_variance
            )
# Result
            result = (
                "STATISTICS RESULTS\n"
                "========================================\n\n"
                f"Data:\n"
                f"    {', '.join(format_result(x) for x in values)}\n\n"
                f"Count (N):\n"
                f"    {count}\n\n"
                f"Sum:\n"
                f"    {format_result(total)}\n\n"
                f"Mean:\n"
                f"    {format_result(mean)}\n\n"
                f"Median:\n"
                f"    {format_result(median_value)}\n\n"
                f"Mode:\n"
                f"    {mode_text}\n\n"
                f"Minimum:\n"
                f"    {format_result(minimum)}\n\n"
                f"Maximum:\n"
                f"    {format_result(maximum)}\n\n"
                f"Range:\n"
                f"    {format_result(data_range)}\n\n"
                f"Population Variance:\n"
                f"    {format_result(population_variance)}\n\n"
                f"Population Standard Deviation:\n"
                f"    {format_result(population_standard_deviation)}"
            )
            show_result(result)
# Add to history
            history_box.insert(
                tk.END,
                (
                    f"STAT: Mean={format_result(mean)}, "
                    f"Median={format_result(median_value)}, "
                    f"Mode={mode_text}, "
                    f"Population SD="
                    f"{format_result(population_standard_deviation)}"
                )
            )
            history_box.see(
                tk.END
            )
            set_status(
                "Statistics calculated"
            )
        except ValueError as error:
            show_result(
                "INVALID DATA\n"
                "========================================\n\n"
                f"{error}\n\n"
                "Please enter valid numbers separated by commas.\n\n"
                "Example:\n"
                "10, 20, 20, 30, 40"
            )
        except Exception as error:
            show_result(
                "CALCULATION ERROR\n"
                "========================================\n\n"
                f"{error}"
            )
# CLEAR STATISTICS
    def clear_statistics():
        data_entry.delete(
            0,
            tk.END
        )
        show_result("")
        data_entry.focus_set()

# BUTTONS
    stats_buttons = tk.Frame(
        stats_window,
        bg=BG
    )
    stats_buttons.pack(
        fill="x",
        padx=25,
        pady=(0, 10)
    )
    calculate_button = tk.Button(
        stats_buttons,
        text="Calculate",
        font=("Segoe UI", 11, "bold"),
        bg=EQUAL_BG,
        fg="white",
        activebackground=HOVER_EQUAL,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=calculate_statistics
    )
    calculate_button.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 5),
        ipady=8
    )
    clear_button = tk.Button(
        stats_buttons,
        text="Clear",
        font=("Segoe UI", 11, "bold"),
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=clear_statistics
    )
    clear_button.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(5, 0),
        ipady=8
    )
    close_button = tk.Button(
        stats_window,
        text="Close",
        font=("Segoe UI", 10, "bold"),
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=stats_window.destroy
    )
    close_button.pack(
        pady=(0, 15),
        ipadx=30,
        ipady=5
    )
# STATISTICS KEYBOARD SUPPORT
    def statistics_keyboard(event):
        if event.keysym in [
            "Return",
            "KP_Enter"
        ]:
            calculate_statistics()
            return "break"
        elif event.keysym == "Escape":
            clear_statistics()
            return "break"
    data_entry.bind(
        "<Return>",
        statistics_keyboard
    )
    data_entry.bind(
        "<KP_Enter>",
        statistics_keyboard
    )
    data_entry.bind(
        "<Escape>",
        statistics_keyboard
    )
    data_entry.focus_set()

# BUTTON ACTIONS
def button_click(value):
    actions = {
        "C": clear,
        "STAT": statistics_mode,
        "⌫": backspace,
        "=": calculate,
        "MC": memory_clear,
        "MR": memory_recall,
        "M+": memory_add,
        "M−": memory_subtract,
        "DEG": set_degree,
        "RAD": set_radian,
        "Ans": insert_answer,
        "sin": lambda: scientific("sin"),
        "cos": lambda: scientific("cos"),
        "tan": lambda: scientific("tan"),
        "asin": lambda: scientific("asin"),
        "acos": lambda: scientific("acos"),
        "atan": lambda: scientific("atan"),
        "log": lambda: scientific("log"),
        "ln": lambda: scientific("ln"),
        "√": lambda: scientific("sqrt"),
        "x²": lambda: scientific("square"),
        "x³": lambda: scientific("cube"),
        "x!": lambda: scientific("factorial"),
        "1/x": lambda: scientific("inverse"),
        "π": lambda: add("pi"),
        "e": lambda: add("e")
    }
    if value in actions:
        actions[value]()
    else:
        add(value)

# BUTTON LIST
buttons = [
    ["MC", "MR", "M+", "M−", "DEG", "RAD"],
    ["STAT", "sin", "cos", "tan", "asin", "acos"],
    ["log", "ln", "√", "x²", "x³", "x!"],
    ["1/x", "π", "e", "Ans", "(", ")"],
    ["7", "8", "9", "÷", "%", "C"],
    ["4", "5", "6", "×", "^", "⌫"],
    ["1", "2", "3", "-", ".", "="],
    ["0", "+", "", "", "", ""]
]
# BUTTON AREA
button_area = tk.Frame(
    calculator_frame,
    bg=BG
)
button_area.pack(
    fill="both",
    expand=True
)
calculator_buttons = []

# CREATE BUTTONS
for row in buttons:
    row_frame = tk.Frame(
        button_area,
        bg=BG
    )
    row_frame.pack(
        fill="both",
        expand=True
    )
    for value in row:
        if value == "":
            tk.Label(
                row_frame,
                text="",
                bg=BG
            ).pack(
                side="left",
                fill="both",
                expand=True,
                padx=3,
                pady=3
            )
            continue
        button = tk.Button(
            row_frame,
            text=value,
            font=("Segoe UI", 12, "bold"),
            bg=get_button_color(value),
            fg=TEXT,
            activebackground=get_button_color(value),
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda v=value: button_click(v)
        )
        button.pack(
            side="left",
            fill="both",
            expand=True,
            padx=3,
            pady=3
        )
        calculator_buttons.append(
            button
        )
 # Hover
        button.bind(
            "<Enter>",
            lambda event, b=button, v=value:
            b.config(
                bg=get_hover_color(v)
            )
        )
        button.bind(
            "<Leave>",
            lambda event, b=button, v=value:
            b.config(
                bg=get_button_color(v)
            )
        )
# HISTORY
history_title = tk.Label(
    history_frame,
    text="Calculation History",
    font=("Segoe UI", 16, "bold"),
    bg=HISTORY_BG,
    fg=TEXT
)
history_title.pack(
    pady=15
)
history_box = tk.Listbox(
    history_frame,
    font=("Consolas", 11),
    bg=HISTORY_BG,
    fg=HISTORY_TEXT,
    selectbackground=OPERATOR_BG,
    selectforeground=TEXT,
    relief="flat"
)
history_box.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)
# HISTORY PANEL SCROLLING
def history_mousewheel(event):
    history_box.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )
    return "break"
def history_scroll_up(event):
    history_box.yview_scroll(
        -1,
        "units"
    )
    return "break"
def history_scroll_down(event):
    history_box.yview_scroll(
        1,
        "units"
    )
    return "break"
def history_page_up(event):
    history_box.yview_scroll(
        -1,
        "pages"
    )
    return "break"
def history_page_down(event):
    history_box.yview_scroll(
        1,
        "pages"
    )
    return "break"
def history_top(event):
    history_box.yview_moveto(
        0
    )
    return "break"
def history_bottom(event):
    history_box.yview_moveto(
        1
    )
    return "break"
history_box.bind(
    "<MouseWheel>",
    history_mousewheel
)
history_box.bind(
    "<Up>",
    history_scroll_up
)
history_box.bind(
    "<Down>",
    history_scroll_down
)
history_box.bind(
    "<Prior>",
    history_page_up
)
history_box.bind(
    "<Next>",
    history_page_down
)
history_box.bind(
    "<Control-Home>",
    history_top
)
history_box.bind(
    "<Control-End>",
    history_bottom
)
# HISTORY DOUBLE CLICK
def history_double_click(event):
    selection = history_box.curselection()
    if not selection:
        return
    item = history_box.get(
        selection[0]
    )
    if "=" in item:
        result = item.split(
            "="
        )[-1].strip()
        set_display(
            result
        )
        set_status(
            "History result loaded"
        )
history_box.bind(
    "<Double-Button-1>",
    history_double_click
)
# CLEAR HISTORY
def clear_history():
    history_box.delete(
        0,
        tk.END
    )
    set_status(
        "History cleared"
    )
clear_history_button = tk.Button(
    history_frame,
    text="Clear History",
    font=("Segoe UI", 11, "bold"),
    bg=FUNCTION_BG,
    fg=TEXT,
    activebackground=HOVER_FUNCTION,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=clear_history
)
clear_history_button.pack(
    fill="x",
    padx=10,
    pady=10
)
# KEYBOARD SHORTCUTS WINDOW
def show_keyboard_shortcuts():
    shortcuts_window = tk.Toplevel(root)
    shortcuts_window.title(
        "Keyboard Shortcuts"
    )
    shortcuts_window.geometry(
        "540x680"
    )
    shortcuts_window.resizable(
        False,
        False
    )
    shortcuts_window.configure(
        bg=BG
    )
    shortcuts_window.transient(root)

# HEADER
    tk.Label(
        shortcuts_window,
        text="⌨ Keyboard Shortcuts",
        font=("Segoe UI", 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=25,
        pady=(20, 5)
    )
    tk.Label(
        shortcuts_window,
        text="Keyboard controls for the calculator",
        font=("Segoe UI", 10),
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=25,
        pady=(0, 15)
    )
 # SCROLLABLE SHORTCUT AREA
    scroll_container = tk.Frame(
        shortcuts_window,
        bg=BG
    )
    scroll_container.pack(
        fill="both",
        expand=True,
        padx=25
    )
    shortcut_canvas = tk.Canvas(
        scroll_container,
        bg=BG,
        highlightthickness=0,
        bd=0
    )
    shortcut_scrollbar = tk.Scrollbar(
        scroll_container,
        orient="vertical",
        command=shortcut_canvas.yview
    )
    shortcut_frame = tk.Frame(
        shortcut_canvas,
        bg=BG
    )
 # Update scroll region
    shortcut_frame.bind(
        "<Configure>",
        lambda event: shortcut_canvas.configure(
            scrollregion=shortcut_canvas.bbox("all")
        )
    )
 # Put frame inside canvas
    shortcut_window = shortcut_canvas.create_window(
        (0, 0),
        window=shortcut_frame,
        anchor="nw"
    )
 # Connect scrollbar
    shortcut_canvas.configure(
        yscrollcommand=shortcut_scrollbar.set
    )
# Make inner frame match canvas width
    def update_shortcut_width(event):
        shortcut_canvas.itemconfigure(
            shortcut_window,
            width=event.width
        )
    shortcut_canvas.bind(
        "<Configure>",
        update_shortcut_width
    )
    shortcut_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )
    shortcut_scrollbar.pack(
        side="right",
        fill="y"
    )
# SHORTCUT LIST
    shortcuts = [
        ("0 – 9", "Numbers"),
        (".", "Decimal point"),
        ("+  -  *  /", "Basic operators"),
        ("^", "Power"),
        ("(", "Open bracket"),
        (")", "Close bracket"),
        ("Enter", "Calculate"),
        ("Backspace", "Delete"),
        ("Esc", "Clear"),
        ("S", "Sin"),
        ("C", "Cos"),
        ("T", "Tan"),
        ("L", "Log"),
        ("N", "Natural log"),
        ("Q", "Square root"),
        ("Ctrl + 1", "DEG mode"),
        ("Ctrl + 2", "RAD mode"),
        ("Ctrl + 3", "Memory Clear"),
        ("Ctrl + 4", "Memory Recall"),
        ("Ctrl + 5", "Memory Add"),
        ("Ctrl + 6", "Memory Subtract"),
        ("Ctrl + 7", "Previous Answer"),
        ("F1", "DEG mode"),
        ("F2", "RAD mode"),
        ("F3", "Memory Clear"),
        ("F4", "Memory Recall"),
        ("F5", "Memory Add"),
        ("F6", "Memory Subtract"),
        ("F7", "Previous Answer")
    ]
# TABLE HEADERS
    tk.Label(
        shortcut_frame,
        text="KEY",
        font=("Segoe UI", 9, "bold"),
        bg=BG,
        fg=MUTED
    ).grid(
        row=0,
        column=0,
        padx=(10, 30),
        pady=5,
        sticky="w"
    )
    tk.Label(
        shortcut_frame,
        text="ACTION",
        font=("Segoe UI", 9, "bold"),
        bg=BG,
        fg=MUTED
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=5,
        sticky="w"
    )
# DISPLAY SHORTCUTS
    for row, (key, action) in enumerate(
        shortcuts,
        start=1
    ):
        tk.Label(
            shortcut_frame,
            text=key,
            font=("Consolas", 10, "bold"),
            bg=FUNCTION_BG,
            fg=TEXT,
            padx=8,
            pady=5
        ).grid(
            row=row,
            column=0,
            padx=(10, 20),
            pady=2,
            sticky="ew"
        )
        tk.Label(
            shortcut_frame,
            text=action,
            font=("Segoe UI", 10),
            bg=BG,
            fg=TEXT
        ).grid(
            row=row,
            column=1,
            padx=10,
            pady=2,
            sticky="w"
        )
# MOUSE WHEEL SCROLLING
    def scroll_shortcuts(event):
        shortcut_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )
        return "break"
    shortcuts_window.bind(
        "<MouseWheel>",
        scroll_shortcuts
    )
# CLOSE BUTTON
    tk.Button(
        shortcuts_window,
        text="Close",
        font=("Segoe UI", 10, "bold"),
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=shortcuts_window.destroy
    ).pack(
        pady=15
    )
# THEME
def toggle_theme():
    global current_theme
    if current_theme == "light":
        current_theme = "dark"
    else:
        current_theme = "light"
    apply_theme()
    if current_theme == "dark":
        set_status(
            "Dark theme enabled"
        )
    else:
        set_status(
            "Light theme enabled"
        )
def apply_theme():
    global BG
    global DISPLAY_BG
    global NUMBER_BG
    global FUNCTION_BG
    global OPERATOR_BG
    global EQUAL_BG
    global MEMORY_BG
    global TEXT
    global MUTED
    global HISTORY_BG
    global HISTORY_TEXT
    global BORDER
    if current_theme == "dark":
        selected_theme = DARK_THEME
    else:
        selected_theme = LIGHT_THEME
    BG = selected_theme["BG"]
    DISPLAY_BG = selected_theme["DISPLAY_BG"]
    NUMBER_BG = selected_theme["NUMBER_BG"]
    FUNCTION_BG = selected_theme["FUNCTION_BG"]
    OPERATOR_BG = selected_theme["OPERATOR_BG"]
    EQUAL_BG = selected_theme["EQUAL_BG"]
    MEMORY_BG = selected_theme["MEMORY_BG"]
    TEXT = selected_theme["TEXT"]
    MUTED = selected_theme["MUTED"]
    HISTORY_BG = selected_theme["HISTORY_BG"]
    HISTORY_TEXT = selected_theme["HISTORY_TEXT"]
    BORDER = selected_theme["BORDER"]

# MAIN WINDOW
    root.configure(
        bg=BG
    )
    main_container.configure(
        bg=BG
    )
    main_canvas.configure(
        bg=BG
    )
    main_frame.configure(
        bg=BG
    )
    calculator_frame.configure(
        bg=BG
    )
 # HEADER
    header_frame.configure(
        bg=BG
    )
    header_title.configure(
        bg=BG,
        fg=TEXT
    )
    header_status.configure(
        bg=BG,
        fg=MUTED
    )
# DISPLAY
    display_card.configure(
        bg=DISPLAY_BG,
        highlightbackground=BORDER
    )
    display.configure(
        bg=DISPLAY_BG,
        fg=TEXT,
        insertbackground=TEXT
    )
    display_status.configure(
        bg=DISPLAY_BG,
        fg=MUTED
    )
    mode_label.configure(
        bg=BG,
        fg="#8AB4F8"
    )
    memory_label.configure(
        bg=BG,
        fg=MUTED
    )
# BUTTON AREA
    button_area.configure(
        bg=BG
    )
    for widget in button_area.winfo_children():
        widget.configure(
            bg=BG
        )
    for button in calculator_buttons:
        value = button.cget(
            "text"
        )
        button.configure(
            bg=get_button_color(value),
            fg=TEXT,
            activebackground=get_button_color(value),
            activeforeground=TEXT
        )
# HISTORY
    history_frame.configure(
        bg=HISTORY_BG
    )
    history_title.configure(
        bg=HISTORY_BG,
        fg=TEXT
    )
    history_box.configure(
        bg=HISTORY_BG,
        fg=HISTORY_TEXT,
        selectbackground=OPERATOR_BG,
        selectforeground=TEXT
    )
    clear_history_button.configure(
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT
    )
# BOTTOM CONTROLS

    bottom_controls.configure(
        bg=BG
    )
    theme_button.configure(
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT
    )
    shortcuts_button.configure(
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT
    )
    statistics_button.configure(
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT
    )
    graph_button.configure(
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT
    )
    programmer_button.configure(
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT
    )
    copy_result_button.configure(
        bg=FUNCTION_BG,
        fg=TEXT,
        activebackground=HOVER_FUNCTION,
        activeforeground=TEXT
    )
    if current_theme == "dark":
        theme_button.configure(
            text="☀ Light Mode"
        )
    else:
        theme_button.configure(
            text="🌙 Dark Mode"
        )
# BOTTOM CONTROL BUTTONS
bottom_controls = tk.Frame(
    calculator_frame,
    bg=BG
)
bottom_controls.pack(
    fill="x",
    pady=(5, 0)
)
# Theme button
theme_button = tk.Button(
    bottom_controls,
    text="🌙 Dark Mode",
    font=("Segoe UI", 9, "bold"),
    bg=FUNCTION_BG,
    fg=TEXT,
    activebackground=HOVER_FUNCTION,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=toggle_theme
)
theme_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 3)
)
# Keyboard shortcuts button
shortcuts_button = tk.Button(
    bottom_controls,
    text="⌨ Keyboard Shortcuts",
    font=("Segoe UI", 9, "bold"),
    bg=FUNCTION_BG,
    fg=TEXT,
    activebackground=HOVER_FUNCTION,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=show_keyboard_shortcuts
)
shortcuts_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=3
)
# Statistics button
statistics_button = tk.Button(
    bottom_controls,
    text="📊 Statistics Mode",
    font=("Segoe UI", 9, "bold"),
    bg=FUNCTION_BG,
    fg=TEXT,
    activebackground=HOVER_FUNCTION,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=statistics_mode
)
statistics_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(3, 0)
)
# Graph button
graph_button = tk.Button(
    bottom_controls,
    text="📈 Graph Plotting Mode",
    font=("Segoe UI", 9, "bold"),
    bg=FUNCTION_BG,
    fg=TEXT,
    activebackground=HOVER_FUNCTION,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=open_graph_mode
)
graph_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(3, 0)
)
# Programmer button
programmer_button = tk.Button(
    bottom_controls,
    text="💻 Programmer Mode",
    font=("Segoe UI", 9, "bold"),
    bg=FUNCTION_BG,
    fg=TEXT,
    activebackground=HOVER_FUNCTION,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=open_programmer_mode
)
programmer_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(3, 0)
)

# COPY RESULT BUTTON
copy_result_button = tk.Button(
    calculator_frame,
    text="📋 Copy Result",
    font=("Segoe UI", 9, "bold"),
    bg=FUNCTION_BG,
    fg=TEXT,
    activebackground=HOVER_FUNCTION,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=copy_result
)
copy_result_button.pack(
    fill="x",
    pady=(5, 0)
)

# KEYBOARD CONTROL
def keyboard_control(event):
    key = event.keysym
    char = event.char

# CTRL SHORTCUTS
    if event.state & 0x0004:
        if key == "1":
            set_degree()
            return "break"
        elif key == "2":
            set_radian()
            return "break"
        elif key == "3":
            memory_clear()
            return "break"
        elif key == "4":
            memory_recall()
            return "break"
        elif key == "5":
            memory_add()
            return "break"
        elif key == "6":
            memory_subtract()
            return "break"
        elif key == "7":
            insert_answer()
            return "break"

# FUNCTION KEYS
    if key == "F1":
        set_degree()
        return "break"
    elif key == "F2":
        set_radian()
        return "break"
    elif key == "F3":
        memory_clear()
        return "break"
    elif key == "F4":
        memory_recall()
        return "break"
    elif key == "F5":
        memory_add()
        return "break"
    elif key == "F6":
        memory_subtract()
        return "break"
    elif key == "F7":
        insert_answer()
        return "break"

# NUMBERS
    if char in "0123456789":
        add(char)
        return "break"

# DECIMAL
    elif char == ".":
        add(".")
        return "break"

# OPERATORS
    elif char == "+":
        add("+")
        return "break"
    elif char == "-":
        add("-")
        return "break"
    elif char == "*":
        add("×")
        return "break"
    elif char == "/":
        add("÷")
        return "break"
    elif char == "^":
        add("^")
        return "break"

# BRACKETS
    elif char in "()":
        add(char)
        return "break"

# ENTER
    elif key in [
        "Return",
        "KP_Enter"
    ]:
        calculate()
        return "break"

# BACKSPACE
    elif key in [
        "BackSpace",
        "Backspace"
    ]:
        backspace()
        return "break"

    # ESCAPE
    elif key == "Escape":
        clear()
        return "break"

# SCIENTIFIC SHORTCUTS
    elif key.lower() == "s":
        scientific("sin")
        return "break"
    elif key.lower() == "c":
        scientific("cos")
        return "break"
    elif key.lower() == "t":
        scientific("tan")
        return "break"
    elif key.lower() == "l":
        scientific("log")
        return "break"
    elif key.lower() == "n":
        scientific("ln")
        return "break"
    elif key.lower() == "q":
        scientific("sqrt")
        return "break"

# GLOBAL KEYBOARD BINDING
root.bind_all(
    "<KeyPress>",
    keyboard_control
)
# START APPLICATION
root.mainloop()