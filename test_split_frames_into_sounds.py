from audiodata import split_frames_into_sounds


def test_should_work_for_empty_string():
    frames = b''
    characters_per_frame = 2
    actual = split_frames_into_sounds(frames, characters_per_frame)
    expected = []
    assert actual == expected


def test_should_work_for_short1_strings():
    frames = b'abcd'
    characters_per_frame = 2
    actual = split_frames_into_sounds(frames, characters_per_frame)
    expected = [b'ab', b'cd']
    assert actual == expected


def test_should_work_for_short2_strings():
    frames = b'efghij'
    characters_per_frame = 3
    actual = split_frames_into_sounds(frames, characters_per_frame)
    expected = [b'efg', b'hij']
    assert actual == expected


def test_should_work_for_short3_strings():
    frames = b'klm'
    characters_per_frame = 1
    actual = split_frames_into_sounds(frames, characters_per_frame)
    expected = [b'k', b'l', b'm']
    assert actual == expected


def test_should_work_for_long1_strings():
    frames = b'abc' * 100
    characters_per_frame = 3
    actual = split_frames_into_sounds(frames, characters_per_frame)
    expected = [b'abc'] * 100
    assert actual == expected


def test_should_work_for_long2_strings():
    frames = b'abcd' * 200
    characters_per_frame = 4
    actual = split_frames_into_sounds(frames, characters_per_frame)
    expected = [b'abcd'] * 200
    assert actual == expected

