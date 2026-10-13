import tkinter as tk
from tkinter import messagebox, ttk
from decimal import Decimal

from app.core.engine import CalculationError, evaluate
from app.core.finance import discount_vat
from app.core.formatter import format_number
from app.core.units import UNITS, convert
from app.data.storage import Storage


COLORS = {
    "dark": {
        "bg": "#0F1115", "surface": "#181B22", "key": "#222631",
        "operator": "#2E3445", "accent": "#7C5CFF", "text": "#F2F4F8",
        "muted": "#8A93A6", "danger": "#FF5C6C", "border": "#343A49",
    },
    "light": {
        "bg": "#F5F6FA", "surface": "#FFFFFF", "key": "#ECEEF4",
        "operator": "#DDE1EC", "accent": "#6A48F5", "text": "#12141A",
        "muted": "#6B7385", "danger": "#E5384C", "border": "#D6D9E2",
    },
}


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Razza Smart Kalkulator")
        self.minsize(340, 560)
        self.storage = Storage()
        self.settings = self.storage.load_settings()
        self.history = self.storage.load_history()
        self.memory = Decimal(0)
        self.answer = None
        self.theme_name = self._resolve_theme(self.settings["theme"])
        self.colors = COLORS[self.theme_name]
        self.expression = tk.StringVar()
        self.preview = tk.StringVar(value="")
        self.result = tk.StringVar(value="0")
        self._history_window = None
        self._build_window()
        self._set_geometry()
        self._apply_theme()
        self.expression.trace_add("write", self._update_preview)
        self.bind("<Return>", self._calculate_event)
        self.bind("<KP_Enter>", self._calculate_event)
        self.bind("<Escape>", lambda event: self._clear())
        self.bind("<Delete>", lambda event: self._clear_entry())
        self.bind("<BackSpace>", self._backspace)
        self.bind("<Control-c>", self._copy_result)
        self.bind("<Control-C>", self._copy_result)
        self.bind("<Control-v>", self._paste_expression)
        self.bind("<Control-V>", self._paste_expression)
        self.bind("<Control-h>", lambda event: self._toggle_history())
        self.bind("<Control-H>", lambda event: self._toggle_history())
        self.bind("<Control-t>", lambda event: self._toggle_theme())
        self.bind("<Control-T>", lambda event: self._toggle_theme())
        for index in range(1, 5):
            self.bind("<Control-%d>" % index, lambda event, i=index: self.tabs.select(i - 1))
        self.bind("<Control-Shift-T>", lambda event: self._toggle_topmost())
        self.protocol("WM_DELETE_WINDOW", self._close)
        if self.storage.warning:
            self.after(300, lambda: self._status(self.storage.warning))

    def _build_window(self):
        self.minsize(320, 480)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.header = tk.Frame(self, padx=18, pady=12)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.columnconfigure(1, weight=1)
        self._label(self.header, "Razza", 17, bold=True).grid(row=0, column=0, sticky="w")
        self._label(self.header, "SMART KALKULATOR", 9, muted=True).grid(
            row=1, column=0, sticky="w"
        )
        self.history_button = self._button(
            self.header, "Riwayat", self._toggle_history, role="operator", compact=True
        )
        self.history_button.grid(row=0, column=2, rowspan=2, padx=(6, 0))
        self.clear_entry_button = self._button(
            self.header, "CE", self._clear_entry, role="operator", compact=True
        )
        self.clear_entry_button.grid(row=0, column=3, rowspan=2, padx=(6, 0))
        self.theme_button = self._button(
            self.header, "◐", self._toggle_theme, role="operator", compact=True
        )
        self.theme_button.grid(row=0, column=4, rowspan=2, padx=(6, 0))
        self.settings_button = self._button(
            self.header, "⚙", self._settings_dialog, role="operator", compact=True
        )
        self.settings_button.grid(row=0, column=5, rowspan=2, padx=(6, 0))

        self.display = tk.Frame(self, padx=20, pady=16)
        self.display.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        self.display.columnconfigure(0, weight=1)
        self.input = tk.Entry(
            self.display, textvariable=self.expression, justify="right",
            relief="flat", font=("Segoe UI", 15), bd=0,
        )
        self.input.grid(row=0, column=0, sticky="ew", ipady=6)
        self.preview_label = self._label(
            self.display, "", 11, muted=True, variable=self.preview
        )
        self.preview_label.grid(row=1, column=0, sticky="e", pady=(7, 2))
        self.result_label = self._label(
            self.display, "0", 34, bold=True, variable=self.result
        )
        self.result_label.grid(row=2, column=0, sticky="e")
        self.status = self._label(self.display, "", 10, muted=True)
        self.status.grid(row=3, column=0, sticky="e", pady=(4, 0))

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self.standard_tab = tk.Frame(self.tabs, padx=10, pady=10)
        self.scientific_tab = tk.Frame(self.tabs, padx=10, pady=10)
        self.converter_tab = tk.Frame(self.tabs, padx=16, pady=18)
        self.discount_tab = tk.Frame(self.tabs, padx=16, pady=18)
        self.tabs.add(self.standard_tab, text="Standar")
        self.tabs.add(self.scientific_tab, text="Ilmiah")
        self.tabs.add(self.converter_tab, text="Konverter")
        self.tabs.add(self.discount_tab, text="Diskon & PPN")
        self._build_keypad(self.standard_tab, scientific=False)
        self._build_keypad(self.scientific_tab, scientific=True)
        self._build_converter()
        self._build_discount()
        self.input.focus_set()

    def _label(self, parent, text, size=12, bold=False, muted=False, variable=None):
        label = tk.Label(
            parent, text=text, textvariable=variable,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            anchor="w", padx=0, pady=0,
        )
        label._muted = muted
        return label

    def _button(self, parent, text, command, role="key", compact=False):
        button = tk.Button(
            parent, text=text, command=command, relief="flat", bd=0,
            font=("Segoe UI", 10 if compact else 15, "bold" if text == "=" else "normal"),
            padx=8 if compact else 4, pady=5 if compact else 9,
            takefocus=True, cursor="hand2",
        )
        button._role = role
        button.bind("<Enter>", lambda event, widget=button: self._hover(widget, True))
        button.bind("<Leave>", lambda event, widget=button: self._hover(widget, False))
        return button

    def _build_keypad(self, parent, scientific):
        parent.columnconfigure(tuple(range(4)), weight=1, uniform="keys")
        row = 0
        if scientific:
            functions = [
                ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
                ("asin", "asin("), ("acos", "acos("), ("atan", "atan("),
                ("log", "log("), ("ln", "ln("), ("√", "sqrt("),
                ("x²", "**2"), ("xʸ", "**"), ("n!", "factorial("),
                ("1/x", "1/"), ("|x|", "abs("), ("π", "pi"),
                ("e", "e"), ("DEG/RAD", "angle"), ("Ans", "ans"),
            ]
            self.scientific_angle = tk.StringVar(value=self.settings.get("angle_unit", "deg").upper())
            for index, (label, value) in enumerate(functions):
                actual = self.scientific_angle.get() if value == "angle" else label
                button = self._button(
                    parent, actual,
                    lambda v=value: self._angle_toggle() if v == "angle" else self._insert(v),
                    role="operator", compact=True,
                )
                button.grid(row=row + index // 4, column=index % 4, sticky="nsew", padx=3, pady=3)
                if value == "angle":
                    self.angle_button = button
            row += (len(functions) + 3) // 4

        mem_row = tk.Frame(parent)
        mem_row.grid(row=row, column=0, columnspan=4, sticky="ew", pady=(4, 6))
        for col, (label, action) in enumerate((
            ("MC", self._memory_clear), ("MR", self._memory_recall),
            ("M+", lambda: self._memory_add(1)), ("M−", lambda: self._memory_add(-1)),
        )):
            mem_row.columnconfigure(col, weight=1)
            self._button(mem_row, label, action, role="operator", compact=True).grid(
                row=0, column=col, sticky="ew", padx=2
            )
        row += 1
        keys = [
            [("C", self._clear, "danger"), ("( )", self._parentheses, "operator"),
             ("%", lambda: self._insert("%"), "operator"), ("÷", lambda: self._insert("÷"), "operator")],
            [("7", lambda: self._insert("7"), "key"), ("8", lambda: self._insert("8"), "key"),
             ("9", lambda: self._insert("9"), "key"), ("×", lambda: self._insert("×"), "operator")],
            [("4", lambda: self._insert("4"), "key"), ("5", lambda: self._insert("5"), "key"),
             ("6", lambda: self._insert("6"), "key"), ("−", lambda: self._insert("−"), "operator")],
            [("1", lambda: self._insert("1"), "key"), ("2", lambda: self._insert("2"), "key"),
             ("3", lambda: self._insert("3"), "key"), ("+", lambda: self._insert("+"), "operator")],
            [("±", self._toggle_sign, "operator"), ("0", lambda: self._insert("0"), "key"),
             (",", lambda: self._insert(","), "key"), ("=", self._calculate, "accent")],
        ]
        for offset, line in enumerate(keys):
            for col, (label, action, role) in enumerate(line):
                button = self._button(parent, label, action, role=role)
                button.grid(row=row + offset, column=col, sticky="nsew", padx=3, pady=3)
                parent.rowconfigure(row + offset, weight=1, uniform="keyrows")

    def _build_converter(self):
        self.converter_tab.columnconfigure(0, weight=1)
        self._label(self.converter_tab, "Konversi satuan", 18, bold=True).grid(
            row=0, column=0, sticky="w", pady=(0, 14)
        )
        self.category = tk.StringVar(value="Panjang")
        self.source_unit = tk.StringVar(value="Meter")
        self.target_unit = tk.StringVar(value="Kilometer")
        self.convert_value = tk.StringVar(value="1")
        self.convert_result = tk.StringVar(value="")
        self._label(self.converter_tab, "Kategori", 10, muted=True).grid(row=1, column=0, sticky="w")
        self.category_box = ttk.Combobox(
            self.converter_tab, textvariable=self.category, values=list(UNITS), state="readonly"
        )
        self.category_box.grid(row=2, column=0, sticky="ew", pady=(4, 12))
        self._label(self.converter_tab, "Dari", 10, muted=True).grid(row=3, column=0, sticky="w")
        self.source_box = ttk.Combobox(
            self.converter_tab, textvariable=self.source_unit, state="readonly"
        )
        self.source_box.grid(row=4, column=0, sticky="ew", pady=(4, 10))
        self._label(self.converter_tab, "Nilai", 10, muted=True).grid(row=5, column=0, sticky="w")
        self.convert_entry = tk.Entry(self.converter_tab, textvariable=self.convert_value, font=("Segoe UI", 13))
        self.convert_entry.grid(row=6, column=0, sticky="ew", ipady=7, pady=(4, 12))
        self.swap_button = self._button(
            self.converter_tab, "Tukar satuan  ⇅", self._swap_units, role="operator"
        )
        self.swap_button.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        self._label(self.converter_tab, "Ke", 10, muted=True).grid(row=8, column=0, sticky="w")
        self.target_box = ttk.Combobox(
            self.converter_tab, textvariable=self.target_unit, state="readonly"
        )
        self.target_box.grid(row=9, column=0, sticky="ew", pady=(4, 10))
        self.convert_output = self._label(
            self.converter_tab, "", 20, bold=True, variable=self.convert_result
        )
        self.convert_output.grid(row=10, column=0, sticky="w", pady=(12, 0))
        self.category_box.bind("<<ComboboxSelected>>", self._category_changed)
        self.source_box.bind("<<ComboboxSelected>>", lambda event: self._convert_units())
        self.target_box.bind("<<ComboboxSelected>>", lambda event: self._convert_units())
        self.convert_value.trace_add("write", self._convert_units)
        self._category_changed()

    def _build_discount(self):
        self.discount_tab.columnconfigure(0, weight=1)
        self._label(self.discount_tab, "Kalkulator diskon & PPN", 18, bold=True).grid(
            row=0, column=0, sticky="w", pady=(0, 14)
        )
        self.discount_price = tk.StringVar(value="100000")
        self.discount_percent = tk.StringVar(value="10")
        self.vat_percent = tk.StringVar(value="11")
        self.discount_result = tk.StringVar(value="Masukkan harga dan persentase.")
        for row, (caption, variable) in enumerate((
            ("Harga awal (Rp)", self.discount_price),
            ("Diskon (%)", self.discount_percent),
            ("PPN (%)", self.vat_percent),
        ), start=1):
            self._label(self.discount_tab, caption, 10, muted=True).grid(
                row=(row - 1) * 2 + 1, column=0, sticky="w"
            )
            entry = tk.Entry(self.discount_tab, textvariable=variable, font=("Segoe UI", 13))
            entry.grid(row=(row - 1) * 2 + 2, column=0, sticky="ew", ipady=7, pady=(4, 12))
        self._button(
            self.discount_tab, "Hitung harga akhir", self._calculate_discount, role="accent"
        ).grid(row=7, column=0, sticky="ew", pady=(2, 12))
        self.discount_output = self._label(
            self.discount_tab, "", 12, variable=self.discount_result
        )
        self.discount_output.grid(row=8, column=0, sticky="w")

    def _set_geometry(self):
        window = self.settings.get("window", {})
        width = max(340, int(window.get("width") or 430))
        height = max(560, int(window.get("height") or 720))
        x, y = window.get("x"), window.get("y")
        self.geometry("%dx%d%s" % (width, height, "+%s+%s" % (x, y) if x is not None and y is not None else ""))
        self.attributes("-topmost", bool(self.settings.get("always_on_top", False)))

    def _apply_theme(self):
        self.colors = COLORS[self.theme_name]
        colors = self.colors
        self.configure(bg=colors["bg"])
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=colors["bg"])
        style.configure("TLabel", background=colors["bg"], foreground=colors["text"])
        style.configure(
            "TNotebook", background=colors["bg"], borderwidth=0, tabmargins=(2, 4, 2, 0)
        )
        style.configure(
            "TNotebook.Tab", background=colors["key"], foreground=colors["muted"],
            padding=(10, 8), font=("Segoe UI", 9),
        )
        style.map(
            "TNotebook.Tab", background=[("selected", colors["surface"])],
            foreground=[("selected", colors["text"])],
        )
        style.configure(
            "TCombobox", fieldbackground=colors["surface"], background=colors["key"],
            foreground=colors["text"], arrowcolor=colors["text"],
        )
        self._theme_children(self)
        for window in (self._history_window,):
            if window and window.winfo_exists():
                self._theme_children(window)

    def _theme_children(self, parent):
        colors = self.colors
        if isinstance(parent, tk.Toplevel):
            parent.configure(bg=colors["bg"])
        for child in parent.winfo_children():
            if isinstance(child, ttk.Widget):
                pass
            elif isinstance(child, (tk.Frame, tk.LabelFrame)):
                child.configure(bg=colors["bg"])
            elif isinstance(child, tk.Checkbutton):
                child.configure(
                    bg=colors["bg"], fg=colors["text"], selectcolor=colors["surface"],
                    activebackground=colors["bg"], activeforeground=colors["text"],
                )
            elif isinstance(child, tk.Label):
                foreground = colors["muted"] if getattr(child, "_muted", False) else colors["text"]
                if child is self.discount_output and child.cget("text").startswith("Harga akhir"):
                    foreground = colors["accent"]
                child.configure(bg=colors["bg"], fg=foreground)
            elif isinstance(child, tk.Entry):
                child.configure(
                    bg=colors["surface"], fg=colors["text"], insertbackground=colors["text"],
                    selectbackground=colors["accent"], relief="flat",
                    highlightthickness=1, highlightbackground=colors["border"],
                    highlightcolor=colors["accent"],
                )
            elif isinstance(child, tk.Button):
                self._style_button(child)
            self._theme_children(child)

    def _style_button(self, button):
        colors = self.colors
        role = getattr(button, "_role", "key")
        bg = colors["accent"] if role == "accent" else (
            colors["danger"] if role == "danger" else
            colors["operator"] if role == "operator" else colors["key"]
        )
        fg = "#FFFFFF" if role in ("accent", "danger") else colors["text"]
        button.configure(
            bg=bg, fg=fg, activebackground=colors["accent"] if role != "danger" else colors["danger"],
            activeforeground="#FFFFFF", highlightthickness=0,
        )

    def _hover(self, button, entering):
        if not button.winfo_exists():
            return
        if entering:
            button.configure(relief="sunken")
        else:
            button.configure(relief="flat")

    def _insert(self, value):
        if value in ("pi", "e", "ans", "sin(", "cos(", "tan(", "asin(", "acos(", "atan(", "log(", "ln(", "sqrt(", "factorial(", "abs("):
            insertion = value
        else:
            insertion = value
        self.input.insert(tk.INSERT, insertion)
        self.input.focus_set()

    def _update_preview(self, *_):
        expression = self.expression.get().strip()
        if not expression:
            self.preview.set("")
            self.result.set("0")
            return
        try:
            value = evaluate(expression, self.settings.get("angle_unit", "deg"), self.answer)
            output = format_number(value, self.settings.get("number_format", "id"), self.settings.get("max_decimals", 10))
            self.preview.set("≈ " + output)
            self.status.configure(text="")
        except CalculationError as error:
            if str(error) in ("Masukkan ekspresi", "Ekspresi tidak valid"):
                self.preview.set("")
            else:
                self.preview.set("")

    def _calculate(self):
        expression = self.expression.get().strip()
        try:
            value = evaluate(expression, self.settings.get("angle_unit", "deg"), self.answer)
        except CalculationError as error:
            self.result.set("—")
            self.preview.set("")
            self.status.configure(text=str(error), fg=self.colors["danger"])
            return
        rendered = format_number(
            value, self.settings.get("number_format", "id"),
            self.settings.get("max_decimals", 10),
        )
        self.answer = value
        self.result.set(rendered)
        self.preview.set("")
        self.status.configure(text="", fg=self.colors["muted"])
        self.history.insert(0, {"expression": expression, "result": str(value)})
        self.history = self.history[:500]
        self._save_history()
        self._refresh_history()

    def _calculate_event(self, _event):
        self._calculate()
        return "break"

    def _clear(self):
        self.expression.set("")
        self.result.set("0")
        self.status.configure(text="")
        self.input.focus_set()

    def _clear_entry(self):
        text = self.expression.get()
        if not text:
            return
        boundary = max(text.rfind("+"), text.rfind("−"), text.rfind("-"),
                       text.rfind("×"), text.rfind("÷"), text.rfind("*"),
                       text.rfind("/"), text.rfind("("))
        expression = text[:boundary + 1]
        tail = text[boundary + 1:]
        if not tail and expression.endswith("("):
            expression = expression[:-1]
        self.expression.set(expression)
        self.status.configure(text="")
        self.input.focus_set()

    def _backspace(self, _event):
        index = self.input.index(tk.INSERT)
        if index > 0:
            self.input.delete(index - 1)
        return "break"

    def _parentheses(self):
        text = self.expression.get()
        self._insert(")" if text.count("(") > text.count(")") and text[-1:] not in "+-*/(" else "(")

    def _toggle_sign(self):
        text = self.expression.get().strip()
        if not text:
            self._insert("−")
        elif text.startswith("−"):
            self.expression.set(text[1:])
        else:
            self.expression.set("−(" + text + ")")

    def _copy_result(self, _event=None):
        value = self.preview.get().replace("≈ ", "") or self.result.get()
        if value and value != "—":
            self.clipboard_clear()
            self.clipboard_append(value)
            self._status("Hasil disalin")
        return "break"

    def _paste_expression(self, _event=None):
        try:
            text = self.clipboard_get()
        except tk.TclError:
            self._status("Clipboard tidak berisi teks.")
            return "break"
        self.expression.set(text)
        self.input.icursor(tk.END)
        return "break"

    def _toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.settings["theme"] = self.theme_name
        self._apply_theme()
        self._save_settings()

    @staticmethod
    def _resolve_theme(theme):
        if theme in COLORS:
            return theme
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                light_mode, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if light_mode else "dark"
        except (ImportError, OSError):
            return "light"

    def _angle_toggle(self):
        current = self.settings.get("angle_unit", "deg")
        self.settings["angle_unit"] = "rad" if current == "deg" else "deg"
        self.angle_button.configure(text=self.settings["angle_unit"].upper())
        self._update_preview()
        self._save_settings()

    def _memory_clear(self):
        self.memory = Decimal(0)
        self._status("Memori dihapus")

    def _memory_recall(self):
        self._insert(format(self.memory, "f"))

    def _memory_add(self, sign):
        try:
            current = evaluate(self.expression.get(), self.settings.get("angle_unit", "deg"), self.answer)
        except CalculationError:
            current = self.answer or Decimal(0)
        self.memory += current * sign
        self._status("Memori diperbarui")

    def _toggle_history(self):
        if self._history_window and self._history_window.winfo_exists():
            self._history_window.destroy()
            self._history_window = None
            return
        self._history_window = tk.Toplevel(self)
        self._history_window.title("Riwayat perhitungan")
        self._history_window.geometry("350x460")
        self._history_window.minsize(300, 300)
        self._history_window.transient(self)
        self._history_window.columnconfigure(0, weight=1)
        self._history_window.rowconfigure(1, weight=1)
        frame = tk.Frame(self._history_window, padx=12, pady=12)
        frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        frame.columnconfigure(0, weight=1)
        self._label(frame, "Riwayat", 17, bold=True).grid(row=0, column=0, sticky="w")
        self._button(frame, "Hapus semua", self._clear_history, role="danger", compact=True).grid(row=0, column=1)
        self.history_list = tk.Listbox(
            self._history_window, relief="flat", font=("Segoe UI", 11), activestyle="none"
        )
        self.history_list.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=12)
        self.history_list.bind("<<ListboxSelect>>", self._reuse_history)
        self.history_list.bind("<Double-Button-1>", self._reuse_history)
        self._button(
            self._history_window, "Hapus pilihan", self._delete_history_entry,
            role="operator", compact=True,
        ).grid(row=2, column=0, sticky="ew", padx=12, pady=10)
        self._button(
            self._history_window, "Tutup", self._close_history, role="operator", compact=True,
        ).grid(row=2, column=1, sticky="ew", padx=(0, 12), pady=10)
        self._theme_children(self._history_window)
        self._refresh_history()

    def _close_history(self):
        if self._history_window and self._history_window.winfo_exists():
            self._history_window.destroy()
        self._history_window = None

    def _refresh_history(self):
        if not self._history_window or not self._history_window.winfo_exists():
            return
        self.history_list.delete(0, tk.END)
        for item in self.history:
            rendered = format_number(
                Decimal(item["result"]), self.settings.get("number_format", "id"),
                self.settings.get("max_decimals", 10),
            )
            self.history_list.insert(tk.END, "%s   =   %s" % (item["expression"], rendered))

    def _reuse_history(self, _event=None):
        selection = self.history_list.curselection()
        if selection:
            self.expression.set(self.history[selection[0]]["expression"])
            self.input.focus_set()

    def _delete_history_entry(self):
        selection = self.history_list.curselection()
        if selection:
            del self.history[selection[0]]
            self._save_history()
            self._refresh_history()

    def _clear_history(self):
        if messagebox.askyesno("Hapus riwayat", "Hapus seluruh riwayat perhitungan?", parent=self._history_window):
            self.history.clear()
            self._save_history()
            self._refresh_history()

    def _category_changed(self, _event=None):
        units = list(UNITS[self.category.get()])
        self.source_box.configure(values=units)
        self.target_box.configure(values=units)
        self.source_unit.set(units[0])
        self.target_unit.set(units[1] if len(units) > 1 else units[0])
        self._convert_units()

    def _convert_units(self, *_):
        try:
            result = convert(
                self.convert_value.get().replace(",", "."),
                self.category.get(), self.source_unit.get(), self.target_unit.get(),
            )
            self.convert_result.set(
                format_number(result, self.settings.get("number_format", "id"), self.settings.get("max_decimals", 10))
            )
        except (ValueError, ArithmeticError):
            self.convert_result.set("Masukkan angka yang valid")

    def _swap_units(self):
        source, target = self.source_unit.get(), self.target_unit.get()
        self.source_unit.set(target)
        self.target_unit.set(source)
        self._convert_units()

    def _calculate_discount(self):
        try:
            result = discount_vat(
                self.discount_price.get().replace(".", "").replace(",", "."),
                self.discount_percent.get().replace(",", "."),
                self.vat_percent.get().replace(",", "."),
            )
        except (ValueError, ArithmeticError):
            self.discount_result.set("Periksa kembali angka yang dimasukkan.")
            return
        fmt = lambda value: format_number(value, self.settings.get("number_format", "id"), self.settings.get("max_decimals", 10))
        self.discount_result.set(
            "Hemat: Rp %s\nHarga setelah diskon: Rp %s\nPPN: Rp %s\nHarga akhir: Rp %s"
            % (fmt(result["savings"]), fmt(result["discounted_price"]),
               fmt(result["vat_amount"]), fmt(result["final_price"]))
        )
        self.discount_output.configure(fg=self.colors["accent"])

    def _settings_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Pengaturan")
        dialog.geometry("340x340")
        dialog.resizable(False, False)
        dialog.transient(self)
        frame = tk.Frame(dialog, padx=18, pady=18)
        frame.pack(fill="both", expand=True)
        self._label(frame, "Pengaturan", 18, bold=True).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))
        theme = tk.StringVar(value=self.settings.get("theme", "dark"))
        number_format = tk.StringVar(value=self.settings.get("number_format", "id"))
        decimals = tk.StringVar(value=str(self.settings.get("max_decimals", 10)))
        always_top = tk.BooleanVar(value=self.settings.get("always_on_top", False))
        options = [
            ("Tema", theme, [("Gelap", "dark"), ("Terang", "light"), ("Sistem", "system")]),
            ("Format angka", number_format, [("Indonesia", "id"), ("Internasional", "intl")]),
            ("Desimal maksimum", decimals, [(str(n), str(n)) for n in range(2, 13)] + [("Otomatis", "auto")]),
        ]
        for row, (label, variable, values) in enumerate(options, start=1):
            self._label(frame, label, 10, muted=True).grid(row=row * 2 - 1, column=0, columnspan=2, sticky="w")
            box = ttk.Combobox(
                frame, textvariable=variable,
                values=[text for text, _ in values], state="readonly",
            )
            box.grid(row=row * 2, column=0, columnspan=2, sticky="ew", pady=(4, 10))
            box._value_map = {text: val for text, val in values}
            box.bind("<<ComboboxSelected>>", lambda event, v=variable, b=box: v.set(b._value_map[b.get()]))
            variable.trace_add("write", lambda *_args, v=variable, b=box: self._select_setting_label(b, v))
            self._select_setting_label(box, variable)
        check = tk.Checkbutton(
            frame, text="Selalu di atas", variable=always_top,
            font=("Segoe UI", 10), anchor="w",
        )
        check.grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 8))
        check._role = "key"
        self._button(frame, "Hapus semua data", lambda: self._clear_all_data(dialog), role="danger", compact=True).grid(
            row=8, column=0, sticky="ew", padx=(0, 4)
        )
        self._button(frame, "Simpan", lambda: self._save_preferences(
            dialog, theme.get(), number_format.get(), decimals.get(), always_top.get()
        ), role="accent", compact=True).grid(row=8, column=1, sticky="ew", padx=(4, 0))
        frame.columnconfigure((0, 1), weight=1)
        self._theme_children(dialog)

    @staticmethod
    def _select_setting_label(box, variable):
        mapping = getattr(box, "_value_map", {})
        selected = next((label for label, value in mapping.items() if value == variable.get()), None)
        if selected:
            box.set(selected)

    def _save_preferences(self, dialog, theme, number_format, decimals, always_top):
        self.settings.update({
            "theme": theme, "number_format": number_format,
            "max_decimals": "auto" if decimals == "auto" else int(decimals),
            "always_on_top": always_top,
        })
        self.theme_name = self._resolve_theme(theme)
        self.attributes("-topmost", always_top)
        self._apply_theme()
        self._update_preview()
        self._refresh_history()
        self._save_settings()
        dialog.destroy()

    def _clear_all_data(self, dialog):
        if not messagebox.askyesno(
            "Hapus semua data", "Pengaturan dan riwayat akan dihapus. Lanjutkan?", parent=dialog
        ):
            return
        self.storage.clear()
        self.history.clear()
        self._refresh_history()
        self.settings = dict(self.storage.load_settings())
        self.theme_name = "dark"
        self._save_history()
        self._save_settings()
        dialog.destroy()
        self._apply_theme()
        self._status("Riwayat dan pengaturan direset.")

    def _toggle_topmost(self):
        value = not self.settings.get("always_on_top", False)
        self.settings["always_on_top"] = value
        self.attributes("-topmost", value)
        self._save_settings()
        self._status("Selalu di atas " + ("aktif" if value else "nonaktif"))

    def _status(self, message):
        self.status.configure(text=message, fg=self.colors["muted"])
        self.after(1800, lambda: self.status.configure(text="") if self.status.winfo_exists() else None)

    def _save_settings(self):
        try:
            self.storage.save_settings(self.settings)
        except OSError as error:
            self._status("Pengaturan gagal disimpan: %s" % error)

    def _save_history(self):
        try:
            self.storage.save_history(self.history)
        except OSError as error:
            self._status("Riwayat gagal disimpan: %s" % error)

    def _close(self):
        geometry = self.geometry().split("+")
        dimensions = geometry[0].split("x")
        self.settings["window"] = {
            "width": int(dimensions[0]), "height": int(dimensions[1]),
            "x": int(geometry[1]) if len(geometry) > 1 else None,
            "y": int(geometry[2]) if len(geometry) > 2 else None,
        }
        self._save_settings()
        self.destroy()
