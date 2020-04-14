import wave
class AudioData:
    channels_number: int
    sample_width: int
    framerate: int
    frames_number: int
    compression_type: int
    compression_name: str

    frames: bytes

    def __init__(self, params: tuple, frames: bytes):
        super().__init__()
        self.channels_number, self.sample_width, self.framerate, self.frames_number, self.compression_type, self.compression_name = params
        self.frames = frames

def read_audiodata(file: wave.Wave_read):
    params = file.getparams()
    frames_number = file.getnframes()
    frames = file.readframes(frames_number)
    audiodata = AudioData(params,frames)
    return audiodata

def write_audiodata(file: wave.Wave_write, audiodata: AudioData):
    params = (audiodata.channels_number, audiodata.sample_width, audiodata.framerate, audiodata.frames_number, audiodata.compression_type, audiodata.compression_name)
    file.setparams(params)
    file.writeframes(audiodata.frames)

def crop2_audiodata(audiodata: AudioData):
    frames_number = audiodata.frames_number
    frames = audiodata.frames
    newframes= frames[:frames_number // 2]
    channels_number = audiodata.channels_number
    sample_width = audiodata.sample_width
    framerate = audiodata.framerate
    newframes_number = frames_number // 2
    compression_type = audiodata.compression_type
    compression_name = audiodata.compression_name
    newparams = (channels_number, sample_width, framerate, newframes_number, compression_type, compression_name)
    newAudiodata = AudioData(newparams, newframes)
    return newAudiodata


a = wave.open('a.wav', 'rb')
b = wave.open('b.wav', 'wb')

audiodata = read_audiodata(a)
newaudiodata = crop2_audiodata(audiodata)
write_audiodata(b, newaudiodata)


