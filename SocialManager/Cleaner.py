import logging
from Lib.RssPost import *
from Lib.MyQueue import *
from Lib.MainConf import *

LOG_FILE_PATH = 'log_cleaner.txt'

#################
# Setup logging #
#################
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
# create file handler which logs warning or higher
fh = logging.FileHandler(LOG_FILE_PATH)
fh.setLevel(logging.WARNING)
# create console handler with a lower log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

force_mode = raw_input('Force mode?: (0 = no, 1 = yes) [0]\n')
if force_mode == '0' or force_mode == '':
	force_mode = False
elif force_mode == '1':
	force_mode = True
else:
	print 'Wrong mode. Please enter 0 or 1.'
	exit()

days_ago = raw_input('Clean the data which are [?] days ago: [7]\n')
if days_ago == '':
	days_ago = 7
days_ago = int(days_ago)
if days_ago <= 0:
	print 'Wrong days ago. Please enter a number greater than 0.'
	exit()

logging.info('Starting Cleaner')

Config = MainConf.Get()

myqueue_count = MyQueue.Clear(Config['IMAGE_FILE_DIR'], days_ago, force_mode)
rsspost_count = RssPost.Clear(Config['IMAGE_FILE_DIR'], days_ago, force_mode)

logging.warning('Deleted: %d Queue item | %d Rss post'%(myqueue_count, rsspost_count))

logging.info('Exiting Cleaner')