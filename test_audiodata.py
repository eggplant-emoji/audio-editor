import unittest
from audiodata import AudioData

framesdata = [b'ab', b'cd', b'ef', b'gh', b'ij']
channels_number = 1
sample_width = 16
framerate = 60000
frames_number = 10
compression_type = 'NONE'
compression_name = 'NONE'

audiodata1 = AudioData((2, 2, 60000, 5, 'NONE', 'not compressed'), [b'abcd', b'efgh', b'ijkl', b'mnop', b'qrst'])
audiodata2 = AudioData((2, 2, 60000, 4, 'NONE', 'not compressed'), [b'qwer', b'tyui', b'op[]', b'asdf'])

one_frame_per_second = AudioData((2, 2, 1, 4, 'NONE', 'not compressed'), [b'qwer', b'tyui', b'op[]', b'asdf'])


class TestAudioData(unittest.TestCase):
    def test_duration_is_correctly_calculated(self):
        actual = one_frame_per_second.duration()
        assert actual == 4000
    
    def test_speedup_should_decrease_duration_by_2_times(self):
        error = 1500
        expected = audiodata1.duration() // 2
        actual = audiodata1.speed_up(2).duration()
        assert expected - error < actual < expected + error

    def test_speedup_should_decrease_duration_by_3_times(self):
        error = 1500
        expected = audiodata1.duration() // 3
        actual = audiodata1.speed_up(3).duration()
        assert expected - error < actual < expected + error

    def test_slowdown_should_increase_duration_by_2_times(self):
        error = 1500
        expected = audiodata1.duration() * 2
        actual = audiodata1.slow_down(2).duration()
        assert expected - error < actual < expected + error

    def test_slowdown_should_increase_duration_by_3_times(self):
        error = 1500
        expected = audiodata1.duration() * 3
        actual = audiodata1.slow_down(3).duration()
        assert expected - error < actual < expected + error
    
    def test_join_should_just_append_two_audiodatas_together(self):
        expected = [b'abcd', b'efgh', b'ijkl', b'mnop', b'qrst'] + [b'qwer', b'tyui', b'op[]', b'asdf']
        actual = audiodata1.join(audiodata2).framesdata
        assert expected == actual
    
    def test_join_should_add_durations(self):
        expected = audiodata1.duration() + audiodata2.duration()
        actual = audiodata1.join(audiodata2).duration()
        assert expected == actual
    
    def test_crop_should_work_on_audiodata_that_has_one_frame_per_second(self):
        expected = [b'tyui', b'op[]']
        actual = one_frame_per_second.crop(1000, 3000).framesdata
        assert expected == actual
    
    def test_reverse_reverses_framesdata_1(self):
        expected = [b'abcd', b'efgh', b'ijkl', b'mnop', b'qrst'][::-1]
        actual = audiodata1.reverse().framesdata
        assert expected == actual
    
    def test_reverse_if_applied_twice_does_not_change_data(self):
        expected = audiodata1
        actual = audiodata1.reverse().reverse()
        assert expected.framesdata == actual.framesdata


if __name__ == '__main__':
    unittest.main()

