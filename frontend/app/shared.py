from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import rpcgrid.aio as rpcg
from rpcgrid.aio.providers.rabbit import RabbitProvider
import os
import asyncio
app = Flask(__name__)

dburl = 'mysql+mysqldb://root@localhost:3306/spb_pochta'
RMQ_URL = 'amqp://guest:guest@localhost'
RMQ_MASTER_QUEUE = 'pochta_watcher'
RMQ_REMOTE_QUEUE = 'pochta'
RMQ_EVENT_QUEUE = 'pochta_events'
RMQ_NAME = 'pochta_watcher'


app.url_map.strict_slashes = False
_dir = os.path.dirname(os.path.abspath(__file__))
app.template_folder = os.path.join(_dir, "template")
app.static_folder = os.path.join(_dir, "static")
app.config['UPLOAD_FOLDER'] = os.path.join(_dir, "upload")

app.config['SQLALCHEMY_DATABASE_URI'] = dburl
db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

loop = asyncio.get_event_loop()

log.info(f'frontend microservice')

async def create_microservice(loop):
    provider = RabbitProvider(
        connection=RMQ_URL,
        master_queue=RMQ_REMOTE_QUEUE,
        remote_queue=RMQ_MASTER_QUEUE,
        loop=loop,
    )
    client = await rpcg.open(provider=provider, loop=loop)

    return client


def get_client():
    return loop.run_until_complete(create_microservice(loop))

client = get_client()


