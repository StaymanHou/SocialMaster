from ..RssPost import *
from ..Tags import *
import requests
import time
from .. import DOMparser
from lxml import etree
from lxml import html as lxmlhtml
from ..systemHelper import parseTime, specialize_path
from ..MyFunction import randomString
import logging

class basicrsshand(object):
    def __init__(self):
        self.rsspost = RssPost()

    def handle(self, d, Acc, imgdir):
        self.imgdir = imgdir
        last_update = Acc['LAST_UPDATE']
        for rsselem in d.entries:
            t = rsselem.published
            t = parseTime(t)
            if t < last_update: continue
            self.rsspost['ACCOUNT'] = Acc['PK']
            try: self.rsspost['TITLE'] = rsselem.title.encode('ascii','ignore')
            except: self.rsspost['TITLE'] = ''
            try: self.rsspost['DESCRIPTION'] = rsselem.summary.encode('ascii','ignore')
            except: self.rsspost['DESCRIPTION'] = ''
            self.rsspost['CONTENT'] = ''
            self.rsspost['TAG'] = ''
            self.rsspost['IMAGE_FILE'] = None
            if ('media_content' in rsselem) and (len(rsselem.media_content)>0) and ('url' in rsselem.media_content[0]): self.rsspost['IMAGE_LINK'] = rsselem.media_content[0]['url']
            else: self.rsspost['IMAGE_LINK'] = None
            self.rsspost['LINK'] = rsselem.link
            self.rsspost['OTHER_FIELD'] = None
            self.rsspost['SOCIAL_SCORE'] = 0
            self.rsspost['CREATE_TIME'] = parseTime(rsselem.published)
            if self.rsspost['LINK']!=None and len(self.rsspost['LINK'])>0: self.getcontent(Acc['TAG_LIMIT'])
            if self.rsspost['IMAGE_LINK']!=None and len(self.rsspost['IMAGE_LINK'])>0: self.withimglink()
            logging.info('Puller: @%s | new feed %s'%(Acc['NAME'], (self.rsspost['TITLE'])[:16]))
            self.rsspost.Put()
        return

    def withimglink(self):
        try: r = requests.get(self.rsspost['IMAGE_LINK'])
        except: return
        if r.status_code!=200: return
        self.rsspost['IMAGE_FILE'] = str(time.time())+'_'+randomString(16)+'.'+self.rsspost['IMAGE_LINK'].split('?')[0].split('.')[-1].strip()
        with open(specialize_path(self.imgdir+self.rsspost['IMAGE_FILE']), 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
        return

    def getcontent(self, tag_limit):
        tag_limit = int(tag_limit)
        try: r = requests.get(self.rsspost['LINK'])
        except: return
        if r.status_code!=200: return
        htmltree = etree.HTML(r.text)
        mostptagelem = DOMparser.findelemwithmostptag(htmltree)
        if mostptagelem is None: return
        self.rsspost['CONTENT'] = '\n'.join([lxmlhtml.tostring(child) for child in mostptagelem if (child.tag=='p') and (child.text is not None) and ('Like Us on' not in child.text)])
        try: self.rsspost['CONTENT'] = self.rsspost['CONTENT'].encode('ascii','ignore')
        except: self.rsspost['CONTENT'] = ''
        tag_list = Tags.ParseTags(self.rsspost['CONTENT'])
        tag_list.extend(Tags.ParseTags(self.rsspost['TITLE']))
        if tag_list is not None and len(tag_list)>0 and tag_limit>0:
           self.rsspost['TAG'] = ','.join(tag_list[:tag_limit])
        self.withhtmltree(htmltree)
        return
        
    def withhtmltree(self, htmltree):
        pass
        return

class myrsshand(basicrsshand):
    """docstring for myrsshand"""
    def __init__(self):
        super(myrsshand, self).__init__()

