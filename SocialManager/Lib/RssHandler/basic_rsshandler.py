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
        last_update = Acc['last_update']
        for rsselem in d.entries:
            t = rsselem.published
            t = parseTime(t)
            if t < last_update: continue
            self.rsspost['account_id'] = Acc['id']
            try: self.rsspost['title'] = rsselem.title.encode('ascii','ignore')
            except: self.rsspost['title'] = ''
            try: self.rsspost['description'] = rsselem.summary.encode('ascii','ignore')
            except: self.rsspost['description'] = ''
            self.rsspost['content'] = ''
            self.rsspost['tags'] = ''
            self.rsspost['image_file'] = None
            if ('media_content' in rsselem) and (len(rsselem.media_content)>0) and ('url' in rsselem.media_content[0]): self.rsspost['image_link'] = rsselem.media_content[0]['url']
            else: self.rsspost['image_link'] = None
            self.rsspost['link'] = rsselem.link
            self.rsspost['social_score'] = 0
            self.rsspost['created_at'] = parseTime(rsselem.published)
            if self.rsspost['link']!=None and len(self.rsspost['link'])>0: self.getcontent(Acc['tag_limit'])
            if self.rsspost['image_link']!=None and len(self.rsspost['image_link'])>0: self.withimglink()
            logging.info('Puller: @%s | new feed %s'%(Acc['name'], (self.rsspost['title'])[:16]))
            self.rsspost.Put()
        return

    def withimglink(self):
        try: r = requests.get(self.rsspost['image_link'])
        except: return
        if r.status_code!=200: return
        self.rsspost['image_file'] = str(time.time())+'_'+randomString(16)+'.'+self.rsspost['image_link'].split('?')[0].split('.')[-1].strip()
        with open(specialize_path(self.imgdir+self.rsspost['image_file']), 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
        return

    def getcontent(self, tag_limit):
        if tag_limit: tag_limit = int(tag_limit)
        else: tag_limit = 0
        try: r = requests.get(self.rsspost['link'])
        except: return
        if r.status_code!=200: return
        htmltree = etree.HTML(r.text)
        mostptagelem = DOMparser.findelemwithmostptag(htmltree)
        if mostptagelem is None: return
        self.rsspost['content'] = '\n'.join([lxmlhtml.tostring(child) for child in mostptagelem if (child.tag=='p') and (child.text is not None) and ('Like Us on' not in child.text)])
        try: self.rsspost['content'] = self.rsspost['content'].encode('ascii','ignore')
        except: self.rsspost['content'] = ''
        tag_list = Tags.ParseTags(self.rsspost['content'])
        tag_list.extend(Tags.ParseTags(self.rsspost['title']))
        if tag_list is not None and len(tag_list)>0 and tag_limit>0:
           self.rsspost['tags'] = ','.join(tag_list[:tag_limit])
        self.withhtmltree(htmltree)
        return
        
    def withhtmltree(self, htmltree):
        pass
        return

class myrsshand(basicrsshand):
    """docstring for myrsshand"""
    def __init__(self):
        super(myrsshand, self).__init__()

