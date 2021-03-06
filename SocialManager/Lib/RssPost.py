import Mydb
import os
from datetime import datetime, timedelta
from MyFunction import floorbyday
from AccSetting import *

class RssPost(object):
    def __init__(self):
        self.id=None
        self.fields={}
        self.fields['account_id'] = None
        self.fields['site_id'] = None
        self.fields['title'] = None
        self.fields['description'] = None
        self.fields['content'] = None
        self.fields['tags'] = None
        self.fields['image_file'] = None
        self.fields['image_link'] = None
        self.fields['link'] = None
        self.fields['social_score'] = 0
        self.fields['created_at'] = None

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
            cur = Mydb.MydbExec(("SELECT image_file FROM pool_posts WHERE created_at < %s",(deadline)))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['image_file'] is None or len(imgfl['image_file'].strip())==0: continue
                imgflpath = imagefiledir+imgfl['image_file']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE FROM pool_posts WHERE created_at < %s",(deadline)))
        else:
            cur = Mydb.MydbExec(("SELECT `pool_posts`.`image_file` FROM `pool_posts` LEFT JOIN `queue_posts` ON `pool_posts`.`id`=`queue_posts`.`pool_post_id` WHERE `queue_posts`.`pool_post_id` IS NULL AND created_at < %s",(deadline)))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['image_file'] is None or len(imgfl['image_file'].strip())==0: continue
                imgflpath = imagefiledir+imgfl['image_file']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE pool_posts FROM `pool_posts` LEFT JOIN `queue_posts` ON `pool_posts`.`id`=`queue_posts`.`pool_post_id` WHERE `queue_posts`.`pool_post_id` IS NULL AND created_at < %s",(deadline)))
        return clear_count

    Clear = staticmethod(StaticClear)
    
    def StaticGetLatest(account_id, module, require_image=False):
        acc_setting = AccSetting.GetByAccAndMod(account_id, module)
        acc_setting_id = acc_setting['id']
        rsspost = RssPost()
        query = "SELECT * FROM pool_posts WHERE account_id = %s"
        if require_image: query += " AND image_link IS NOT NULL"
        query += " AND id NOT IN (SELECT pool_post_id FROM queue_posts WHERE acc_setting_id = %s) ORDER BY id DESC LIMIT 1"
        cur = Mydb.MydbExec((query,(account_id, acc_setting_id,)))
        if cur.rowcount:
            row = cur.fetchone()
            rsspost['id'] = row['id']
            rsspost['account_id'] = row['account_id']
            rsspost['site_id'] = row['site_id']
            rsspost['title'] = row['title']
            rsspost['description'] = row['description']
            rsspost['content'] = row['content']
            rsspost['tags'] = row['tags']
            rsspost['content'] = row['content']
            rsspost['image_file'] = row['image_file']
            rsspost['image_link'] = row['image_link']
            rsspost['link'] = row['link']
            rsspost['social_score'] = row['social_score']
            rsspost['created_at'] = row['created_at']
        return rsspost
        
    GetLatest = staticmethod(StaticGetLatest)

    def Put(self):
        Mydb.MydbExec(("INSERT INTO pool_posts(account_id, pool_post_type_id, site_id, hidden, title, description, content, tags, image_file, image_link, link, social_score, created_at) VALUES (%s, 1, %s, 0, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(self.fields['account_id'], self.fields['site_id'], self.fields['title'].encode('utf-8'), self.fields['description'].encode('utf-8'), self.fields['content'].encode('utf-8'), self.fields['tags'], self.fields['image_file'], self.fields['image_link'], self.fields['link'], self.fields['social_score'], self.fields['created_at'])))
        return 