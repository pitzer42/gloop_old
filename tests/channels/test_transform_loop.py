import pytest

from tests import async_mock

from gloop.channels import transform_loop
from gloop.channels import BreakTransformLoop


@pytest.mark.asyncio
async def test_loop_stops_when_func_raises_break_transform_loop(mocker):

    async def increment_if_not_none(x):
        if x is None:
            raise BreakTransformLoop()
        return x + 1

    message = 1
    items_to_send = [message, None]
    channel_in = mocker.Mock()
    channel_out = mocker.Mock()

    async def next_item():
        return items_to_send.pop(0)

    channel_in.receive = next_item
    async_mock(channel_out.send)

    await transform_loop(
        increment_if_not_none,
        channel_in,
        channel_out
    )

    assert len(items_to_send) == 0
    channel_out.send.assert_called_once_with(message + 1)
