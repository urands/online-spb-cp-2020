from aiorequest import fetch_address
import time
import asyncio
import rpcgrid.aio as rpcg
from logger import get_logger
from provider import MicroserviceProvider
import sys
import os
import pandas as pd
log = get_logger(__name__)
dburl = 'mysql://root@localhost:3306/spb_pochta'

from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Files(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    name = fields.TextField()
    filename = fields.TextField()
    filename_norm = fields.TextField()
    status = fields.TextField()
    processed = fields.IntField()
    failed = fields.IntField()
    created_date = fields.DatetimeField(null=True)
    finish_date = fields.DatetimeField(null=True)

    class Meta:
        table = "files"

    def __str__(self):
        return self.name





@rpcg.register
async def procceed_address(*args):
    if not isinstance(args, tuple) and not isinstance(args, list):
        log.error('Input params must be array')
        raise Exception(f'Input params must be array. Not {type(args)}')

    return args


@rpcg.register
async def procceed_file(fileid):
    log.info('procceed_file')
    print('Proceed file', fileid)

    file = await Files.filter(id=int(fileid)).first()

    print(file)

    if file is None:
        return None


    fname, fext = os.path.splitext(file.filename)

    print(fname,fext)

    chunksize = 1000

    if fext == '.xlsx':
        try:
            df = pd.read_excel(file.filename, header=None )
        except Exception as e:
            log.error(e)
            return None
    if fext == '.csv':
        try:
            df = pd.read_csv(file.filename, sep="@",)
        except Exception as e:
            log.error(e)
            return None

    total = len(df)

    def chunk(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))
    f = open(fname + '_norm.csv', 'w')

    failed = 0
    processed = 0
    for df_chunk in chunk(df, 1000):
        strings = df_chunk[df_chunk.columns[0]].values
        result = await fetch_address(strings)

        for i,r in enumerate(result):
            if ('state' in r) and (r['state'] in ['301','303']):
                try:
                    rdata = [
                        r['state'],
                        r['addr']['inaddr'],
                        r['addr']['outaddr'],
                        r['addr']['addrType'],
                        r['addr']['direct'],
                        r['addr']['delivery'],
                        r['addr']['accuracy']
                    ]
                    #print(rdata)
                    f.write(';'.join(map(str,rdata)) + '\n')
                    processed+=1

                except Exception as e:
                    failed += 1
                    log.error(e)
            else:
                failed+=1
                rdata = [
                    r['state'],
                    strings[i],
                    '',
                    '',
                    '',
                    '',
                    ''
                ]
                f.write(';'.join(map(str, rdata)) + '\n')

        file.failed = failed
        file.processed = processed
        await file.save()
        #break
        #print()
    f.close()
    file.status = 'done'
    await file.save()

    print('Proceed file done')
    return { 'ok':'done'}




async def create_microservice(loop):
    while True:

        await Tortoise.init(db_url=dburl, modules={"models": ["app"]})
        #await Tortoise.generate_schemas()

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
