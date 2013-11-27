from datetime import datetime, timedelta
from ..MyQueue import *
from ..AutoMode import *
from ..Tags import *
from ..MyDict import STATUS_DICT
from ..MyFunction import domainFromUrl
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
        AM = AutoMode.GetByPk(AccSet['auto_mode_id'])
        self.auto_mode_handle(Acc, AccSet, AM)
        now = datetime.now()
        if AccSet['time_start'] < AccSet['time_end']:
            TS = now.replace(hour=AccSet['time_start'].hour, minute=AccSet['time_start'].minute, second=AccSet['time_start'].second, microsecond=0)
            TE = now.replace(hour=AccSet['time_end'].hour, minute=AccSet['time_end'].minute, second=AccSet['time_end'].second, microsecond=0)
        else:
            if now.time() <= AccSet['time_end']:
                TS = (now-timedelta(days=1)).replace(hour=AccSet['time_start'].hour, minute=AccSet['time_start'].minute, second=AccSet['time_start'].second, microsecond=0)
                TE = now.replace(hour=AccSet['time_end'].hour, minute=AccSet['time_end'].minute, second=AccSet['time_end'].second, microsecond=0)
            else:
                TS = now.replace(hour=AccSet['time_start'].hour, minute=AccSet['time_start'].minute, second=AccSet['time_start'].second, microsecond=0)
                TE = (now+timedelta(days=1)).replace(hour=AccSet['time_end'].hour, minute=AccSet['time_end'].minute, second=AccSet['time_end'].second, microsecond=0)
        if now < TS or now >= TE: return
        TD = (TE-TS)/AccSet['num_per_day']
        PD = (now-TS).seconds/(TD.seconds)
        PS = TS + PD*TD
        PE = TS + (PD+1)*TD
        QI = None
        # schedule pending in this period if no scheduled
        thisqueuelst = self.queue.GetPkList(AccSet['id'], PS, PE)
        if (thisqueuelst is None) or (len(thisqueuelst)==0):
            if self.queue.GetPendingFirst(AccSet['id']):
                lasttime = MyQueue.GetLastTime(Acc['id'])
                if lasttime is None: WS = 0
                else:
                    WS = max(0,(lasttime-PS).days*86400+(lasttime-PS).seconds+AccSet['min_post_interval'])
                WE = (PE-PS).days*86400+(PE-PS).seconds
                if WS<=WE:
                    scheduletime = PS+timedelta(seconds=randint(WS,WE))
                    self.queue.SetSchedule(scheduletime)
                    logging.info('Poster: @%s #%s | [Scheduled] %s'%(Acc['name'], self.module_name, (self.queue['title'])[:16]))
        # check for first scheduled pending and post
        QI = MyQueue.GetScheduledPendingFirst(AccSet['id'])
        if QI is not None and QI['status_id']==STATUS_DICT['Pending'] and QI['schedule_time']<=datetime.now():
            if QI['tags'] is not None and len(QI['tags'])>0:
                Tags.SaveTags(QI['tags'].split(','), domainFromUrl(QI['link']))
            if self.post_handle(AccSet, QI, imgdir):
                QI['status_id'] = STATUS_DICT['Posted']
                QI.save()
                logging.info('Poster: @%s #%s | [POSTED] %s'%(Acc['name'], self.module_name, (QI['title'])[:16]))
            else:
                QI['status_id'] = STATUS_DICT['PostFail']
                QI.save()
                logging.warning('Poster: @%s #%s | [FAILED] %s'%(Acc['name'], self.module_name, (QI['title'])[:16]))
        return

    def auto_mode_handle(self, acc, accset, am):
        raise Exception('Post_handle is working! Please override auto_mode_handle method to make it "really" working!')
        return

    def post_handle(self, accset, queueitem, imgdir):
        raise Exception('Post_handle is working! Please override post_handle method to make it "really" working!')
        return 1
