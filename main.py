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


def read_audiodata(file: wave.Wave_read) -> AudioData:
    params = file.getparams()
    frames_number = file.getnframes()
    frames = file.readframes(frames_number)
    characters_per_frame = len(frames) // frames_number
    framesdata = split_frames_into_sounds(frames, characters_per_frame)
    audiodata = AudioData(params, framesdata)
    return audiodata


def write_audiodata(file: wave.Wave_write, audiodata: AudioData) -> None:
    params = (audiodata.channels_number, audiodata.sample_width, audiodata.framerate, audiodata.frames_number,
              audiodata.compression_type, audiodata.compression_name)
    file.setparams(params)
    file.writeframes(join_framesdata(audiodata.framesdata))


def crop2_audiodata(audiodata: AudioData):
    frames_number = audiodata.frames_number
    frames = audiodata.framesdata
    newframes = frames[:frames_number // 2]
    channels_number = audiodata.channels_number
    sample_width = audiodata.sample_width
    framerate = audiodata.framerate
    newframes_number = frames_number // 2
    compression_type = audiodata.compression_type
    compression_name = audiodata.compression_name
    newparams = (channels_number, sample_width, framerate, newframes_number, compression_type, compression_name)
    newAudiodata = AudioData(newparams, newframes)
    return newAudiodata


def reverse_audiodata(audiodata: AudioData) -> AudioData:
    newframes = audiodata.framesdata[::-1]
    params = (audiodata.channels_number, audiodata.sample_width, audiodata.framerate, audiodata.frames_number,
              audiodata.compression_type, audiodata.compression_name)
    newaudiodata = AudioData(params, newframes)
    return newaudiodata


def join_audiodata(audiodata1: AudioData, audiodata2: AudioData) -> AudioData:
    framesdata1 = audiodata1.framesdata
    framesdata2 = audiodata2.framesdata
    newframesdata = framesdata1 + framesdata2
    frames_number1 = audiodata1.frames_number
    frames_number2 = audiodata2.frames_number
    newframes_number = frames_number1 + frames_number2
    newparams = (audiodata1.channels_number, audiodata1.sample_width, audiodata1.framerate, newframes_number,
              audiodata1.compression_type, audiodata1.compression_name)
    newAudiodata = AudioData(newparams, newframesdata)
    return newAudiodata


a = wave.open('a.wav', 'rb')
b = wave.open('b.wav', 'wb')
audiodata = read_audiodata(a)
write_audiodata(b, audiodata)

