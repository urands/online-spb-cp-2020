import json

from rpcgrid.aio.providers.rabbit import RabbitProvider, aio_pika

from logger import get_logger
import settings

log = get_logger(__name__)


class MicroserviceProvider(RabbitProvider):
    _event_queue = None

    def __init__(self, loop):
        super(MicroserviceProvider, self).__init__(
            connection=settings.RMQ_URL,
            master_queue=settings.RMQ_MASTER_QUEUE,
            remote_queue=settings.RMQ_REMOTE_QUEUE,
            loop=loop,
        )
        self._event_queue = settings.RMQ_EVENT_QUEUE

    async def notify(self, event, message):
        msg = json.dumps(
            {'event': f'{settings.RMQ_NAME}:{event}', 'result': message}
        )
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=msg.encode()), routing_key=self._event_queue
        )
        log.info(f'Notify({self._event_queue}): {msg}')
