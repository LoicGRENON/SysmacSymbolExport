import tkinter as tk
from tkinter import ttk


class SymbolsTreeview(ttk.Treeview):
    def __init__(self, master):
        frame = ttk.Frame(master, padding=10)
        super().__init__(
            frame,
            columns = ('Name', 'Type'),
            selectmode = 'browse',
            show = 'headings'
        )

        self.heading("#0", text="")
        self.heading("Name", text="Symbol name")
        self.heading("Type", text="Type")

        # Define column widths
        self.column("#0", width=10, stretch=False)
        self.column("Name", width=300, anchor='w', stretch=False)
        self.column("Type", width=150, anchor='center', stretch=False)

        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.xview)
        self.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack the Treeview, scrollbars and frame
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame.pack(fill=tk.BOTH, expand=True)

    def update_symbols(self, data):
        self.delete(*self.get_children())
        for symbol in data:
            self.insert(
                '',
                tk.END,
                text=symbol.name,
                values=(
                    symbol.name,
                    symbol.base_type
                )
            )
