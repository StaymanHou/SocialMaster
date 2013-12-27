# coding: utf-8

from basic_posterhandler import *
import time
from time import sleep
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import traceback
from ..MyQueue import *
from ..RssPost import *
from ..Tags import *
from ..MyDict import STATUS_DICT

class handler(basicposterhandler):

    def __init__(self):
        super(handler, self).__init__()
        self.module_name = 'facebook'

    # override
    def auto_mode_handle(self, acc, accset, am):
        if am['id']==1:
            return
        elif am['id']==2:
            myqueue = MyQueue()
            myqueue.GetPendingFirst(accset['id'])
            if myqueue['id'] is not None: return
            lastrp = RssPost.GetLatest(acc['id'], accset['smodule_id'])
            if lastrp['id'] is None: return
            myqueue['status_id'] = STATUS_DICT['Pending']
            myqueue['acc_setting_id'] = accset['id']
            myqueue['post_type'] = 2
            myqueue['title'] = lastrp['title']
            myqueue['content'] = lastrp['title']
            myqueue['tags'] = lastrp['tags']
            myqueue['link'] = lastrp['link']
            myqueue['image_file'] = lastrp['image_file']
            myqueue['image_link'] = lastrp['image_link']
            myqueue['pool_post_id'] = lastrp['id']
            if (myqueue['image_file'] is None) or (myqueue['image_file']==''): myqueue['post_type'] = 1
            myqueue.save()
            return
        else:
            pass
        return

    # override
    def post_handle(self, accset, queueitem, imgdir, load_iteration=1):
        # check required accset['other_setting']
        if 'page_path' not in accset['other_setting'] or not accset['other_setting']['page_path'].strip():
            logging.warning('facebook post handle page_path not specified! e.g. (https://m.facebook.com)"/pages/Staymancom/203819689790928"')
            return 0
        if 'page_id' not in accset['other_setting'] or not str(accset['other_setting']['page_id']).strip():
            logging.warning('facebook post handle page_id not specified! e.g. "203819689790928"')
            return 0

        flag_close_browser = False
        if (queueitem['post_type']==2) and (queueitem['image_file'] is not None) and (queueitem['image_file'].strip()!=''):
            pass
        else:
            self.browser = webdriver.Firefox()
            flag_close_browser = True
        try:
            self.inner_handle(accset, queueitem, imgdir, load_iteration)
        except Exception:
            logging.warning('post handle error: %s'%str(traceback.format_exc()))
            return 0
        else:
            return 1
        finally:
            if flag_close_browser:
                self.browser.quit()

    def inner_handle(self, accset, queueitem, imgdir, load_iteration=1):
        if (queueitem['post_type']==2) and (queueitem['image_file'] is not None) and (queueitem['image_file'].strip()!=''):
            # type image
            
            imgfile = open(imgdir+queueitem['image_file'], 'rb')

            # get login page
            s = requests.Session()
            url = 'https://m.facebook.com/login.php'
            r = s.get(url)
            htmltree = etree.HTML(r.text.encode('ascii', 'ignore'))
            elems = htmltree.xpath('//input[@name="lsd"]')
            if len(elems) == 0:
                raise Exception('facebook login error: lsd not found.')
            lsd = elems[0].attrib['value']
            elems = htmltree.xpath('//input[@name="li"]')
            if len(elems) == 0:
                raise Exception('facebook login error: li not found.')
            li = elems[0].attrib['value']
            sleep(load_iteration)

            # post login
            url = 'https://m.facebook.com/login.php?refsrc=https%3A%2F%2Fm.facebook.com%2Flogin.php&refid=9'
            payload = {'width': 0,
                        'version': 1,
                        'signup_layout': 'layout|bottom_clean||wider_form||prmnt_btn|special||st|create||header_crt_acct_button||hdbtn_color|green||signupinstr||launched_Mar3',
                        'pxr': 0,
                        'pass': accset['password'],
                        'm_ts': int(time.time()),
                        'lsd': lsd,
                        'login': 'Log In',
                        'li': li,
                        'gps': 0,
                        'email': accset['username'],
                        'charset_test': '€,´,€,´,水,Д,Є',
                        'ajax': 0}
            r = s.post(url, data=payload)
            if r.status_code!=200:
                raise Exception('facebook post handle unexpected response: %s : %s'%(url, r.status_code))
            sleep(load_iteration)

            # switch to page
            url = 'https://m.facebook.com' + accset['other_setting']['page_path'].strip()
            r = s.get(url)
            if r.status_code!=200:
                raise Exception('facebook post handle unexpected response: %s : %s'%(url, r.status_code))
            htmltree = etree.HTML(r.text.encode('ascii', 'ignore'))
            elems = htmltree.xpath('//a[text()="Change"]')
            if len(elems) == 0:
                raise Exception('facebook switch page error: a[text()="Change"] not found.')
            url = 'https://m.facebook.com' + elems[0].attrib['href']
            elems = htmltree.xpath('//a[text()="Change"]')
            if len(elems) == 0:
                raise Exception('facebook switch page error: a[text()="Change"] not found.')
            url = 'https://m.facebook.com' + elems[0].attrib['href']
            voice_flag = False
            elems = htmltree.xpath('//span[@class="name" and contains(text(), "%s")]'%accset['other_setting']['page_name'])
            if len(elems) == 0:
                voice_flag = True

            # act as page
            if voice_flag:
                r = s.get(url)
                if r.status_code!=200:
                    raise Exception('facebook post handle unexpected response: %s : %s'%(url, r.status_code))

            # photo post
            url = 'https://m.facebook.com/photos/upload/?upload_source=advanced_composer&max_allowed=3&target_id=%s&ref=hl'%accset['other_setting']['page_id']
            r = s.get(url)
            if r.status_code!=200:
                raise Exception('facebook post handle unexpected response: %s : %s'%(url, r.status_code))
            htmltree = etree.HTML(r.text.encode('ascii', 'ignore'))
            elems = htmltree.xpath('//input[@name="fb_dtsg"]')
            if len(elems) == 0:
                raise Exception('facebook photo post error: fb_dtsg not found.')
            fb_dtsg = elems[0].attrib['value']
            elems = htmltree.xpath('//input[@name="return_uri"]')
            if len(elems) == 0:
                raise Exception('facebook photo post error: return_uri not found.')
            return_uri = elems[0].attrib['value']
            elems = htmltree.xpath('//input[@name="return_uri_error"]')
            if len(elems) == 0:
                raise Exception('facebook photo post error: return_uri_error not found.')
            return_uri_error = elems[0].attrib['value']
            elems = htmltree.xpath('//form[@method="post"]')
            if len(elems) == 0:
                raise Exception('facebook photo post error: form not found.')
            url = elems[0].attrib['action']

            # commit post
            content = addhashtag(queueitem['content'], queueitem['tags'], mode = 1) + '\n\nRead more:\n' + queueitem['link']
            payload = {'fb_dtsg': fb_dtsg,
                        'charset_test': '€,´,€,´,水,Д,Є',
                        'caption': content,
                        'return_uri': return_uri,
                        'return_uri_error': return_uri_error,
                        'target': accset['other_setting']['page_id'],
                        'ref': 'm_upload_pic',
                        'album_fbid': ''}
            files = {'file1': imgfile}
            r = s.post(url, data=payload, files=files)
            if r.status_code!=200:
                raise Exception('facebook post handle unexpected response: %s : %s'%(url, r.status_code))

        else:
            # type link
            
            # login
            self.browser.get('http://facebook.com')
            sleep(load_iteration)
            elem = self.browser.find_element_by_id('email')
            elem.send_keys(accset['username'])
            elem = self.browser.find_element_by_id('pass')
            elem.send_keys(accset['password'])
            elem = self.browser.find_element_by_xpath('//*[@id="loginbutton"]')
            elem.click()
            sleep(load_iteration)
            # switch identity
            elem = self.browser.find_element_by_id('userNavigationLabel')
            elem.click()
            elem = self.browser.find_element_by_xpath('//a[./div/div/div/text()="%s"]'%str(accset['other_setting']['page_name']))
            elem.click()
            sleep(load_iteration)
            # self.browser.get('https://www.facebook.com'+accset['other_setting']['page_path'].strip())
            # sleep(load_iteration)
            # voice_flag = False
            # try: elem = self.browser.find_element_by_xpath('//div[@class="pagesVoiceBarText" and contains(text(),"%s")]'%accset['other_setting']['page_name'])
            # except: voice_flag = True

            # if voice_flag:
            #     elem = self.browser.find_element_by_xpath('//span[@class="pagesAltVoiceText fwb"]/a')
            #     elem.click()
            #     sleep(load_iteration)

            # post
            sleep(10)
            elems = self.browser.find_elements_by_xpath('//textarea[@name="xhpc_message"]')
            # elems = self.browser.find_elements_by_xpath('//textarea[@aria-label="Write something..."]')
            elem = None
            for e in elems:
                if e.is_displayed():
                    elem = e
                    break
            if elem is None:
                raise Exception('facebook post handle error: can\'t find //textarea[@name="xhpc_message"]')
            elem.click()
            sleep(load_iteration)
            elem.send_keys(queueitem['link'])
            elem.send_keys(Keys.ENTER)
            sleep(10)
            elem.clear()
            content = addhashtag(queueitem['content'], queueitem['tags'], mode = 1)
            elem.send_keys(content)
            elems = self.browser.find_elements_by_xpath('//button[text()="Post"]')
            elem = None
            for e in elems:
                if e.is_displayed():
                    elem = e
                    break
            if elem is None:
                raise Exception('facebook post handle error: can\'t find //button[text()="Post"]')
            elem.click()
            # check success
            sleep(10)
            elem = self.browser.find_element_by_xpath('//abbr[contains(text(), "seconds ago")]')


        
