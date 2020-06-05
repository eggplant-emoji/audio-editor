from tkinter import Frame, Label, Entry, Button

from actionwindow import ActionWindow
from track import write_track


class ExportWindow(ActionWindow):
    def __init__(self, master):
        super().__init__(master, 1)
        self.entry = Entry(self.body)
        self.entry.pack()

    def on_submit(self):
        filename = self.entry.get()
        write_track(self.selected_tracks[0], "../" + filename)
