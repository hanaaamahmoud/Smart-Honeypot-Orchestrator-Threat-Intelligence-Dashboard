import pytest

from analytics.session_replay import (
    SessionReplayDeferredError,
    build_session_replay,
)


def test_session_replay_is_deferred():
    with pytest.raises(SessionReplayDeferredError):
        build_session_replay([])
