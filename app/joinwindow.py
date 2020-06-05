from app.actionwindow import ActionWindow
from core.track import Track, JoinedTrack


class JoinWindow(ActionWindow):
    def __init__(self, master):
        super().__init__(master, 2)

    def calculate_result(self) -> Track:
        track1 = self.selected_tracks[0]
        track2 = self.selected_tracks[1]
        return JoinedTrack(track1, track2)
