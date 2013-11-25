from basic_posterhandler import *
import time
from time import sleep
from base64 import b64encode
import urllib
import twitter_requests
import re
import logging
from ..MyQueue import *
from ..RssPost import *
from ..Tags import *
from ..MyDict import STATUS_DICT

class handler(basicposterhandler):

    def __init__(self):
        super(handler, self).__init__()
        self.module_name = 'twitter'

    # override
    def auto_mode_handle(self, acc, accset, am):
        if am['CODE']==1:
            return
        elif am['CODE']==2:
            myqueue = MyQueue()
            myqueue.GetPendingFirst(acc['PK'], am['MODULE'])
            if myqueue['PK'] is not None: return
            lastrp = RssPost.GetLatest(acc['PK'], am['MODULE'])
            if lastrp['PK'] is None: return
            myqueue['STATUS'] = STATUS_DICT['Pending']
            myqueue['ACCOUNT'] = acc['PK']
            myqueue['MODULE'] = am['MODULE']
            myqueue['TYPE'] = 2
            myqueue['TITLE'] = lastrp['TITLE']
            myqueue['EXTRA_CONTENT'] = accset['EXTRA_CONTENT']
            myqueue['TAG'] = lastrp['TAG']
            myqueue['LINK'] = lastrp['LINK']
            myqueue['IMAGE_FILE'] = lastrp['IMAGE_FILE']
            myqueue['RSS_SOURCE_PK'] = lastrp['PK']
            if (myqueue['IMAGE_FILE'] is None) or (myqueue['IMAGE_FILE']==''): myqueue['TYPE'] = 1
            myqueue.save()
            return
        else:
            pass
        return

    # override
    def post_handle(self, accset, queueitem, imgdir, load_iteration=1):
        try:
            self.inner_handle(accset, queueitem, imgdir, load_iteration)
        except Exception, e:
            logging.warning('post handle error: %s'%str(e))
            return 0
        else:
            return 1

    def inner_handle(self, accset, queueitem, imgdir, load_iteration=1):
        # validate
        if queueitem['TYPE']==2:
            imgfile = open(imgdir+queueitem['IMAGE_FILE'], 'rb').read()

        s = twitter_requests.Session()
        url = 'https://twitter.com/login'
        r = s.get(url)
        if r.status_code!=200:
            raise Exception('unexpected response: %s : %s'%(url, r.status_code))
        # extract authenticity_token
        m = re.search('<input type="hidden" name="authenticity_token" value=".+?">',r.text)
        if m is None:
            raise Exception('login error: token not found.')
        auth_token = m.group(0)[54:-2]
        sleep(load_iteration)
        url = 'https://twitter.com/sessions'
        payload = {'session[username_or_email]': accset['USERNAME'],
                   'session[password]': accset['PSWD'],
                   'scribe_log': '',
                   'return_to_ssl': 'true',
                   'remember_me': '0',
                   'redirect_after_login:': '',
                   'authenticity_token': auth_token}
        r = s.post(url, data=payload)
        if r.status_code!=200:
            raise Exception('unexpected response: %s : %s'%(url, r.status_code))
        sleep(load_iteration)
        # type 1: text tweet
        if queueitem['TYPE']==1:
            if (queueitem['EXTRA_CONTENT'] is None or queueitem['EXTRA_CONTENT'].strip()==''):
                extra_content = ''
            else:
                extra_content = ' ' + queueitem['EXTRA_CONTENT'].strip()
            tweet_content = addhashtag(queueitem['TITLE'], queueitem['TAG'], mode = 1)
            if len(tweet_content)>=(117-len(extra_content)):
                tweet_content = tweet_content[:(113-len(extra_content))] + '... '
            url = 'https://twitter.com/i/tweet/create'
            payload = {'authenticity_token': auth_token,
                       'place_id': '',
                       'status': tweet_content+' '+queueitem['LINK']+extra_content}
            r = s.post(url, data=urllib.urlencode(payload))
            if r.status_code!=200:
                raise Exception('unexpected response: %s : %s'%(url, r.status_code))
            # type 2: tweet with image
        elif queueitem['TYPE']==2:
            if (queueitem['EXTRA_CONTENT'] is None or queueitem['EXTRA_CONTENT'].strip()==''):
                extra_content = ''
            else:
                extra_content = ' ' + queueitem['EXTRA_CONTENT'].strip()
            tweet_content = addhashtag(queueitem['TITLE'], queueitem['TAG'], mode = 1)
            if (queueitem['IMAGE_FILE'] is None) or (queueitem['IMAGE_FILE']==''):
                raise Exception('No image file specified in a image type tweet.')
            if len(tweet_content)>=(93-len(extra_content)):
                tweet_content = tweet_content[:(89-len(extra_content))] + '... '
            # for debug url = 'http://localhost'
            url = 'https://upload.twitter.com/i/tweet/create_with_media.iframe'
            payload = {'post_authenticity_token': auth_token,
                       'iframe_callback': 'window.top.swift_tweetbox_'+str(int(time.time()))+'000',
                       'in_reply_to_status_id': '',
                       'impression_id': '',
                       'earned': '',
                       'status': tweet_content+' '+queueitem['LINK']+extra_content,
                       'media_data[]': b64encode(imgfile),
                       'place_id': ''}
            files = {'media_empty': ('', '')}
            r = s.post(url, data=payload, files=files)
            if r.status_code!=200:
                raise Exception('unexpected response: %s : %s'%(url, r.status_code))
        else:
            raise Exception('wrong type: %d'%queueitem['TYPE'])
        return
