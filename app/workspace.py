from typing import Dict, List

from core.track import Track, WaveTrack, JoinedTrack, TrackFragment, SlowedDownTrack, SpedUpTrack, ReversedTrack

workspace: Dict[str, 'Track'] = dict()

tracks_id: List['Track'] = []

on_update = None

def add_to_workspace(track: 'Track'):
    print("added " + get_track_name(track) + " to workspace")
    workspace[get_track_name(track)] = track
    tracks_id.append(track)
    if callable(on_update):
        on_update()

def get_track_id(track: 'Track') -> str:
    return "#" + str(tracks_id.index(track))

def get_track_name(track: 'Track'):
    track_id = len(workspace)
    prefix = "#" + str(track_id) + " "
    if isinstance(track, WaveTrack):
        return prefix + "Imported Track " + track.filename
    elif isinstance(track, JoinedTrack):
        first = get_track_id(track.sources[0])
        second = get_track_id(track.sources[1])
        return prefix + "Joined Track(" + first +", " + second + ")"
    elif isinstance(track, TrackFragment):
        first = get_track_id(track.sources[0])
        return prefix + "Fragment of Track(" + first + ")" + " from " + str(track.start) + " to " + str(track.end)
    elif isinstance(track, SpedUpTrack):
        first = get_track_id(track.sources[0])
        return prefix + "Sped Up Track(" + first +") by " + str(track.coefficient) + " times"
    elif isinstance(track, SlowedDownTrack):
        first = get_track_id(track.sources[0])
        return prefix + "Slowed Down Track(" + first +") by " + str(track.coefficient) + " times"
    elif isinstance(track, ReversedTrack):
        first = get_track_id(track.sources[0])
        return prefix + "Reversed Track(" + first + ")"
    else:
        return prefix + "Track"


def on_workspace_update(fn):
    global on_update
    on_update = fn