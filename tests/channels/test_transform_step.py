import pytest

from tests import async_mock

from gloop.channels import transform_step


@pytest.mark.asyncio
async def test_transform(mocker):

    async def increment(x):
        return x + 1

    message = 1
    channel_in = mocker.Mock()
    channel_out = mocker.Mock()

    async_mock(
        channel_in.receive,
        message
    )

    async_mock(
        channel_out.send
    )

    result = await transform_step(
        increment,
        channel_in,
        channel_out
    )

    assert result is message + 1
    channel_in.receive.assert_called_once()
    channel_out.send.assert_called_once_with(result)


@pytest.mark.asyncio
async def test_transform_does_not_send_none(mocker):

    async def void(*args, **kwargs):
        pass

    channel_in = mocker.Mock()
    channel_out = mocker.Mock()

    async_mock(
        channel_in.receive
    )

    async_mock(
        channel_out.send
    )

    result = await transform_step(
        void,
        channel_in,
        channel_out
    )

    assert result is None
    channel_in.receive.assert_called_once()
    channel_out.send.assert_not_called()
