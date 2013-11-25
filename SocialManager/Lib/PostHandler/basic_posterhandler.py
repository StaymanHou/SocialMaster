from datetime import datetime, timedelta
from ..MyQueue import *
from ..AutoMode import *
from ..Tags import *
from ..MyDict import STATUS_DICT
from random import randint
import logging

class basicposterhandler(object):
    def __init__(self):
        self.now = datetime.now()
        self.queue = MyQueue()
        self.imgdir = None
        self.module_name = 'basic_module'

    def handle(self, Acc, AccSet, imgdir):
        self.imgdir = imgdir
        AM = AutoMode.GetByPk(AccSet['AUTO_MODE'])
        self.auto_mode_handle(Acc, AccSet, AM)
        now = datetime.now()
        if AccSet['TIME_START'] < AccSet['TIME_END']:
            TS = now.replace(hour=AccSet['TIME_START'].hour, minute=AccSet['TIME_START'].minute, second=AccSet['TIME_START'].second, microsecond=0)
            TE = now.replace(hour=AccSet['TIME_END'].hour, minute=AccSet['TIME_END'].minute, second=AccSet['TIME_END'].second, microsecond=0)
        else:
            if now.time() <= AccSet['TIME_END']:
                TS = (now-timedelta(days=1)).replace(hour=AccSet['TIME_START'].hour, minute=AccSet['TIME_START'].minute, second=AccSet['TIME_START'].second, microsecond=0)
                TE = now.replace(hour=AccSet['TIME_END'].hour, minute=AccSet['TIME_END'].minute, second=AccSet['TIME_END'].second, microsecond=0)
            else:
                TS = now.replace(hour=AccSet['TIME_START'].hour, minute=AccSet['TIME_START'].minute, second=AccSet['TIME_START'].second, microsecond=0)
                TE = (now+timedelta(days=1)).replace(hour=AccSet['TIME_END'].hour, minute=AccSet['TIME_END'].minute, second=AccSet['TIME_END'].second, microsecond=0)
        if now < TS or now >= TE: return
        TD = (TE-TS)/AccSet['NUM_PER_DAY']
        PD = (now-TS).seconds/(TD.seconds)
        PS = TS + PD*TD
        PE = TS + (PD+1)*TD
        QI = None
        # schedule pending in this period if no scheduled
        thisqueuelst = self.queue.GetPkList(Acc['PK'], AccSet['MODULE'], PS, PE)
        if (thisqueuelst is None) or (len(thisqueuelst)==0):
            if self.queue.GetPendingFirst(Acc['PK'], AccSet['MODULE']):
                lasttime = MyQueue.GetLastTime(Acc['PK'], AccSet['MODULE'])
                if lasttime is None: WS = 0
                else:
                    WS = max(0,(lasttime-PS).days*86400+(lasttime-PS).seconds+AccSet['MIN_POST_INTERVAL'])
                WE = (PE-PS).days*86400+(PE-PS).seconds
                if WS<=WE:
                    scheduletime = PS+timedelta(seconds=randint(WS,WE))
                    self.queue.SetSchedule(scheduletime)
                    logging.info('Poster: @%s #%s | [Scheduled] %s'%(Acc['NAME'], self.module_name, (self.queue['TITLE'])[:16]))
        # check for first scheduled pending and post
        QI = MyQueue.GetScheduledPendingFirst(Acc['PK'], AccSet['MODULE'])
        if QI is not None and QI['STATUS']==STATUS_DICT['Pending'] and QI['SCHEDULE_TIME']<=datetime.now():
            if QI['TAG'] is not None and len(QI['TAG'])>0:
                Tags.SaveTags(QI['TAG'].split(','))
            if self.post_handle(AccSet, QI, imgdir):
                QI['STATUS'] = STATUS_DICT['Posted']
                QI.save()
                logging.info('Poster: @%s #%s | [POSTED] %s'%(Acc['NAME'], self.module_name, (QI['TITLE'])[:16]))
            else:
                QI['STATUS'] = STATUS_DICT['PostFail']
                QI.save()
                logging.warning('Poster: @%s #%s | [FAILED] %s'%(Acc['NAME'], self.module_name, (QI['TITLE'])[:16]))
        return

    def auto_mode_handle(self, acc, accset, am):
        raise Exception('Post_handle is working! Please override auto_mode_handle method to make it "really" working!')
        return

    def post_handle(self, accset, queueitem, imgdir):
        raise Exception('Post_handle is working! Please override post_handle method to make it "really" working!')
        return 1
