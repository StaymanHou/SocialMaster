import Mydb
import os
import json
from datetime import datetime, timedelta
from MyFunction import floorbyday
from MyDict import STATUS_DICT

class MyQueue(object):
    def __init__(self):
        self.id=None
        self.fields={}
        self.fields['status_id'] = None
        self.fields['acc_setting_id'] = None
        self.fields['post_type'] = None
        self.fields['title'] = None
        self.fields['content'] = None
        self.fields['extra_content'] = None
        self.fields['tags'] = None
        self.fields['image_file'] = None
        self.fields['image_link'] = None
        self.fields['link'] = None
        self.fields['other_field'] = None
        self.fields['schedule_time'] = None
        self.fields['pool_post_id'] = None

    def __getitem__(self,field):
        if field == 'id':
            return self.id
        else:
            if field in self.fields:
                return self.fields[field]

    def __setitem__(self,field,value):
        if field == 'id':
            self.id = value
        else:
            self.fields[field] = value
    
    def StaticClear(imagefiledir, cachingtime, force_mode=False):
        today = floorbyday(datetime.now())
        deadline = today - timedelta(days = cachingtime)
        clear_count = 0
        if force_mode:
            cur = Mydb.MydbExec(("SELECT image_file FROM queue_posts WHERE schedule_time != '0000-00-00 00:00:00' AND schedule_time < %s",(deadline)))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['image_file'] is None: continue
                imgflpath = imagefiledir+imgfl['image_file']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE FROM queue_posts WHERE schedule_time != '0000-00-00 00:00:00' AND schedule_time < %s",(deadline)))
        else:
            cur = Mydb.MydbExec(("SELECT image_file FROM queue_posts WHERE schedule_time < %s AND status_id != %s",(deadline, STATUS_DICT['Pending'])))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['image_file'] is None: continue
                imgflpath = imagefiledir+imgfl['image_file']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE FROM queue_posts WHERE schedule_time < %s AND status_id != %s",(deadline, STATUS_DICT['Pending'])))
        return clear_count

    Clear = staticmethod(StaticClear)
    
    def StaticGetPkList(acc_setting_id, timestart, timeend):
        cur = Mydb.MydbExec(("SELECT id FROM queue_posts WHERE acc_setting_id = %s AND schedule_time >= %s AND schedule_time < %s",(acc_setting_id, timestart, timeend)))
        queue_postslst = cur.fetchall()
        return queue_postslst

    GetPkList = staticmethod(StaticGetPkList)
        
    def StaticGetLastTime(acc_setting_id):
        cur = Mydb.MydbExec(("SELECT schedule_time FROM queue_posts WHERE acc_setting_id = %s ORDER BY schedule_time DESC LIMIT 1",(acc_setting_id, )))
        if cur.rowcount:
            row = cur.fetchone()
            return row['schedule_time']
        return datetime.min

    GetLastTime = staticmethod(StaticGetLastTime)
    
    def GetPendingFirst(self, acc_setting_id):
        cur = Mydb.MydbExec(("SELECT id, status_id, acc_setting_id, post_type, title, content, extra_content, tags, image_file, image_link, link, other_field, schedule_time FROM queue_posts WHERE status_id = %s AND acc_setting_id = %s ORDER BY id ASC LIMIT 1",(STATUS_DICT['Pending'], acc_setting_id)))
        if cur.rowcount:
            row = cur.fetchone()
            self.id = row['id']
            self.fields['status_id'] = row['status_id']
            self.fields['acc_setting_id'] = row['acc_setting_id']
            self.fields['tags'] = row['tags']
            self.fields['post_type'] = row['post_type']
            try: self.fields['title'] = row['title'].decode('utf-8').encode('ascii','ignore')
            except: self.fields['title'] = ''
            try: self.fields['content'] = row['content'].decode('utf-8').encode('ascii','ignore')
            except: self.fields['content'] = ''
            self.fields['extra_content'] = row['extra_content']
            self.fields['image_file'] = row['image_file']
            self.fields['image_link'] = row['image_link']
            self.fields['link'] = row['link']
            if row['other_field'] is not None and row['other_field']!='':
                self.fields['other_field'] = json.loads(row['other_field'])
            else:
                self.fields['other_field'] = {}
            self.fields['schedule_time'] = row['schedule_time']
        else: return 0
        return 1

    def StaticGetScheduledPendingFirst(acc_setting_id):
        qi = None
        cur = Mydb.MydbExec(("SELECT id, status_id, acc_setting_id, post_type, title, content, extra_content, tags, image_file, image_link, link, other_field, schedule_time FROM queue_posts WHERE status_id = %s AND acc_setting_id = %s AND schedule_time > '0000-00-00 00:00:00' ORDER BY schedule_time ASC LIMIT 1",(STATUS_DICT['Pending'], acc_setting_id)))
        if cur.rowcount:
            row = cur.fetchone()
            qi = MyQueue()
            qi['id'] = row['id']
            qi['status_id'] = row['status_id']
            qi['acc_setting_id'] = row['acc_setting_id']
            qi['post_type'] = row['post_type']
            try: qi['title'] = row['title'].decode('utf-8').encode('ascii','ignore')
            except: qi['title'] = ''
            try: qi['content'] = row['content'].decode('utf-8').encode('ascii','ignore')
            except: qi['content'] = ''
            qi['extra_content'] = row['extra_content']
            qi['tags'] = row['tags']
            qi['image_file'] = row['image_file']
            qi['image_link'] = row['image_link']
            qi['link'] = row['link']
            if row['other_field'] is not None and row['other_field']!='':
                qi['other_field'] = json.loads(row['other_field'])
            else:
                qi['other_field'] = {}
            qi['schedule_time'] = row['schedule_time']
        return qi

    GetScheduledPendingFirst = staticmethod(StaticGetScheduledPendingFirst)

    def SetSchedule(self, schedule_time):
        self.fields['schedule_time'] = schedule_time
        self.save()
    
    def StaticGetByPk(id):
        qi = MyQueue()
        cur = Mydb.MydbExec(("SELECT id, status_id, acc_setting_id, post_type, title, content, extra_content, tags, image_file, image_link, link, other_field, schedule_time FROM queue_posts WHERE id = %s",(id)))
        if cur.rowcount:
            row = cur.fetchone()
            qi['id'] = row['id']
            qi['status_id'] = row['status_id']
            qi['acc_setting_id'] = row['acc_setting_id']
            qi['post_type'] = row['post_type']
            try: qi['title'] = row['title'].decode('utf-8').encode('ascii','ignore')
            except: qi['title'] = ''
            try: qi['content'] = row['content'].decode('utf-8').encode('ascii','ignore')
            except: qi['content'] = ''
            qi['extra_content'] = row['extra_content']
            qi['tags'] = row['tags']
            qi['image_file'] = row['image_file']
            qi['image_link'] = row['image_link']
            qi['link'] = row['link']
            if row['other_field'] is not None and row['other_field']!='':
                qi['other_field'] = json.loads(row['other_field'])
            else:
                qi['other_field'] = {}
            qi['schedule_time'] = row['schedule_time']
        return qi
    
    GetByPk = staticmethod(StaticGetByPk)
    
    def save(self):
        if self.id is None:
            if self.fields['schedule_time'] is None:
                self.fields['schedule_time'] = '0000-00-00 00:00:00'
            Mydb.MydbExec(('INSERT INTO queue_posts(status_id, acc_setting_id, post_type, title, content, extra_content, tags, image_file, image_link, link, other_field, schedule_time, pool_post_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(self.fields['status_id'], self.fields['acc_setting_id'], self.fields['post_type'], self.fields['title'], self.fields['content'], self.fields['extra_content'], self.fields['tags'], self.fields['image_file'], self.fields['image_link'], self.fields['link'], json.JSONEncoder().encode(self.fields['other_field']), self.fields['schedule_time'], self.fields['pool_post_id'])))
        else:
            if self.fields['schedule_time'] is None:
                self.fields['schedule_time'] = '0000-00-00 00:00:00'
            Mydb.MydbExec(('UPDATE queue_posts SET status_id = %s, acc_setting_id = %s, post_type = %s, title = %s, content = %s, extra_content = %s, tags = %s, image_file = %s, image_link = %s, link = %s, other_field = %s, schedule_time = %s WHERE id = %s',(self.fields['status_id'], self.fields['acc_setting_id'], self.fields['post_type'], self.fields['title'], self.fields['content'], self.fields['extra_content'], self.fields['tags'], self.fields['image_file'], self.fields['image_link'], self.fields['link'], json.JSONEncoder().encode(self.fields['other_field']), self.fields['schedule_time'], self.id)))
    
