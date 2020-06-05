from tkinter import Label, Entry, Spinbox

from app.actionwindow import ActionWindow
from core.track import Track, SpedUpTrack, SlowedDownTrack


class SpeedWindow(ActionWindow):
    def __init__(self, master):
        super().__init__(master, 1)
        self.edit = Spinbox(self.body, from_=2, to=10)
        self.edit.pack()

    def change_speed(self, track: 'Track', coef: int) -> Track:
        pass

    def calculate_result(self) -> Track:
        track = self.selected_tracks[0]
        return self.change_speed(track, int(self.edit.get()))


class SpeedUpWindow(SpeedWindow):
    def change_speed(self, track: 'Track', coef: int) -> Track:
        return SpedUpTrack(track, coef)


class SlowDownWindow(SpeedWindow):
    def change_speed(self, track: 'Track', coef: int) -> Track:
        return SlowedDownTrack(track, coef)
