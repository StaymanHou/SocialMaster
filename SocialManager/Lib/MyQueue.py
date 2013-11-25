import Mydb
import os
import json
from datetime import datetime, timedelta
from MyFunction import floorbyday
from MyDict import STATUS_DICT

class MyQueue(object):
    def __init__(self):
        self.pk=None
        self.fields={}
        self.fields['STATUS'] = None
        self.fields['ACCOUNT'] = None
        self.fields['MODULE'] = None
        self.fields['TYPE'] = None
        self.fields['TITLE'] = None
        self.fields['CONTENT'] = None
        self.fields['EXTRA_CONTENT'] = None
        self.fields['TAG'] = None
        self.fields['IMAGE_FILE'] = None
        self.fields['LINK'] = None
        self.fields['OTHER_FIELD'] = None
        self.fields['SCHEDULE_TIME'] = None
        self.fields['RSS_SOURCE_PK'] = None

    def __getitem__(self,field):
        if field == 'PK':
            return self.pk
        else:
            if field in self.fields:
                return self.fields[field]

    def __setitem__(self,field,value):
        if field == 'PK':
            self.pk = value
        else:
            self.fields[field] = value
    
    def StaticClear(imagefiledir, cachingtime, force_mode=False):
        today = floorbyday(datetime.now())
        deadline = today - timedelta(days = cachingtime)
        clear_count = 0
        if force_mode:
            cur = Mydb.MydbExec(("SELECT IMAGE_FILE FROM queue WHERE SCHEDULE_TIME != '0000-00-00 00:00:00' AND SCHEDULE_TIME < %s",(deadline)))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['IMAGE_FILE'] is None: continue
                imgflpath = imagefiledir+imgfl['IMAGE_FILE']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE FROM queue WHERE SCHEDULE_TIME != '0000-00-00 00:00:00' AND SCHEDULE_TIME < %s",(deadline)))
        else:
            cur = Mydb.MydbExec(("SELECT IMAGE_FILE FROM queue WHERE SCHEDULE_TIME < %s AND STATUS != %s",(deadline, STATUS_DICT['Pending'])))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['IMAGE_FILE'] is None: continue
                imgflpath = imagefiledir+imgfl['IMAGE_FILE']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE FROM queue WHERE SCHEDULE_TIME < %s AND STATUS != %s",(deadline, STATUS_DICT['Pending'])))
        return clear_count

    Clear = staticmethod(StaticClear)
    
    def StaticGetPkList(account, module, timestart, timeend):
        cur = Mydb.MydbExec(("SELECT PK FROM queue WHERE ACCOUNT = %s AND MODULE = %s AND SCHEDULE_TIME >= %s AND SCHEDULE_TIME < %s",(account, module, timestart, timeend)))
        queuelst = cur.fetchall()
        return queuelst

    GetPkList = staticmethod(StaticGetPkList)
        
    def StaticGetLastTime(account, module):
        cur = Mydb.MydbExec(("SELECT SCHEDULE_TIME FROM queue WHERE ACCOUNT = %s AND MODULE = %s ORDER BY SCHEDULE_TIME DESC LIMIT 1",(account, module)))
        if cur.rowcount:
            row = cur.fetchone()
            return row['SCHEDULE_TIME']
        return datetime.min

    GetLastTime = staticmethod(StaticGetLastTime)
    
    def GetPendingFirst(self, AccPk, ModPk):
        cur = Mydb.MydbExec(("SELECT PK, STATUS, ACCOUNT, MODULE, TYPE, TITLE, CONTENT, EXTRA_CONTENT, TAG, IMAGE_FILE, LINK, OTHER_FIELD, SCHEDULE_TIME FROM queue WHERE STATUS = %s AND ACCOUNT = %s AND MODULE = %s ORDER BY PK ASC LIMIT 1",(STATUS_DICT['Pending'], AccPk, ModPk)))
        if cur.rowcount:
            row = cur.fetchone()
            self.pk = row['PK']
            self.fields['STATUS'] = row['STATUS']
            self.fields['ACCOUNT'] = row['ACCOUNT']
            self.fields['MODULE'] = row['MODULE']
            self.fields['TAG'] = row['TAG']
            self.fields['TYPE'] = row['TYPE']
            try: self.fields['TITLE'] = row['TITLE'].decode('utf-8').encode('ascii','ignore')
            except: self.fields['TITLE'] = ''
            try: self.fields['CONTENT'] = row['CONTENT'].decode('utf-8').encode('ascii','ignore')
            except: self.fields['CONTENT'] = ''
            self.fields['EXTRA_CONTENT'] = row['EXTRA_CONTENT']
            self.fields['IMAGE_FILE'] = row['IMAGE_FILE']
            self.fields['LINK'] = row['LINK']
            if row['OTHER_FIELD'] is not None and row['OTHER_FIELD']!='':
                self.fields['OTHER_FIELD'] = json.loads(row['OTHER_FIELD'])
            else:
                self.fields['OTHER_FIELD'] = {}
            self.fields['SCHEDULE_TIME'] = row['SCHEDULE_TIME']
        else: return 0
        return 1

    def StaticGetScheduledPendingFirst(AccPk, ModPk):
        qi = None
        cur = Mydb.MydbExec(("SELECT PK, STATUS, ACCOUNT, MODULE, TYPE, TITLE, CONTENT, EXTRA_CONTENT, TAG, IMAGE_FILE, LINK, OTHER_FIELD, SCHEDULE_TIME FROM queue WHERE STATUS = %s AND ACCOUNT = %s AND MODULE = %s AND SCHEDULE_TIME > '0000-00-00 00:00:00' ORDER BY SCHEDULE_TIME ASC LIMIT 1",(STATUS_DICT['Pending'], AccPk, ModPk)))
        if cur.rowcount:
            row = cur.fetchone()
            qi = MyQueue()
            qi['PK'] = row['PK']
            qi['STATUS'] = row['STATUS']
            qi['ACCOUNT'] = row['ACCOUNT']
            qi['MODULE'] = row['MODULE']
            qi['TYPE'] = row['TYPE']
            try: qi['TITLE'] = row['TITLE'].decode('utf-8').encode('ascii','ignore')
            except: qi['TITLE'] = ''
            try: qi['CONTENT'] = row['CONTENT'].decode('utf-8').encode('ascii','ignore')
            except: qi['CONTENT'] = ''
            qi['EXTRA_CONTENT'] = row['EXTRA_CONTENT']
            qi['TAG'] = row['TAG']
            qi['IMAGE_FILE'] = row['IMAGE_FILE']
            qi['LINK'] = row['LINK']
            if row['OTHER_FIELD'] is not None and row['OTHER_FIELD']!='':
                qi['OTHER_FIELD'] = json.loads(row['OTHER_FIELD'])
            else:
                qi['OTHER_FIELD'] = {}
            qi['SCHEDULE_TIME'] = row['SCHEDULE_TIME']
        return qi

    GetScheduledPendingFirst = staticmethod(StaticGetScheduledPendingFirst)

    def SetSchedule(self, schedule_time):
        self.fields['SCHEDULE_TIME'] = schedule_time
        self.save()
    
    def StaticGetByPk(pk):
        qi = MyQueue()
        cur = Mydb.MydbExec(("SELECT PK, STATUS, ACCOUNT, MODULE, TYPE, TITLE, CONTENT, EXTRA_CONTENT, TAG, IMAGE_FILE, LINK, OTHER_FIELD, SCHEDULE_TIME FROM queue WHERE PK = %s",(pk)))
        if cur.rowcount:
            row = cur.fetchone()
            qi['PK'] = row['PK']
            qi['STATUS'] = row['STATUS']
            qi['ACCOUNT'] = row['ACCOUNT']
            qi['MODULE'] = row['MODULE']
            qi['TYPE'] = row['TYPE']
            try: qi['TITLE'] = row['TITLE'].decode('utf-8').encode('ascii','ignore')
            except: qi['TITLE'] = ''
            try: qi['CONTENT'] = row['CONTENT'].decode('utf-8').encode('ascii','ignore')
            except: qi['CONTENT'] = ''
            qi['EXTRA_CONTENT'] = row['EXTRA_CONTENT']
            qi['TAG'] = row['TAG']
            qi['IMAGE_FILE'] = row['IMAGE_FILE']
            qi['LINK'] = row['LINK']
            if row['OTHER_FIELD'] is not None and row['OTHER_FIELD']!='':
                qi['OTHER_FIELD'] = json.loads(row['OTHER_FIELD'])
            else:
                qi['OTHER_FIELD'] = {}
            qi['SCHEDULE_TIME'] = row['SCHEDULE_TIME']
        return qi
    
    GetByPk = staticmethod(StaticGetByPk)
    
    def save(self):
        if self.pk is None:
            if self.fields['SCHEDULE_TIME'] is None:
                self.fields['SCHEDULE_TIME'] = '0000-00-00 00:00:00'
            Mydb.MydbExec(('INSERT INTO queue(STATUS, ACCOUNT, MODULE, TYPE, TITLE, CONTENT, EXTRA_CONTENT, TAG, IMAGE_FILE, LINK, OTHER_FIELD, SCHEDULE_TIME, RSS_SOURCE_PK) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(self.fields['STATUS'], self.fields['ACCOUNT'], self.fields['MODULE'], self.fields['TYPE'], self.fields['TITLE'], self.fields['CONTENT'], self.fields['EXTRA_CONTENT'], self.fields['TAG'], self.fields['IMAGE_FILE'], self.fields['LINK'], json.JSONEncoder().encode(self.fields['OTHER_FIELD']), self.fields['SCHEDULE_TIME'], self.fields['RSS_SOURCE_PK'])))
        else:
            if self.fields['SCHEDULE_TIME'] is None:
                self.fields['SCHEDULE_TIME'] = '0000-00-00 00:00:00'
            Mydb.MydbExec(('UPDATE queue SET STATUS = %s, ACCOUNT = %s, MODULE = %s, TYPE = %s, TITLE = %s, CONTENT = %s, EXTRA_CONTENT = %s, TAG = %s, IMAGE_FILE = %s, LINK = %s, OTHER_FIELD = %s, SCHEDULE_TIME = %s WHERE PK = %s',(self.fields['STATUS'], self.fields['ACCOUNT'], self.fields['MODULE'], self.fields['TYPE'], self.fields['TITLE'], self.fields['CONTENT'], self.fields['EXTRA_CONTENT'], self.fields['TAG'], self.fields['IMAGE_FILE'], self.fields['LINK'], json.JSONEncoder().encode(self.fields['OTHER_FIELD']), self.fields['SCHEDULE_TIME'], self.pk)))
    
