ADDRESS_VERSION = '0.0.1'

# DB_URL = 'mysql://root:1@localhost:3306/eth_watcher?charset=utf8'
DB_URL = 'sqlite:///db.sqlite3'
DB_UPDATE_SCHEMA = True

RMQ_URL =  os.getenv('RMQ_URL', 'amqp://guest:guest@localhost')
RMQ_MASTER_QUEUE = 'pochta_watcher'
RMQ_REMOTE_QUEUE = 'pochta'
RMQ_EVENT_QUEUE = 'pochta_events'
RMQ_NAME = 'pochta_watcher'

