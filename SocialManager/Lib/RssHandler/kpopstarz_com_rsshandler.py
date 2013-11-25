from basic_rsshandler import *
from lxml import etree

class myrsshand(basicrsshand):

    # override
    def withhtmltree(self, htmltree):
        #removed for ignoring the small sized image in rss
        #if self.rsspost['IMAGE_FILE'] != None:
        #    return
        elem = htmltree.xpath('//div[@class="ar_pic"]/img[1]') #article img
        if len(elem)==0: elem = htmltree.xpath('//img[@id="slides"]') #if can't find article img try photo img
        if len(elem)==0: elem = htmltree.xpath('//img[@class="imgNone"]') #if can't find photo img try imgNone
        if len(elem)==0: return #if can't find img abort
        self.rsspost['IMAGE_LINK'] = elem[0].get('src')
        return
