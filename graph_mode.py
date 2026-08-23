import tkinter as tk
from tkinter import messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotting Mode")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)
        self.dark_mode = True
        self.angle_mode = "RAD"
        self.setup_colors()
        self.create_interface()
# COLORS
    def setup_colors(self):
        if self.dark_mode:
            self.colors = {
                "BG": "#202124",
                "CARD": "#303134",
                "INPUT": "#3C4043",
                "BUTTON": "#5F6368",
                "ACCENT": "#3C78D8",
                "SUCCESS": "#34A853",
                "TEXT": "#FFFFFF",
                "MUTED": "#BDC1C6",
                "BORDER": "#5F6368",
            }
        else:
            self.colors = {
                "BG": "#FFFFFF",
                "CARD": "#F8F9FA",
                "INPUT": "#FFFFFF",
                "BUTTON": "#E8EAED",
                "ACCENT": "#4285F4",
                "SUCCESS": "#34A853",
                "TEXT": "#202124",
                "MUTED": "#6B7280",
                "BORDER": "#DADCE0",
            }
# INTERFACE
    def create_interface(self):
        self.root.configure(
            bg=self.colors["BG"]
        )
# MAIN CONTAINER
        main_frame = tk.Frame(
            self.root,
            bg=self.colors["BG"]
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )
# HEADER
        header = tk.Frame(
            main_frame,
            bg=self.colors["BG"]
        )
        header.pack(
            fill="x",
            pady=(0, 12)
        )
        tk.Label(
            header,
            text="📈 Graph Plotting Mode",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors["BG"],
            fg=self.colors["TEXT"]
        ).pack(
            side="left"
        )
        self.mode_label = tk.Label(
            header,
            text="RAD",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["ACCENT"],
            fg="white",
            padx=12,
            pady=5
        )
        self.mode_label.pack(
            side="right"
        )
# CONTROL CARD
        control_card = tk.Frame(
            main_frame,
            bg=self.colors["CARD"],
            highlightbackground=self.colors["BORDER"],
            highlightthickness=1
        )
        control_card.pack(
            fill="x",
            pady=(0, 12)
        )
# Function label
        tk.Label(
            control_card,
            text="FUNCTION",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["CARD"],
            fg=self.colors["MUTED"]
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(12, 4)
        )
# Function entry
        self.function_entry = tk.Entry(
            control_card,
            font=("Consolas", 15),
            bg=self.colors["INPUT"],
            fg=self.colors["TEXT"],
            insertbackground=self.colors["TEXT"],
            relief="flat"
        )
        self.function_entry.grid(
            row=1,
            column=0,
            columnspan=5,
            sticky="ew",
            padx=15,
            pady=(0, 12),
            ipady=8
        )
        self.function_entry.insert(
            0,
            "x^2"
        )
# Example
        tk.Label(
            control_card,
            text="Examples: x^2   sin(x)   cos(x)   sqrt(x)   x^3 + 2*x",
            font=("Segoe UI", 9),
            bg=self.colors["CARD"],
            fg=self.colors["MUTED"]
        ).grid(
            row=2,
            column=0,
            columnspan=5,
            sticky="w",
            padx=15,
            pady=(0, 12)
        )
# X RANGE
        tk.Label(
            control_card,
            text="X MIN",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["CARD"],
            fg=self.colors["MUTED"]
        ).grid(
            row=3,
            column=0,
            padx=(15, 5),
            pady=8
        )
        self.x_min_entry = self.create_small_entry(
            control_card,
            "-10",
            1,
            3
        )
        tk.Label(
            control_card,
            text="X MAX",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["CARD"],
            fg=self.colors["MUTED"]
        ).grid(
            row=3,
            column=2,
            padx=(15, 5),
            pady=8
        )
        self.x_max_entry = self.create_small_entry(
            control_card,
            "10",
            3,
            3
        )
# Y RANGE
        tk.Label(
            control_card,
            text="Y MIN",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["CARD"],
            fg=self.colors["MUTED"]
        ).grid(
            row=4,
            column=0,
            padx=(15, 5),
            pady=8
        )
        self.y_min_entry = self.create_small_entry(
            control_card,
            "-10",
            1,
            4
        )
        tk.Label(
            control_card,
            text="Y MAX",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["CARD"],
            fg=self.colors["MUTED"]
        ).grid(
            row=4,
            column=2,
            padx=(15, 5),
            pady=8
        )
        self.y_max_entry = self.create_small_entry(
            control_card,
            "10",
            3,
            4
        )
# BUTTONS
        button_frame = tk.Frame(
            control_card,
            bg=self.colors["CARD"]
        )
        button_frame.grid(
            row=3,
            column=4,
            rowspan=2,
            padx=15,
            pady=8,
            sticky="nsew"
        )
        self.create_button(
            button_frame,
            "📈 Plot",
            self.plot_graph,
            self.colors["SUCCESS"]
        ).pack(
            side="left",
            padx=3
        )
        self.create_button(
            button_frame,
            "⟳ Reset",
            self.reset_view,
            self.colors["BUTTON"]
        ).pack(
            side="left",
            padx=3
        )
        self.create_button(
            button_frame,
            "Clear",
            self.clear_graph,
            self.colors["BUTTON"]
        ).pack(
            side="left",
            padx=3
        )
# MODE BUTTONS
        mode_frame = tk.Frame(
            control_card,
            bg=self.colors["CARD"]
        )
        mode_frame.grid(
            row=5,
            column=0,
            columnspan=5,
            sticky="ew",
            padx=15,
            pady=(5, 12)
        )
        tk.Label(
            mode_frame,
            text="Angle:",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["CARD"],
            fg=self.colors["MUTED"]
        ).pack(
            side="left",
            padx=(0, 8)
        )
        self.deg_button = self.create_button(
            mode_frame,
            "DEG",
            lambda: self.set_angle_mode("DEG"),
            self.colors["BUTTON"]
        )
        self.deg_button.pack(
            side="left",
            padx=3
        )
        self.rad_button = self.create_button(
            mode_frame,
            "RAD",
            lambda: self.set_angle_mode("RAD"),
            self.colors["ACCENT"]
        )
        self.rad_button.pack(
            side="left",
            padx=3
        )
# Theme
        self.theme_button = self.create_button(
            mode_frame,
            "☀ Light Mode",
            self.toggle_theme,
            self.colors["BUTTON"]
        )
        self.theme_button.pack(
            side="right"
        )
# Configure columns
        control_card.columnconfigure(
            1,
            weight=1
        )
        control_card.columnconfigure(
            3,
            weight=1
        )
# GRAPH AREA
        graph_card = tk.Frame(
            main_frame,
            bg=self.colors["CARD"],
            highlightbackground=self.colors["BORDER"],
            highlightthickness=1
        )
        graph_card.pack(
            fill="both",
            expand=True
        )
        self.figure = plt.Figure(
            figsize=(8, 5),
            dpi=100
        )
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_card
        )
        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )
# Initial graph

        self.reset_view()
# STATUS
        self.status_label = tk.Label(
            main_frame,
            text="Ready — enter a function and click Plot.",
            font=("Segoe UI", 10),
            bg=self.colors["BG"],
            fg=self.colors["MUTED"],
            anchor="w"
        )
        self.status_label.pack(
            fill="x",
            pady=(8, 0)
        )
# SMALL ENTRY
    def create_small_entry(
        self,
        parent,
        default,
        column,
        row
    ):
        entry = tk.Entry(
            parent,
            width=10,
            font=("Consolas", 11),
            bg=self.colors["INPUT"],
            fg=self.colors["TEXT"],
            insertbackground=self.colors["TEXT"],
            relief="flat"
        )
        entry.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=5,
            pady=5,
            ipady=5
        )
        entry.insert(
            0,
            default
        )
        return entry
# BUTTON
    def create_button(
        self,
        parent,
        text,
        command,
        background
    ):
        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=background,
            fg=self.colors["TEXT"],
            activebackground=self.colors["ACCENT"],
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command,
            padx=10,
            pady=6
        )
        return button
# ANGLE MODE
    def set_angle_mode(self, mode):
        self.angle_mode = mode
        self.mode_label.config(
            text=mode
        )
        if mode == "DEG":
            self.deg_button.config(
                bg=self.colors["ACCENT"]
            )
            self.rad_button.config(
                bg=self.colors["BUTTON"]
            )
        else:
            self.deg_button.config(
                bg=self.colors["BUTTON"]
            )
            self.rad_button.config(
                bg=self.colors["ACCENT"]
            )
        self.status_label.config(
            text=f"Angle mode changed to {mode}"
        )
# THEME
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.setup_colors()
# Rebuild window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_interface()
        if self.dark_mode:
            self.theme_button.config(
                text="☀ Light Mode"
            )
        else:
            self.theme_button.config(
                text="🌙 Dark Mode"
            )
# FUNCTION PROCESSING
    def prepare_expression(self, expression):
        expression = expression.strip()
        expression = expression.replace(
            "^",
            "**"
        )
        expression = expression.replace(
            "π",
            "pi"
        )
        expression = expression.replace(
            "×",
            "*"
        )
        expression = expression.replace(
            "÷",
            "/"
        )
        return expression
# MATH ENVIRONMENT
    def create_math_environment(self, x):
        if self.angle_mode == "DEG":
            sin_func = lambda value: np.sin(
                np.deg2rad(value)
            )
            cos_func = lambda value: np.cos(
                np.deg2rad(value)
            )
            tan_func = lambda value: np.tan(
                np.deg2rad(value)
            )
        else:
            sin_func = np.sin
            cos_func = np.cos
            tan_func = np.tan
        environment = {
            "x": x,
            "pi": np.pi,
            "e": np.e,
            "sin": sin_func,
            "cos": cos_func,
            "tan": tan_func,
            "sqrt": np.sqrt,
            "log": np.log10,
            "ln": np.log,
            "exp": np.exp,
            "abs": np.abs,
            "asin": np.arcsin,
            "acos": np.arccos,
            "atan": np.arctan,
            "sinh": np.sinh,
            "cosh": np.cosh,
            "tanh": np.tanh,
        }
        return environment
# PLOT
    def plot_graph(self):
        try:
            expression_text = self.function_entry.get().strip()
            if not expression_text:
                raise ValueError(
                    "Please enter a function."
                )
            x_min = float(
                self.x_min_entry.get()
            )
            x_max = float(
                self.x_max_entry.get()
            )
            y_min = float(
                self.y_min_entry.get()
            )
            y_max = float(
                self.y_max_entry.get()
            )
            if x_min >= x_max:
                raise ValueError(
                    "X MIN must be smaller than X MAX."
                )
            if y_min >= y_max:
                raise ValueError(
                    "Y MIN must be smaller than Y MAX."
                )
# X VALUES
            x = np.linspace(
                x_min,
                x_max,
                2000
            )
# CLEAR
            self.ax.clear()
# MULTIPLE FUNCTIONS
            expressions = [
                item.strip()
                for item in expression_text.split(";")
                if item.strip()
            ]
            for expression in expressions:
                expression = self.prepare_expression(
                    expression
                )
                environment = self.create_math_environment(
                    x
                )
                allowed_names = set(
                    environment.keys()
                )
 # Validate names
                code = compile(
                    expression,
                    "<graph>",
                    "eval"
                )
                for name in code.co_names:
                    if name not in allowed_names:
                        raise ValueError(
                            f"Unsupported function or name: {name}"
                        )
                y = eval(
                    code,
                    {
                        "__builtins__": {}
                    },
                    environment
                )
                y = np.asarray(
                    y,
                    dtype=float
                )
                if y.ndim == 0:
                    y = np.full_like(
                        x,
                        float(y)
                    )
                if y.shape != x.shape:
                    raise ValueError(
                        "The expression did not produce valid graph values."
                    )
# Remove extreme values
                y = np.where(
                    np.isfinite(y),
                    y,
                    np.nan
                )
                self.ax.plot(
                    x,
                    y,
                    linewidth=2,
                    label=f"y = {expression}"
                )
# GRAPH SETTINGS
            self.ax.set_xlim(
                x_min,
                x_max
            )
            self.ax.set_ylim(
                y_min,
                y_max
            )
            self.ax.axhline(
                0,
                linewidth=1
            )
            self.ax.axvline(
                0,
                linewidth=1
            )
            self.ax.grid(
                True,
                alpha=0.3
            )
            if len(expressions) > 1:
                self.ax.legend()
            self.ax.set_xlabel(
                "X"
            )
            self.ax.set_ylabel(
                "Y"
            )
            self.ax.set_title(
                "Function Graph"
            )
            self.figure.tight_layout()
            self.canvas.draw()
            self.status_label.config(
                text=f"Graph plotted successfully — {len(expressions)} function(s)"
            )
        except SyntaxError:
            messagebox.showerror(
                "Invalid Expression",
                "The function contains invalid mathematical syntax."
            )
        except NameError as error:
            messagebox.showerror(
                "Unknown Function",
                str(error)
            )
        except ValueError as error:
            messagebox.showerror(
                "Graph Error",
                str(error)
            )
        except Exception as error:
            messagebox.showerror(
                "Graph Error",
                f"Unable to plot the function.\n\n{error}"
            )
# RESET
    def reset_view(self):
        try:
            x_min = float(
                self.x_min_entry.get()
            )
            x_max = float(
                self.x_max_entry.get()
            )
            y_min = float(
                self.y_min_entry.get()
            )
            y_max = float(
                self.y_max_entry.get()
            )
        except Exception:
            x_min = -10
            x_max = 10
            y_min = -10
            y_max = 10
        self.ax.clear()
        self.ax.set_xlim(
            x_min,
            x_max
        )
        self.ax.set_ylim(
            y_min,
            y_max
        )
        self.ax.axhline(
            0,
            linewidth=1
        )
        self.ax.axvline(
            0,
            linewidth=1
        )
        self.ax.grid(
            True,
            alpha=0.3
        )
        self.ax.set_xlabel(
            "X"
        )
        self.ax.set_ylabel(
            "Y"
        )
        self.ax.set_title(
            "Function Graph"
        )
        self.figure.tight_layout()
        self.canvas.draw()
        if hasattr(
            self,
            "status_label"
        ):
            self.status_label.config(
                text="View reset."
            )
# CLEAR GRAPH
    def clear_graph(self):
        self.ax.clear()
        self.ax.set_xlim(
            -10,
            10
        )
        self.ax.set_ylim(
            -10,
            10
        )
        self.ax.axhline(
            0,
            linewidth=1
        )
        self.ax.axvline(
            0,
            linewidth=1
        )
        self.ax.grid(
            True,
            alpha=0.3
        )
        self.ax.set_xlabel(
            "X"
        )
        self.ax.set_ylabel(
            "Y"
        )
        self.ax.set_title(
            "Function Graph"
        )
        self.figure.tight_layout()
        self.canvas.draw()
        self.status_label.config(
            text="Graph cleared."
        )
# START APPLICATION
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphPlotter(
        root
    )
    root.mainloop()