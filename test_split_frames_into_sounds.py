import unittest
from audiodata import split_frames_into_sounds


class TestSplitFramesIntoSounds(unittest.TestCase):
    def test_should_work_for_empty_string(self):
        frames = b''
        characters_per_frame = 2
        actual = split_frames_into_sounds(frames, characters_per_frame)
        expected = []
        assert actual == expected


    def test_should_work_for_short1_strings(self):
        frames = b'abcd'
        characters_per_frame = 2
        actual = split_frames_into_sounds(frames, characters_per_frame)
        expected = [b'ab', b'cd']
        assert actual == expected


    def test_should_work_for_short2_strings(self):
        frames = b'efghij'
        characters_per_frame = 3
        actual = split_frames_into_sounds(frames, characters_per_frame)
        expected = [b'efg', b'hij']
        assert actual == expected


    def test_should_work_for_short3_strings(self):
        frames = b'klm'
        characters_per_frame = 1
        actual = split_frames_into_sounds(frames, characters_per_frame)
        expected = [b'k', b'l', b'm']
        assert actual == expected


    def test_should_work_for_long1_strings(self):
        frames = b'abc' * 100
        characters_per_frame = 3
        actual = split_frames_into_sounds(frames, characters_per_frame)
        expected = [b'abc'] * 100
        assert actual == expected


    def test_should_work_for_long2_strings(self):
        frames = b'abcd' * 200
        characters_per_frame = 4
        actual = split_frames_into_sounds(frames, characters_per_frame)
        expected = [b'abcd'] * 200
        assert actual == expected


if __name__ == '__main__':
    unittest.main()