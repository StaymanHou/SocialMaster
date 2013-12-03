from basic_posterhandler import *
import time
from time import sleep
import urllib
import requests
import re
import logging
import json
import traceback
from ..MyQueue import *
from ..RssPost import *
from ..Tags import *
from ..MyDict import STATUS_DICT

def recfindboard(jsonobj):
    board_dict = {}
    if isinstance(jsonobj, list):
        for child in jsonobj:
            board_dict.update(recfindboard(child))
    elif isinstance(jsonobj, dict):
        if 'board_name' in jsonobj and 'board_id' in jsonobj:
            board_dict.update({jsonobj['board_name']: jsonobj['board_id']})
        for child in jsonobj.values():
            board_dict.update(recfindboard(child))
    else: pass
    return board_dict

class handler(basicposterhandler):

    def __init__(self):
        super(handler, self).__init__()
        self.module_name = 'pinterest'

    # override
    def auto_mode_handle(self, acc, accset, am):
        if am['id']==1:
            return
        elif am['id']==2:
            myqueue = MyQueue()
            myqueue.GetPendingFirst(accset['id'])
            if myqueue['id'] is not None: return
            lastrp = RssPost.GetLatest(acc['id'], accset['smodule_id'], require_image=True)
            if lastrp['id'] is None: return
            myqueue['status_id'] = STATUS_DICT['Pending']
            myqueue['acc_setting_id'] = acc['id']
            myqueue['post_type'] = 2
            myqueue['title'] = lastrp['title']
            myqueue['content'] = lastrp['description']
            myqueue['tags'] = lastrp['tags']
            myqueue['link'] = lastrp['link']
            myqueue['image_file'] = lastrp['image_file']
            myqueue['image_link'] = lastrp['image_link']
            myqueue['pool_post_id'] = lastrp['id']
            myqueue.save()
            return
        else:
            pass
        return

    # override
    def post_handle(self, accset, queueitem, imgdir, load_iteration=1):
        try:
            self.inner_handle(accset, queueitem, imgdir, load_iteration)
        except Exception:
            logging.warning('post handle error: %s'%str(traceback.format_exc()))
            return 0
        else:
            return 1

    def inner_handle(self, accset, queueitem, imgdir, load_iteration=1):
        s = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0'}
        # visit login page
        url = 'https://www.pinterest.com/login'
        r = s.get(url, headers=headers)
        if r.status_code!=200:
            raise Exception('unexpected response: %s : %s'%(url, r.status_code))
        m = re.search('{"app_version": "(.+?)",', r.text)
        if m is None:
            raise Exception('login error: app_version not found.')
        app_version = m.group(1)
        headers['X-NEW-APP'] = 1
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Pragma'] = 'no-cache'
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['X-CSRFToken'] = r.cookies.get_dict()['csrftoken']
        sleep(load_iteration)
        # login
        url = 'https://www.pinterest.com/resource/UserSessionResource/create/'
        payload = 'data={"options":{"username_or_email":"'+accset['username']+'","password":"'+accset['password']+'"},"context":{"app_version":"'+app_version+'"}}&source_url=/login/&module_path=App()>LoginPage()>Login()>Button('
        payload = urllib.quote_plus(payload).replace('%28','(').replace('%29',')').replace('%3D','=').replace('%26','&')+'class_name%3Dprimary%2C+text%3DLog+in%2C+type%3Dsubmit%2C+tagName%3Dbutton%2C+size%3Dlarge)'
        headers['Referer'] = 'https://www.pinterest.com/login'
        r = s.post(url, data=payload, headers=headers)
        if r.status_code!=200:
            raise Exception('unexpected response: %s : %s'%(url, r.status_code))
        logindata = json.loads(r.text)
        username = logindata['resource_response']['data']['username']
        sleep(load_iteration)
        # retreive board_id from board_name
        url = '?data='+urllib.quote_plus('{"options":{},"module":{"name":"UserBoards","options":{"username":"'+username+'","secret_board_count":0},"append":false,"errorStrategy":2},"context":{"app_version":"'+app_version+'"}}')
        url += '&source_url='+urllib.quote_plus('/'+username+'/boards/')
        url += '&module_path='+urllib.quote_plus('App()>Header()>UserMenu(resource=UserResource(username='+username+'))>Dropdown()>UserDropdown()>List(items=[object Object],[object Object],[object Object],[object Object],[object Object],[object Object],[object Object], tagName=ul)').replace('%28','(').replace('%29',')')
        url += '&_='+str(int(1000*time.time()))
        url = 'http://www.pinterest.com/resource/NoopResource/get/'+url
        headers['Referer'] = 'http://www.pinterest.com/'+username+'/boards/'
        r = s.get(url, headers=headers)
        if r.status_code!=200:
            raise Exception('unexpected response: %s : %s'%(url, r.status_code))
        boarddata = json.loads(r.text)
        board_dict = recfindboard(boarddata)
        if len(board_dict)==0:
            raise Exception('can\'t find any board')
        board_id = board_dict.values()[0]
        if 'board_name' in accset['other_setting'] and accset['other_setting']['board_name'] in board_dict:
            board_id = board_dict[accset['other_setting']['board_name']]
        if 'board_name' in queueitem['other_field'] and queueitem['other_field']['board_name'] in board_dict:
            board_id = board_dict[queueitem['other_field']['board_name']]
        # pin
        description = ''
        if queueitem['title'] is not None and len(queueitem['title'].strip())>0: description += addhashtag(queueitem['title'], queueitem['tags'], mode = 1)+' '
        # removed according to  the customers request: if queueitem['content'] is not None and len(queueitem['content'].strip())>0: description += addhashtag(queueitem['content'], queueitem['tags'])+' | '
        link = str(queueitem['link'])
        description += 'More: '+link
        image_link = queueitem['image_link']
        url = 'http://www.pinterest.com/resource/PinResource/create/'
        urlencodedlink = urllib.quote_plus(link)
        payload = {'data':{'options':{'board_id': board_id.encode('ascii','replace'),
                                      'description': description.replace('\'','%27'),
                                      'link': link,
                                      'image_url': image_link.encode('ascii','replace'),
                                      'method': 'scraped'},
                           'context':{'app_version': app_version.encode('ascii','replace')}},
                   'source_url': '/pin/find/?url='+urlencodedlink,
                   'module_path':'App()>ImagesFeedPage(resource=FindPinImagesResource(url='+link+'))>Grid()>GridItems()>Pinnable()>ShowModalButton(module=PinCreate)#Modal(module=PinCreate())'}
        headers['Referer'] = 'http://www.pinterest.com/pin/find/?url='+urlencodedlink
        r = s.post(url, data=urllib.urlencode(payload).replace('%22','%5C%22').replace('%27','%22').replace('%2527','%27'), headers=headers)           
        if r.status_code!=200:
            raise Exception('unexpected response: %s : %s'%(url, r.status_code))
        if r.text.endswith('"error": null}}'): return
        raise Exception('unexpected response: %s : %s'%(url, r.text.encode('ascii','replace')))

