import logging
import queue
import tkinter as tk
from tkinter.filedialog import askdirectory, asksaveasfilename
from tkinter import messagebox, ttk

from src import __version__
from ui import ProjectsTreeview
from ui import StatusBar
from ui import SymbolsDialog
from ui import WorkerThread


logger = logging.getLogger(__name__)


def ask_for_overwrite(filepath):
    """If file exists, prompt for overwrite or to select another filepath"""
    if filepath.exists():
        overwrite = messagebox.askquestion(
            "Overwrite existing target file",
            f"The selected target file {filepath} already exists on your filesystem.\n\n"
            f"Press 'YES' if you wish to overwrite it or 'NO' to select another filename",
            type=messagebox.YESNO)

        if overwrite == messagebox.NO:
            return asksaveasfilename(filetypes=[('CSV files', '.csv'), ('All files', '.*')])
    return filepath


class AppUi(tk.Tk):
    def __init__(self):
        super(AppUi, self).__init__()

        # Queues
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

        # Worker to handle time-consuming tasks in order to keep the UI responsive
        self.worker = WorkerThread(self.task_queue, self.result_queue)
        self.worker.start()

        # UI
        self.title(f"Sysmac global variables export - V{__version__}")
        self.main_frm = ttk.Frame(self, padding=10)
        self.symbols_dialog = None

        self._add_labels()
        self._add_path_frame()

        self.projects_tv = ProjectsTreeview(self.main_frm)
        self.projects_tv.bind('<<TreeviewSelect>>', self.on_project_tv_select)
        self.projects_tv.bind('<Double-1>', self.on_project_tv_double_click)

        self.status_bar = StatusBar(self.main_frm)

        self.main_frm.pack(fill=tk.BOTH, expand=True)

        self.__check_result_queue()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Schedule work for WorkerThread
        command = 'get_solutions'
        cmd_args = (self.path_entry_var.get(),)
        self.task_queue.put((command, cmd_args))

        self.status_bar.set_text(f'Looking for projects in {cmd_args}. Please wait ...')

    def _add_path_frame(self):
        self.path_frm = ttk.Frame(self.main_frm)
        self.path_entry_label = ttk.Label(self.path_frm, text="Solution path: ")
        self.path_entry_var = tk.StringVar(value="C:\\OMRON\\Data\\Solution")
        self.path_entry = tk.Entry(self.path_frm, width=40, state='disabled', textvariable=self.path_entry_var)
        self.path_button = tk.Button(self.path_frm, text='Browse', command=self._path_button_cb)
        self.path_entry_label.grid(row=0, column=0)
        self.path_entry.grid(row=0, column=1)
        self.path_button.grid(row=0, column=2, padx=5)
        self.path_frm.pack(fill=tk.BOTH, pady=10)

    def _path_button_cb(self):
        input_path = tk.filedialog.askdirectory(
            title='Please select a directory',
            initialdir=self.path_entry_var.get()
        )
        if input_path:
            self.path_entry_var.set(input_path)

            # Schedule work for WorkerThread
            command = 'get_solutions'
            cmd_args = (self.path_entry_var.get(),)
            self.task_queue.put((command, cmd_args))

            self.status_bar.set_text(f'Looking for projects in {cmd_args}. Please wait ...')

    def __check_result_queue(self):
        try:
            while True:
                message, data = self.result_queue.get_nowait()
                if message == 'get_solutions':
                    self.projects_tv.update_projects(data)
                    self.status_bar.set_text(f'{len(data)} projects found')
                elif message == 'get_vars_from_solution':
                    solution = data['solution']
                    symbols = data['symbols']
                    self.status_bar.set_text(f'{len(symbols)} symbols found from project {solution.name}')
                    self.projects_tv.enable_selection()
                    self.symbols_dialog = SymbolsDialog(self, solution, symbols, self.task_queue)
                elif message == 'save_symbols_to_file':
                    solution = data['solution']
                    filename = data['filename']
                    self.status_bar.set_text(f'Symbols from project {solution.name} saved to {filename}')

        except queue.Empty:
            pass
        # Schedule another call after 100ms
        self.after(100, self.__check_result_queue)

    def _add_labels(self):
        label = ttk.Label(
            self.main_frm,
            text="This application allows you to export the global variables from a OMRON Sysmac® Studio project.\n"
                 "Double-click on the line corresponding to the project "
                 "from which you want to export them.\n\n"
                 "NB: Only the variables published on the network can be exported (Network Publish=Publish only)."
        )
        label.pack(side=tk.TOP, fill=tk.BOTH)

    def on_closing(self):
        self.task_queue.put(("stop", None))
        if self.symbols_dialog:
            self.symbols_dialog.destroy()
        self.destroy()

    def on_project_tv_select(self, event):
        tv_selection = self.projects_tv.selection()
        if not tv_selection:
            return

        selected_item_values = self.projects_tv.item(tv_selection[0], "values")
        project_name = selected_item_values[0]
        project_uuid = self.projects_tv.item(tv_selection[0], "text")
        self.status_bar.set_text(f'{project_name}: {project_uuid}')

    def on_project_tv_double_click(self, event):
        tv_selection = self.projects_tv.selection()
        if not tv_selection:
            return

        selected_item_values = self.projects_tv.item(tv_selection[0], "values")
        project_name = selected_item_values[0]
        self.status_bar.set_text(f'Retrieving variables for project {project_name}. Please wait ...')

        # Schedule work for WorkerThread
        solutions_path = self.path_entry_var.get()
        project_uuid = self.projects_tv.item(tv_selection[0], "text")
        command = 'get_vars_from_solution'
        cmd_args = (solutions_path, project_uuid)
        self.task_queue.put((command, cmd_args))
        self.projects_tv.disable_selection()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main_app = AppUi()
    main_app.mainloop()
