from time import sleep
from datetime import datetime, timedelta
import logging
from Lib.MainConf import *
from Lib.Account import *
import feedparser
import socket
import os
from Lib.MyFunction import domainFromUrl

debug_mode = True

timeout = 10
socket.setdefaulttimeout(timeout)

LOG_FILE_PATH = 'log_puller.txt'

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

print 'Starting RssPuller'

while 1:
    Config = MainConf.Get()
    AccLst = Account.GetActiveList()
    for Acc in AccLst:
        if Acc['LAST_UPDATE']==None:
            Acc['LAST_UPDATE'] = datetime.now() - timedelta(days=7)
        rss_urls = [ rss_url.strip() for rss_url in Acc['RSS_URL'].split(',') ]
        for rss_url in rss_urls:
            try: d = feedparser.parse(rss_url)
            except:
                logging.warning('Can\'t get the following feed: '+Acc['RSS_URL'])
                continue
            domain = domainFromUrl(rss_url)
            modname = 'Lib.RssHandler.basic_rsshandler'
            for i in xrange(len(domain.split('.'))):
                subdomain = '_'.join(domain.split('.')[i:])
                if os.path.exists('Lib/RssHandler/'+subdomain+'_rsshandler.py'):
                    modname = 'Lib.RssHandler.'+subdomain+'_rsshandler'
                    break
            mod = __import__(modname, fromlist=[''])
            handler = mod.myrsshand()
            handler.handle(d, Acc, Config['IMAGE_FILE_DIR'])
        last_update = datetime.now()
        Account.SetLastUpdate(Acc['PK'], last_update)
    sleep(Config['PULLER_ITERATION'])

print 'Exiting RssPuller'

