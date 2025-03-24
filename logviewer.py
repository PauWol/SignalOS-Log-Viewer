import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from pathlib import Path

class LogViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Log Viewer")
        self.geometry("900x600")
        self.current_db_path = None

        self._create_menu()
        self._create_toolbar()
        self._create_filter_section()
        self._create_table()
        self._create_statusbar()

    def _create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Log File...", command=self.open_log_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def _create_toolbar(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        refresh_btn = ttk.Button(toolbar, text="Refresh", command=self.load_logs)
        refresh_btn.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def _create_filter_section(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(filter_frame, text="Filter by Level:").pack(side=tk.LEFT, padx=(0, 5))
        self.level_filter = tk.StringVar(value="All")
        levels = ["All", "TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "FATAL"]
        dropdown = ttk.Combobox(filter_frame, textvariable=self.level_filter, values=levels, state="readonly")
        dropdown.pack(side=tk.LEFT)
        dropdown.bind("<<ComboboxSelected>>", lambda e: self.load_logs())

    def _create_table(self):
        columns = ("ID", "Level", "Time", "File", "Function", "Line", "Message")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_logs(c))
            # Adjust column width: message gets more space
            width = 100 if col != "Message" else 300
            self.tree.column(col, anchor="w", width=width)

        # Enable vertical and horizontal scrolling
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.pack(expand=True, fill="both", padx=10, pady=(0,10))
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_statusbar(self):
        self.status = tk.StringVar()
        statusbar = tk.Label(self, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor="w")
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self._update_status("No log file selected.")

    def _update_status(self, message: str):
        self.status.set(message)

    def open_log_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Log Database",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_db_path = Path(file_path)
            self._update_status(f"Log file: {self.current_db_path.resolve()}")
            self.load_logs()

    def load_logs(self):
        if not self.current_db_path or not self.current_db_path.exists():
            messagebox.showerror("Error", "No valid log file selected.")
            return

        try:
            conn = sqlite3.connect(self.current_db_path.resolve())
            cursor = conn.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open database: {e}")
            return

        query = "SELECT id, level, time, file, function, line, message FROM logs"
        params = ()

        level = self.level_filter.get()
        if level != "All":
            query += " WHERE level = ?"
            params = (self.get_level_number(level),)

        try:
            cursor.execute(query, params)
            logs = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Query error: {e}")
            logs = []
        finally:
            conn.close()

        # Clear existing items
        self.tree.delete(*self.tree.get_children())
        for log in logs:
            # Optionally convert level number back to string
            level_str = self.get_level_string(log[1])
            values = (log[0], level_str, log[2], log[3], log[4], log[5], log[6])
            self.tree.insert("", "end", values=values)

        self._update_status(f"Loaded {len(logs)} log entries from {self.current_db_path.resolve()}")

    def sort_logs(self, col):
        """Sort the logs by the given column."""
        try:
            data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        except Exception as e:
            messagebox.showerror("Error", f"Sorting error: {e}")
            return

        # For numeric columns (ID and Line), sort numerically
        if col in ("ID", "Line"):
            data.sort(key=lambda t: int(t[0]))
        else:
            data.sort(key=lambda t: t[0].lower())

        # Rearrange items in sorted order
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)

    @staticmethod
    def get_level_number(level_name: str) -> int:
        levels = {"TRACE": 0, "DEBUG": 1, "INFO": 2, "WARNING": 3, "ERROR": 4, "FATAL": 5}
        return levels.get(level_name, 0)

    @staticmethod
    def get_level_string(level_number: int) -> str:
        level_strings = {0: "TRACE", 1: "DEBUG", 2: "INFO", 3: "WARNING", 4: "ERROR", 5: "FATAL"}
        return level_strings.get(level_number, "UNKNOWN")



app = LogViewer()
app.mainloop()
