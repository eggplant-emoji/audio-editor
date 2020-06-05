from actionwindow import ActionWindow
from track import Track, ReversedTrack


class ReverseWindow(ActionWindow):
    def __init__(self, master):
        super().__init__(master, 1)

    def calculate_result(self) -> Track:
        track = self.selected_tracks[0]
        return ReversedTrack(track)
