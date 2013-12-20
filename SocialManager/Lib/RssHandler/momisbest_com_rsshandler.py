from basic_rsshandler import *

class myrsshand(basicrsshand):

    # override
    def handle(self, d, Acc, domain, imgdir):
        self.imgdir = imgdir
        last_update = Acc['last_update']
        self.site = Site.GetOrCreate(domain)
        for rsselem in d.entries:
            t = rsselem.published
            t = parseTime(t)
            if t < last_update: continue
            self.rsspost['account_id'] = Acc['id']
            self.rsspost['site_id'] = self.site['id']
            try: self.rsspost['title'] = rsselem.title.encode('ascii','ignore')
            except: self.rsspost['title'] = ''
            try: self.rsspost['description'] = rsselem.summary.encode('ascii','ignore')
            except: self.rsspost['description'] = ''
            self.rsspost['content'] = ''
            self.rsspost['tags'] = ''
            self.rsspost['image_file'] = None
            m = re.search('src="([^"]+?)"', rsselem.summary.encode('ascii','ignore'))
            if m is None:
                self.rsspost['image_link'] = None
            else:
                self.rsspost['image_link'] = m.group(1)
            self.rsspost['link'] = rsselem.link
            self.rsspost['social_score'] = 0
            self.rsspost['created_at'] = parseTime(rsselem.published)
            if self.rsspost['link']!=None and len(self.rsspost['link'])>0: self.getcontent(Acc['tag_limit'])
            if self.rsspost['image_link']!=None and len(self.rsspost['image_link'])>0: self.withimglink()
            logging.info('Puller: @%s | new feed %s'%(Acc['name'], (self.rsspost['title'])[:16]))
            self.rsspost.Put()
        return
