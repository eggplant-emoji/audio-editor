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
    """
    Represents an audiofile, all the data it contains.
    channels_number -- number of channels in the audiofile
    framerate -- number of samples per second
    frames_number -- total number of samples
    compression_type -- only 'NONE' is supported
    compression_name -- only 'not compressed' is supported
    """
    channels_number: int
    sample_width: int
    framerate: int
    frames_number: int
    compression_type: int
    compression_name: str

    framesdata: List[bytes]

    def __init__(self, params: tuple, framesdata: List[bytes]):
        """
        Creates new audiodata object
        params are the parameters returned by Wave_read.getparams()
        params = (
            channels_number, sample_width, framerate, frames_number, comp_type, comp_name
        )
        Represents an audiofile, all the data it contains.
        channels_number -- number of channels in the audiofile
        framerate -- number of samples per second
        frames_number -- total number of samples
        compression_type -- only 'NONE' is supported
        compression_name -- only 'not compressed' is supported
        """
        super().__init__()
        self.channels_number, self.sample_width, self.framerate, self.frames_number, self.compression_type, self.compression_name = params
        self.framesdata = framesdata

    def get_params(self, **overrides):
        """
        Returns parameters similarly to Wave_read.getparams() if overrides dict is empty
        Otherwise if a named parameter is received it overrides the parameter in the returned tuple
        Each keyword argument (key: value) overrides a returned parameter with name = key
        Keyword arguments:
          channels_number
          sample_width
          framerate
          frames_number
          compression_type
          compression_name
        """
        return (
            self.channels_number if 'channels_number' not in overrides else overrides['channels_number'],
            self.sample_width if 'sample_width' not in overrides else overrides['sample_width'],
            self.framerate if 'framerate' not in overrides else overrides['framerate'],
            self.frames_number if 'frames_number' not in overrides else overrides['frames_number'],
            self.compression_type if 'compression_type' not in overrides else overrides['compression_type'],
            self.compression_name if 'compression_name' not in overrides else overrides['compression_name']
        )

    def duration(self) -> float:
        """
        Returns a number of miliseconds the audiofile should last
        """
        return self.frames_number * 1000 // self.framerate

    def reverse(self):
        """
        Reverses an audiodata.
        Returns the audiodata that if played back sounds like the original
        """
        new_frames = self.framesdata[::-1]
        return AudioData(self.get_params(), new_frames)

    def join(self, audiodata):
        """
        Joins two audiodatas
        Accepts the second audiodata
        Returns a new audiodata that is essentially
        two audiodatas joined together like self + audiodata
        """
        new_framesdata = self.framesdata + audiodata.framesdata
        new_frames_number = self.frames_number + audiodata.frames_number
        new_params = self.get_params(frames_number=new_frames_number)
        return AudioData(new_params, new_framesdata)

    def crop(self, start_milis: int, end_milis: int):
        """
        Croppes the audiodata
        Returns a copy of audiodata that starts at start_milis miliseconds and ends at end_milis miliseconds
        relative to the original audiodata
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
        """
        Writes audio data to the file
        """
        file.setparams(self.get_params())
        file.writeframes(join_framesdata(self.framesdata))

    @staticmethod
    def read(file: wave.Wave_read):
        """
        Reads file and produces an audiodata from its data
        Returns that audiodata
        """
        params = file.getparams()
        frames_number = file.getnframes()
        frames = file.readframes(frames_number)
        characters_per_frame = len(frames) // frames_number
        framesdata = split_frames_into_sounds(frames, characters_per_frame)
        return AudioData(params, framesdata)

    def speed_up(self, coefficient: int):
        """
        Speeds up audiodata by a n times
        Accepts a whole number n
        Returns new audiodata
        """
        new_framerate = self.framerate * coefficient
        new_params = self.get_params(framerate=new_framerate)
        return AudioData(new_params, self.framesdata)

    def slow_down(self, coefficient: int):
        """
        Slows down audiodata by n times
        Accepts a whole number n
        Returns a new slowed down audiodata
        """
        new_framerate = self.framerate / coefficient
        new_params = self.get_params(framerate=new_framerate)
        return AudioData(new_params, self.framesdata)
    
    def bassboost(self):
        frames_channels = [split_frames_into_sounds(frame, self.sample_width) for frame in self.framesdata]
        def bassboost_each(bts):
            n = int.from_bytes(bts, byteorder='little')
            return int(n // 2).to_bytes(self.sample_width, byteorder='little')
        new_frame_channels = [[bassboost_each(channel) for channel in frame] for frame in frames_channels]
        return AudioData(self.get_params(), [b''.join(frame) for frame in new_frame_channels])
