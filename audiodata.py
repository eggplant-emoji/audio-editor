import wave
from typing import List


def split_frames_into_sounds(frames: bytes, characters_per_frame: int) -> List[bytes]:
    framesdata = []
    for i in range(0, len(frames), characters_per_frame):
        framesdata.append(frames[i:i + characters_per_frame])
    return framesdata


def join_framesdata(framesdata: List[bytes]) -> bytes:
    return b''.join(framesdata)


class AudioData:
    channels_number: int
    sample_width: int
    framerate: int
    frames_number: int
    compression_type: int
    compression_name: str

    framesdata: List[bytes]

    def __init__(self, params: tuple, framesdata: List[bytes]):
        super().__init__()
        self.channels_number, self.sample_width, self.framerate, self.frames_number, self.compression_type, self.compression_name = params
        self.framesdata = framesdata

    def get_params(self, **overrides):
        return (
            self.channels_number if 'channels_number' not in overrides else overrides['channels_number'],
            self.sample_width if 'sample_width' not in overrides else overrides['sample_width'],
            self.framerate if 'framerate' not in overrides else overrides['framerate'],
            self.frames_number if 'frames_number' not in overrides else overrides['frames_number'],
            self.compression_type if 'compression_type' not in overrides else overrides['compression_type'],
            self.compression_name if 'compression_name' not in overrides else overrides['compression_name']
        )

    def reverse(self):
        new_frames = self.framesdata[::-1]
        return AudioData(self.get_params(), new_frames)

    def join(self):
        """ Method for compound two audiofiles
        Accepts second file which will be join with first file
        Returns AudioData"""
        new_framesdata = self.framesdata + audiodata.framesdata
        new_frames_number = self.frames_number + audiodata.frames_number
        new_params = self.get_params(frames_number=new_frames_number)
        return AudioData(new_params, new_framesdata)

    def crop(self, start_milis: int, end_milis: int):
        """ Method for cropping an audiofile
        Accepts audiodata and start_milis, end_milis
        Creates a copy of audiodata that starts at [start_milis] miliseconds and ends at [end_milis] miliseconds
        """
        start_frame_index = self.frame_index_from_milis(start_milis)
        end_frame_index = self.frame_index_from_milis(end_milis)
        new_framesdata = self.framesdata[start_frame_index: end_frame_index]
        new_frames_number = len(self.framesdata[start_frame_index: end_frame_index])
        new_params = self.get_params(frames_number=new_frames_number)
        return AudioData(new_params, new_framesdata)

    def frame_index_from_milis(self, milis: int):
        return (self.framerate * milis) // 1000

    def write(self, file: wave.Wave_write) -> None:
        file.setparams(self.get_params())
        file.writeframes(join_framesdata(self.framesdata))

    @staticmethod
    def read(file: wave.Wave_read):
        params = file.getparams()
        frames_number = file.getnframes()
        frames = file.readframes(frames_number)
        characters_per_frame = len(frames) // frames_number
        framesdata = split_frames_into_sounds(frames, characters_per_frame)
        return AudioData(params, framesdata)

    def speed_up(self, coefficient: int):
        """ Method for speed-up an audiofile
        Accepts audiofile and coefficient (how many times you need to speed-up the track)

        Returns new audiofile """
        new_framerate = self.framerate * coefficient
        new_params = self.get_params(framerate=new_framerate)
        return AudioData(new_params, self.framesdata)

    def slow_down(self, coefficient: int):
        """ Method for slow down an audiofile
         Accepts audiofile and coefficient (how many times you need to slow down the track)
         Returns new audiodata"""

        new_framerate = self.framerate / coefficient
        new_params = self.get_params(framerate=new_framerate)
        return AudioData(new_params, self.framesdata)
