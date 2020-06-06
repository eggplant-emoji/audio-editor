from track import WaveTrack, ReversedTrack, JoinedTrack, TrackFragment, SpedUpTrack, SlowedDownTrack

original_track: 'WaveTrack' = WaveTrack("a.wav")

# Reversed

reversed_track: 'ReversedTrack' = ReversedTrack(original_track)


def test_reversed_track_has_the_same_frames_number():
    assert reversed_track.metadata.frames_number == original_track.metadata.frames_number


def test_reversed_track_is_the_original_but_reversed():
    for i in range(original_track.metadata.frames_number):
        assert original_track[i] == reversed_track[original_track.metadata.frames_number - 1 - i]


# Joined

joined_track = JoinedTrack(original_track, original_track)


def test_joined_track_has_twice_frames_number():
    assert joined_track.metadata.frames_number == original_track.metadata.frames_number + original_track.metadata.frames_number


def test_joined_track_should_be_original_track_joined_twice():
    for i in range(original_track.metadata.frames_number):
        assert original_track[i] == joined_track[i % original_track.metadata.frames_number]


# Cropped

cropped_track = TrackFragment(original_track, 0, 100)


def test_cropped_track_has_100_frames():
    assert cropped_track.metadata.frames_number == 100


def test_cropped_track_should_be_cropped():
    for i in range(100):
        assert cropped_track[i] == original_track[i]


# SpeedUp

spedup_track = SpedUpTrack(original_track, 2)


def test_spedup_track_has_half_frames_number():
    assert spedup_track.metadata.frames_number == original_track.metadata.frames_number // 2


def test_spedup_track_has_the_same_frames():
    for i in range(spedup_track.metadata.frames_number):
        assert spedup_track[i] == original_track[2 * i]


# Slowed Down Track

slowed_down_track = SlowedDownTrack(original_track, 2)


def test_slowed_track_has_twice_number_of_frames():
    assert slowed_down_track.metadata.frames_number == original_track.metadata.frames_number * 2


def test_slowed_track_has_same_frames():
    for i in range(original_track.metadata.frames_number):
        assert original_track[i] == slowed_down_track[2 * i]
