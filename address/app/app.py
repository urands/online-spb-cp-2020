from aiorequest import fetch_address
import time
import asyncio
import rpcgrid.aio as rpcg
from logger import get_logger
from provider import MicroserviceProvider
import sys

log = get_logger(__name__)

@rpcg.register
async def procceed_address(*args):
    if not isinstance(args, tuple) and not isinstance(args, list):
        log.error('Input params must be array')
        raise Exception(f'Input params must be array. Not {type(args)}')

    return args

async def create_microservice(loop):
    while True:
        try:
            return await rpcg.create(
                provider=MicroserviceProvider(loop), loop=loop
            )
        except ConnectionError as rmq_err:
            log.warning(rmq_err)
        await asyncio.sleep(10)


def main(loop):
    server = None
    try:
        log.info('Initialize ...')
        log.info('Initialize rabbit...')
        server = loop.run_until_complete(create_microservice(loop))
        log.info('Initialize completed!')
        loop.run_until_complete(server.run())
        # loop.run_forever()
    except KeyboardInterrupt:
        log.info('Microservice stopped by user . . .')
        if server is not None:
            loop.run_until_complete(server.close())


def sigterm_handler(signum, frame):
    log.info('Terminate application')
    sys.exit(1)


if __name__ == '__main__':
    log.info(f'pochta addess microservice {0.1}')
    main(asyncio.get_event_loop())
