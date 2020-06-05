import wave

from core.utils import chunked


class Frame:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def from_raw(raw: bytes, sample_width: int) -> 'Frame':
        data = chunked(raw, sample_width)
        return Frame(data)

    def join(self) -> bytes:
        return b''.join(self.data)


class Metadata:
    def __init__(self, channels_number, sample_width, frame_rate, frames_number, compression_type, compression_name):
        self.channels_number = channels_number
        self.sample_width = sample_width
        self.frame_rate = frame_rate
        self.frames_number = frames_number
        self.compression_type = compression_type
        self.compression_name = compression_name

    def as_tuple(self) -> tuple:
        return (self.channels_number, self.sample_width, self.frame_rate, self.frames_number, self.compression_type,
                self.compression_name)

    def changed(self, **overrides) -> 'Metadata':
        return Metadata(
            self.channels_number if 'channels_number' not in overrides else overrides['channels_number'],
            self.sample_width if 'sample_width' not in overrides else overrides['sample_width'],
            self.frame_rate if 'frame_rate' not in overrides else overrides['framerate'],
            self.frames_number if 'frames_number' not in overrides else overrides['frames_number'],
            self.compression_type if 'compression_type' not in overrides else overrides['compression_type'],
            self.compression_name if 'compression_name' not in overrides else overrides['compression_name']
        )


class Track:
    def __init__(self):
        self.metadata = None

    def __getitem__(self, i) -> 'Frame':
        pass


class SoftOperationResult(Track):
    def __init__(self, *tracks: 'Track'):
        super().__init__()
        self.sources = tracks


class JoinedTrack(SoftOperationResult):
    def __init__(self, track1: Track, track2: Track):
        super().__init__(track1, track2)
        self.metadata = track1.metadata.changed(
            frames_number=track1.metadata.frames_number + track2.metadata.frames_number
        )

    def __getitem__(self, i):
        track1 = self.sources[0]
        track2 = self.sources[1]
        if i < track1.metadata.frames_number:
            return track1[i]
        else:
            return track2[i - track1.metadata.frames_number]


class ReversedTrack(SoftOperationResult):
    def __init__(self, track: Track):
        super().__init__(track)
        self.metadata = track.metadata

    def __getitem__(self, i):
        original_track = self.sources[0]
        return original_track[original_track.metadata.frames_number - 1 - i]


class TrackFragment(SoftOperationResult):
    def __init__(self, track, start, end):
        """
        End is not inclusive
        """
        super().__init__(track)
        self.start = start
        self.end = end
        self.metadata = track.metadata.changed(frames_number=end - start)

    def __getitem__(self, i):
        original_track = self.sources[0]
        return original_track[i + self.start]


class SpedUpTrack(SoftOperationResult):
    def __init__(self, track: 'Track', coefficient: int):
        super().__init__(track)
        self.coefficient = coefficient
        self.metadata = track.metadata.changed(frames_number=track.metadata.frames_number // coefficient)

    def __getitem__(self, i):
        original_track = self.sources[0]
        return original_track[i * self.coefficient]


class SlowedDownTrack(SoftOperationResult):
    def __init__(self, track: 'Track', coefficient: int):
        super().__init__(track)
        self.coefficient = coefficient
        self.metadata = track.metadata.changed(frames_number=track.metadata.frames_number * self.coefficient)

    def __getitem__(self, i):
        original_track = self.sources[0]
        return original_track[i // self.coefficient]


class WaveTrack(Track):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.file = wave.open(filename, 'rb')
        self.metadata = Metadata(*self.file.getparams())

    def __getitem__(self, item):
        self.file.setpos(item)
        raw_frame = self.file.readframes(1)
        frame = Frame.from_raw(raw_frame, self.metadata.sample_width)
        return frame


def write_track(track: 'Track', filename: str):
    frames = b''.join(track[i].join() for i in range(track.metadata.frames_number))
    file = wave.open(filename, 'wb')
    file.setparams(track.metadata.as_tuple())
    file.writeframes(frames)


t = WaveTrack('../a.wav')
c = TrackFragment(t, 100000, 400000)
write_track(c, '../cropped.wav')
