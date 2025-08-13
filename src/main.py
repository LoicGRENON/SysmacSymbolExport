import logging
import queue
import tkinter as tk
from tkinter.messagebox import askyesno, showinfo
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename
from tkinter import ttk

from settings_manager import SettingsManager
from src import __version__, APP_NAME
from ui import ProjectsTreeview
from ui import StatusBar
from ui import SymbolsDialog
from ui import WorkerThread
from utils import resource_path


logger = logging.getLogger(__name__)


class AppUi(tk.Tk):
    def __init__(self):
        super(AppUi, self).__init__()

        self.symbols_dialog = None

        # Queues
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

        # Worker to handle time-consuming tasks in order to keep the UI responsive
        self.worker = WorkerThread(self.task_queue, self.result_queue)
        self.worker.start()

        self.settings = SettingsManager()

        # UI
        if "__compiled__" in globals():
            iconbitmap = resource_path('SysmacSymbolExport.ico')
        else:
            iconbitmap = '../SysmacSymbolExport.ico'
        self.iconbitmap(iconbitmap)
        self.title(f"Sysmac global variables export - V{__version__}")
        self.minsize(500, 200)
        self.add_menu_bar()

        main_frm = ttk.Frame(self, padding=10)
        content_frame = ttk.Frame(main_frm)
        self.status_bar = StatusBar(main_frm)

        label = ttk.Label(
            content_frame,
            text="Double-click on the line corresponding to the project from which you want to export them.\n"
                 "NB: Only the variables published on the network can be exported (Network Publish=Publish only)."
        )
        label.pack(side=tk.TOP, fill=tk.BOTH)
        self._add_path_frame(content_frame)

        self.projects_tv = ProjectsTreeview(content_frame)
        self.projects_tv.bind('<<TreeviewSelect>>', self.on_project_tv_select)
        self.projects_tv.bind('<Double-1>', self.on_project_tv_double_click)

        self.load_from_settings()

        content_frame.pack(fill=tk.BOTH, expand=True)
        main_frm.pack(fill=tk.BOTH, expand=True)

        self.__check_result_queue()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_menu_bar(self):
        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Import settings", command=self.do_import_settings)
        menu_file.add_command(label="Export settings", command=self.do_export_settings)
        menu_file.add_command(label="Restore default settings", command=self.do_restore_settings)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.on_closing)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About", command=self.do_about)
        menu_bar.add_cascade(label="Help", menu=menu_help)

        self.config(menu=menu_bar)

    def _add_path_frame(self, master):
        self.path_frm = ttk.Frame(master)
        self.path_entry_label = ttk.Label(self.path_frm, text="Solution path: ")
        self.path_entry_var = tk.StringVar()
        self.path_entry = tk.Entry(self.path_frm, width=40, state='disabled', textvariable=self.path_entry_var)
        self.path_button = tk.Button(self.path_frm, text='Browse', command=self._path_button_cb)
        self.path_entry_label.grid(row=0, column=0)
        self.path_entry.grid(row=0, column=1)
        self.path_button.grid(row=0, column=2, padx=5)
        self.path_frm.pack(fill=tk.BOTH, pady=10)

    def do_about(self):
        desc = "This application allows you to export global variables from OMRON Sysmac Studio projects."
        content = (f"{APP_NAME}\n"
                   f"\n"
                   f"{desc}\n"
                   f"\n"
                   f"Version {__version__}\n"
                   f"Copyright © 2025 GRENON Loïc\n"
                   f"\n"
                   f"Follow on GitHub: https://github.com/LoicGRENON/SysmacSymbolExport")
        showinfo(f"About {APP_NAME}", content)

    def do_import_settings(self):
        askopenfile_title = "Please choose the file you want to import the settings from"
        askopenfile_filetypes = [('ini files', '.ini'), ('All files', '.*')]
        import_filepath = askopenfilename(title=askopenfile_title, filetypes=askopenfile_filetypes)
        if import_filepath:
            self.settings.import_from(import_filepath)
            self.load_from_settings()

    def do_export_settings(self):
        asksavefile_title = "Please choose a filename to save the settings on"
        asksavefile_filetypes = [('ini files', '.ini'), ('All files', '.*')]
        settings_filepath = asksaveasfilename(title=asksavefile_title,
                                              filetypes=asksavefile_filetypes,
                                              defaultextension='.ini')
        if settings_filepath:
            self.settings.export_to(settings_filepath)

    def do_restore_settings(self):
        title = 'Restore default settings'
        msg = 'Are you sure you want to restore the settings to their default values ?'
        answer = askyesno(title, msg, default='no')
        if answer == 'yes':
            self.settings.restore_default()
            self.load_from_settings()

    def load_from_settings(self):
        self.path_entry_var.set(self.settings.get('general', 'solution_path'))

        # Schedule work for WorkerThread
        command = 'get_solutions'
        cmd_args = (self.path_entry_var.get(),)
        self.task_queue.put((command, cmd_args))
        self.status_bar.set_text(f'Looking for projects in {cmd_args}. Please wait ...')

    def _path_button_cb(self):
        input_path = tk.filedialog.askdirectory(
            title='Please select a directory',
            initialdir=self.path_entry_var.get()
        )
        if input_path:
            self.path_entry_var.set(input_path)

            # Schedule work for WorkerThread
            command = 'get_solutions'
            cmd_args = (input_path,)
            self.task_queue.put((command, cmd_args))

            self.status_bar.set_text(f'Looking for projects in {input_path}. Please wait ...')
            self.settings.set('general', 'solution_path', input_path)
            self.settings.save()

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
