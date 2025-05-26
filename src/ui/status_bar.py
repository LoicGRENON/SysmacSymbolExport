import tkinter as tk

from .truncated_label import TruncatedLabel


class StatusBar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = TruncatedLabel(self)
        self.label.pack(side=tk.LEFT)
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def set_text(self, value: str):
        self.label.full_text = value
        self.label.config(text=value)

    def clear_text(self):
        self.label.config(text='')
