import wave

from audiodata import AudioData

test_file_input = wave.open('a.wav', 'rb')
test_file_output = wave.open('test_output.wav', 'wb')


def test_reads_writes_without_errors():
    r = AudioData.read(test_file_input)
    r.write(test_file_output)
