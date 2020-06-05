from tkinter import Frame, Button, Label, StringVar, OptionMenu
from typing import List, Dict
from tkinter import ttk

from workspace import workspace, add_to_workspace
from track import Track


class ActionWindow(Frame):
    def __init__(self, master, file_number: int):
        super().__init__(master)
        self.file_number = file_number
        self.frame = Frame(self.master)
        self.frame.pack()
        self.title = Label(self.frame, text='Select the files')
        self.title.pack()
        self.selected_file_names = []
        for i in range(self.file_number):
            selected_file = StringVar(master)
            selected_file.set("-")
            available_tracks = ["-"] + list(workspace.keys())
            file_selector = OptionMenu(self.frame, selected_file, *available_tracks, command=self.on_file_select(i))
            file_selector.pack()
            self.selected_file_names.append(selected_file)
        self.body = Frame(self.frame)
        self.body.pack()
        self.error_message = Label(self, text="Select the files")
        self.submit = Button(self.frame, text='подтвердить', state='disabled', command=self.on_submit)
        self.submit.pack()
        self.selected_tracks = [None] * file_number

    def get_file_dropdown(self, index):
        default = StringVar("-")
        return OptionMenu(self.frame, default, workspace.keys(), command=self.on_file_select(index))

    def on_file_select(self, file_index):
        def listener(_):
            selected_file_name = self.selected_file_names[file_index].get()
            if selected_file_name in workspace:
                self.selected_tracks[file_index] = workspace[selected_file_name]
            self.on_selection_changed()

        return listener

    def on_selection_changed(self):
        if None not in self.selected_tracks:
            self.on_all_files_selected()
        else:
            self.on_some_files_not_selected()

    def on_all_files_selected(self):
        self.hide_error()

    def on_some_files_not_selected(self):
        self.show_error("All files need to be selected")

    def show_error(self, text):
        self.error_message['text'] = text
        self.submit['state'] = 'disabled'

    def hide_error(self):
        self.error_message['text'] = ''
        self.submit['state'] = 'normal'

    def on_submit(self):
        result = self.calculate_result()
        add_to_workspace(result)

    def calculate_result(self) -> Track:
        pass
