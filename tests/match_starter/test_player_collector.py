import pytest

from gloop.match_starter.player_collector import collect_players


@pytest.fixture
def match_size():
    return 2


@pytest.fixture
def collector(match_size):
    return collect_players(
        list(),
        match_size
    )


@pytest.fixture
def players(match_size):
    return [str(i) for i in range(match_size)]


@pytest.mark.asyncio
async def test_all_players_in_match(collector, players):
    result = None

    for i in players:
        result = await collector(i)

    for i in players:
        assert i in result

