import tkinter as tk
from tkinter.filedialog import asksaveasfilename

from .symbols_treeview import SymbolsTreeview


class SymbolsDialog(tk.Toplevel):
    def __init__(self, master, solution, symbols, task_queue, **kwargs):
        super().__init__(master, **kwargs)
        self.solution = solution
        self.symbols = symbols
        self.task_queue = task_queue

        self.minsize(300, 100)
        self.title(f'Global data - {solution.name}')

        tk.Label(self, text=f'{len(self.symbols)} symbols found from project {solution.name}.').pack(pady=10)
        tk.Button(self, text='Export to file', command=self.export_symbols).pack()
        self.symbols_treeview = SymbolsTreeview(self)
        self.symbols_treeview.update_symbols(self.symbols)

        # Make dialog modal
        self.grab_set()

    def export_symbols(self):
        saveasfilename = asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('txt files', '.txt'), ('All files', '.*')]
        )
        if saveasfilename:
            command = 'save_symbols_to_file'
            cmd_args = (self.solution, self.symbols, saveasfilename)
            self.task_queue.put((command, cmd_args))
            self.destroy()
