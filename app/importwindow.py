from tkinter import Button, Frame, filedialog

from app.workspace import add_to_workspace
from core.track import WaveTrack


class ImportWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.frame = Frame(master)
        self.frame.pack()
        self.import_button = Button(self.frame, text='Выберете файл', command=self.on_file_select)
        self.import_button.pack()

    def on_file_select(self):
        filename = filedialog.askopenfilename(filetypes=[("Wave", ".wav")])
        track = WaveTrack(filename)
        add_to_workspace(track)
