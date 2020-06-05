from tkinter import Button, Frame, filedialog

from pydub import AudioSegment

from app.workspace import add_to_workspace
from core.track import WaveTrack


class ImportWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.frame = Frame(master)
        self.frame.pack()
        self.import_button = Button(self.frame, text='Выберете файл .wav', command=self.on_file_select)
        self.import_button.pack()
        self.import_button_mp3 = Button(self.frame, text='Выберете файл .mp3', command=self.on_file_select_mp3)
        self.import_button_mp3.pack()

    def on_file_select(self):
        filename = filedialog.askopenfilename(filetypes=[("Wave", ".wav")])
        track = WaveTrack(filename)
        add_to_workspace(track)

    def on_file_select_mp3(self):
        filename = filedialog.askopenfilename(filetypes=[("MP3", ".mp3")])
        file = AudioSegment.from_mp3(filename)
        file.export("temp.wav", format="wav")
        track = WaveTrack("temp.wav")
        add_to_workspace(track)
