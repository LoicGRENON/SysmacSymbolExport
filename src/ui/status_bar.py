import tkinter as tk
from tkinter import font


class TruncatedLabel(tk.Label):
    def __init__(self, master, text="", **kwargs):
        super().__init__(master, **kwargs)
        self.full_text = text
        self.bind("<Configure>", self.update_text)

    def update_text(self, event=None):
        max_width = self.master.winfo_width()
        label_font = font.Font(font=self.cget("font"))

        text = self.full_text
        truncated_text = text

        if label_font.measure(text) <= max_width:
            self.config(text=text)
            return

        # Truncate until the width is ok
        for i in range(len(text), 0, -5):
            truncated = text[:i] + "..."
            if label_font.measure(truncated) <= max_width:
                truncated_text = truncated
                break

        self.config(text=truncated_text)


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
