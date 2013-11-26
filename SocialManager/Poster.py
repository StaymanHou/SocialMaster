from time import sleep
import logging
from Lib.MainConf import *
from Lib.Account import *
from Lib.AccSetting import *
from Lib.Module import *
from Lib.MyQueue import *
import socket

debug_mode = True

timeout = 60
socket.setdefaulttimeout(timeout)

LOG_FILE_PATH = 'log_poster.txt'

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

print 'Starting Poster'

while 1:
    AccLst = Account.GetActiveList()
    ModLst = Module.GetActiveList()
    for Acc in AccLst:
        for Mod in ModLst:
            AccSet = AccSetting.GetByAccAndMod(Acc['id'], Mod['id'])
            if (AccSet is None) or (len(AccSet)==0):
                logging.warning('Fail to load account setting: %s %s'%(Acc['name'], Mod['name']))
                continue
            if AccSet['active']==False: continue
            modname = 'Lib.PostHandler.'+Mod['name']+'_posterhandler'
            try:
                mod = __import__(modname, fromlist=[''])
                handler = mod.handler()
            except Exception, e:
                logging.warning('Fail to load poster module: %s : %s'%(Mod['name'], e))
                continue
            handler.handle(Acc, AccSet, MainConf['IMAGE_FILE_DIR'])
    sleep(MainConf['POSTER_ITERATION'])

print 'Exiting Poster'

