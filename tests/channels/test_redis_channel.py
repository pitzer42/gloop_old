import asyncio
import pytest
import docker

from gloop.channels import Channel
from gloop.channels.redis import RedisChannel


@pytest.fixture(scope='module')
def redis_channel_params():

    host_port = 6380
    channel_name = 'test_channel'
    redis_address = f'redis://localhost:{host_port}'
    docker_params = dict(
        image='redis',
        ports={6379: host_port},
        name='test_redis',
        detach=True
    )

    docker_cli = docker.from_env()
    container = docker_cli.containers.run(**docker_params)

    yield channel_name, redis_address

    container.stop()
    container.remove()


@pytest.fixture
def channel_factory(redis_channel_params):
    channel_name, address = redis_channel_params

    def factory():
        return RedisChannel(
            channel_name,
            address=address
        )

    return factory


@pytest.fixture
def channel(channel_factory) -> Channel:
    return channel_factory()


@pytest.mark.asyncio
async def test_must_be_opened_before_used(channel: Channel):
    with pytest.raises(Exception):
        await channel.send('foo')


@pytest.mark.asyncio
async def test_cannot_be_used_after_closed(channel: Channel):
    await channel.open()
    await channel.send('foo')
    await channel.close()
    with pytest.raises(Exception):
        await channel.send('foo')


@pytest.mark.asyncio
async def test_multiple_consumers(channel_factory):

    n_consumers = 2
    ready_consumers = [0]
    expected_message = b'foo'

    async def consumer():
        consumer_channel = channel_factory()
        await consumer_channel.open()
        ready_consumers[0] += 1
        message = await consumer_channel.receive()
        assert message == expected_message

    async def producer():
        producer_channel = channel_factory()
        await producer_channel.open()
        while ready_consumers[0] < n_consumers:
            await asyncio.sleep(1)
        await producer_channel.send(expected_message)

    await asyncio.gather(
        producer(),
        *[consumer() for i in range(n_consumers)]
    )
