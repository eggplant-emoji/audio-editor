from tkinter import Scale, HORIZONTAL

from app.actionwindow import ActionWindow
from core.track import TrackFragment, Track


class FragmentWindow(ActionWindow):
    def __init__(self, master):
        super().__init__(master, 1)
        self.scale1 = Scale(self.body, from_=0, to=1, state='disabled', orient=HORIZONTAL,
                            command=self.check_correct_scales)
        self.scale1.pack()
        self.scale2 = Scale(self.body, from_=0, to=1, state='disabled', orient=HORIZONTAL,
                            command=self.check_correct_scales)
        self.scale2.pack()

    def check_correct_scales(self, _):
        val1 = self.scale1.get()
        val2 = self.scale2.get()
        if val1 < val2:
            self.hide_error()
        else:
            self.show_error("Wrong start and end")

    def on_all_files_selected(self):
        track = self.selected_tracks[0]
        num_frames = track.metadata.frames_number
        self.scale1['from'] = 0
        self.scale1['to'] = num_frames
        self.scale2['from'] = 0
        self.scale2['to'] = num_frames
        self.scale1['state'] = 'normal'
        self.scale2['state'] = 'normal'

    def calculate_result(self) -> Track:
        val1 = self.scale1.get()
        val2 = self.scale2.get()
        return TrackFragment(self.selected_tracks[0], val1, val2)