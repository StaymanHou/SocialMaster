import Mydb
import os
from datetime import datetime, timedelta
from MyFunction import floorbyday

class RssPost(object):
    def __init__(self):
        self.pk=None
        self.fields={}
        self.fields['ACCOUNT'] = None
        self.fields['TITLE'] = None
        self.fields['DESCRIPTION'] = None
        self.fields['CONTENT'] = None
        self.fields['TAG'] = None
        self.fields['IMAGE_FILE'] = None
        self.fields['IMAGE_LINK'] = None
        self.fields['LINK'] = None
        self.fields['OTHER_FIELD'] = None
        self.fields['SOCIAL_SCORE'] = 0
        self.fields['CREATE_TIME'] = None

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
    
    def Put(self):
        cur = Mydb.MydbExec(("INSERT INTO rss_post(ACCOUNT, TITLE, DESCRIPTION, CONTENT, TAG, IMAGE_FILE, IMAGE_LINK, LINK, OTHER_FIELD, SOCIAL_SCORE, CREATE_TIME) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(self.fields['ACCOUNT'], self.fields['TITLE'].encode('utf-8'), self.fields['DESCRIPTION'].encode('utf-8'), self.fields['CONTENT'].encode('utf-8'), self.fields['TAG'], self.fields['IMAGE_FILE'], self.fields['IMAGE_LINK'], self.fields['LINK'], self.fields['OTHER_FIELD'], self.fields['SOCIAL_SCORE'], self.fields['CREATE_TIME'])))
        return 

    def StaticClear(imagefiledir, cachingtime, force_mode=False):
        today = floorbyday(datetime.now())
        deadline = today - timedelta(days = cachingtime)
        clear_count = 0
        if force_mode:
            cur = Mydb.MydbExec(("SELECT IMAGE_FILE FROM rss_post WHERE CREATE_TIME < %s",(deadline)))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['IMAGE_FILE'] is None or len(imgfl['IMAGE_FILE'].strip())==0: continue
                imgflpath = imagefiledir+imgfl['IMAGE_FILE']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE FROM rss_post WHERE CREATE_TIME < %s",(deadline)))
        else:
            cur = Mydb.MydbExec(("SELECT `rss_post`.`IMAGE_FILE` FROM `rss_post` LEFT JOIN `queue` ON `rss_post`.`PK`=`queue`.`RSS_SOURCE_PK` WHERE `queue`.`RSS_SOURCE_PK` IS NULL AND CREATE_TIME < %s",(deadline)))
            imglst = cur.fetchall()
            clear_count = len(imglst)
            for imgfl in imglst:
                if imgfl['IMAGE_FILE'] is None or len(imgfl['IMAGE_FILE'].strip())==0: continue
                imgflpath = imagefiledir+imgfl['IMAGE_FILE']
                try: os.remove(imgflpath)
                except: pass
            cur = Mydb.MydbExec(("DELETE rss_post FROM `rss_post` LEFT JOIN `queue` ON `rss_post`.`PK`=`queue`.`RSS_SOURCE_PK` WHERE `queue`.`RSS_SOURCE_PK` IS NULL AND CREATE_TIME < %s",(deadline)))
        return clear_count

    Clear = staticmethod(StaticClear)
    
    def StaticGetLatest(account, module, require_image=False):
        rsspost = RssPost()
        query = "SELECT * FROM rss_post WHERE ACCOUNT = %s"
        if require_image: query += " AND IMAGE_LINK IS NOT NULL"
        query += " AND PK NOT IN (SELECT RSS_SOURCE_PK FROM queue WHERE ACCOUNT = %s AND MODULE = %s) ORDER BY PK DESC LIMIT 1"
        cur = Mydb.MydbExec((query,(account, account, module)))
        if cur.rowcount:
            row = cur.fetchone()
            rsspost['PK'] = row['PK']
            rsspost['ACCOUNT'] = row['ACCOUNT']
            rsspost['TITLE'] = row['TITLE']
            rsspost['DESCRIPTION'] = row['DESCRIPTION']
            rsspost['CONTENT'] = row['CONTENT']
            rsspost['TAG'] = row['TAG']
            rsspost['TITLE'] = row['TITLE']
            rsspost['CONTENT'] = row['CONTENT']
            rsspost['IMAGE_FILE'] = row['IMAGE_FILE']
            rsspost['IMAGE_LINK'] = row['IMAGE_LINK']
            rsspost['LINK'] = row['LINK']
            if row['OTHER_FIELD'] is not None and row['OTHER_FIELD']!='':
                rsspost['OTHER_FIELD'] = json.loads(row['OTHER_FIELD'])
            else:
                rsspost['OTHER_FIELD'] = {}
            rsspost['SOCIAL_SCORE'] = row['SOCIAL_SCORE']
            rsspost['CREATE_TIME'] = row['CREATE_TIME']
        return rsspost
        
    GetLatest = staticmethod(StaticGetLatest)
