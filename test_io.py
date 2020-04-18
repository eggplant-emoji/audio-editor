import unittest
import wave
from audiodata import AudioData

test_file_input = wave.open('test_input.wav', 'rb')
test_file_output = wave.open('test_output.wav', 'wb')


class TestReadWrite(unittest.TestCase):   
    def test_reads_writes_without_errors(self):
        r = AudioData.read(test_file_input)
        r.write(test_file_output)


if __name__ == '__main__':
    unittest.main()
