import tkinter as tk
from datetime import datetime
from functools import partial
from tkinter import ttk


class ProjectsTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        frame = ttk.Frame(master, **kwargs)
        super().__init__(
            frame,
            columns = ('Name', 'Author', 'DateModified', 'ProjectType'),
            selectmode = 'browse',
            show = 'headings'
        )

        self.heading("#0", text="")
        self.heading("Name", text="Project name", sort_by='name')
        self.heading("Author", text="Author", sort_by='name')
        self.heading("DateModified", text="Last modification", sort_by='date')
        self.heading("ProjectType", text="Type", sort_by='name')

        # Define column widths
        self.column("#0", width=10, stretch=False)
        self.column("Name", width=200, anchor='center', stretch=False)
        self.column("Author", width=100, anchor='center', stretch=False)
        self.column("DateModified", width=140, stretch=False)
        self.column("ProjectType", width=100, stretch=False)

        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.xview)
        self.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack the Treeview, scrollbars and frame
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame.pack(fill=tk.BOTH, expand=True)

        self.enable_selection()

    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_column_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
        return super().heading(column, **kwargs)

    def _sort_column(self, column, reverse, data_type, callback):
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_column_by_num(self, column, reverse):
        self._sort_column(column, reverse, int, self._sort_column_by_num)

    def _sort_column_by_name(self, column, reverse):
        self._sort_column(column, reverse, str, self._sort_column_by_name)

    def _sort_column_by_date(self, column, reverse):
        def _str_to_datetime(string):
            return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

        self._sort_column(column, reverse, _str_to_datetime, self._sort_column_by_date)

    def update_projects(self, data):
        self.delete(*self.get_children())
        for solution in data:
            if solution.name == '':
                continue
            project_type = 'Standard' if solution.project_type == 'StandardProject' else solution.project_type
            self.insert(
                '',
                tk.END,
                text=solution.uuid,  # Used on double-click event
                values=(
                    solution.name,
                    solution.author,
                    solution.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
                    project_type
                )
            )

    def disable_selection(self):
        self.config(selectmode="none")

    def enable_selection(self):
        self.config(selectmode="browse")
