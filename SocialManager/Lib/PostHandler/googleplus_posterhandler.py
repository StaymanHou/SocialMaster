from time import sleep
from PyUserInput.pykeyboard import PyKeyboard
from basic_posterhandler import *
from selenium import webdriver
import logging
from ..MyQueue import *
from ..RssPost import *
from ..Tags import *
from ..MyDict import STATUS_DICT
from ..systemHelper import specialize_path

class handler(basicposterhandler):

	def __init__(self):
		super(handler, self).__init__()
		self.module_name = 'gplus'

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
			myqueue['acc_setting_id'] = acc['id']
			myqueue['type'] = 1
			myqueue['title'] = lastrp['title']
			myqueue['content'] = lastrp['title']
			myqueue['tags'] = lastrp['tags']
			myqueue['link'] = lastrp['link']
			myqueue['image_file'] = lastrp['image_file']
			myqueue['image_link'] = lastrp['image_link']
			myqueue['other_field'] = {}
			myqueue['pool_post_id'] = lastrp['id']
			myqueue.save()
			return
		else:
			pass
		return

	# override
	def post_handle(self, accset, queueitem, imgdir, load_iteration=1):
		self.browser = webdriver.Firefox()
		try:
			self.inner_handle(accset, queueitem, imgdir, load_iteration)
		except Exception, e:
			logging.warn('post handle error: %s'%str(e))
			return 0
		else:
			return 1
		finally:
			self.browser.quit()

	def inner_handle(self, accset, queueitem, imgdir, load_iteration=1):
		# log into page
		self.browser.get('https://accounts.google.com/ServiceLogin?hl=en&continue=https://plus.google.com'+accset['other_setting']['page_path'])
		elem = self.browser.find_element_by_id('Email')
		elem.send_keys(accset['username'])
		elem = self.browser.find_element_by_id('Passwd')
		elem.send_keys(accset['password'])
		elem = self.browser.find_element_by_id('signIn')
		elem.click()
		sleep(10)
		# switch to the Share dialog
		elem = self.browser.find_element_by_xpath('//div[text()="Share"]')
		elem.click()
		sleep(10)
		self.browser.switch_to_frame(self.browser.find_element_by_xpath('//iframe[../../div/div[1]/a/div/text()="Share"]'))
		if (queueitem['type'] == 2) and (queueitem['image_file'] is not None) and (queueitem['image_file'].strip()!=''):
			# type 2 photo
			elem = self.browser.find_element_by_xpath('//span[@title="Add photos"]')
			elem.click()
			sleep(2)
			elem = self.browser.find_element_by_xpath('//span[text()="Upload from computer"]')
			elem.click()
			sleep(1)
			k = PyKeyboard()
			k.type_string(specialize_path(imgdir+queueitem['image_file']), 0.1)
			k.tap_key(k.enter_key, 1, 0.1)
			sleep(10)
			elem = self.browser.find_element_by_xpath('//div[2][../div/text()="Share what\'s new..."]')
			content = addhashtag(queueitem['content'], queueitem['tags'], mode = 1) + '\n' + queueitem['link']
			elem.send_keys(content)
		else:
			# type 1 link
			elem = self.browser.find_element_by_xpath('//span[@title="Add link"]')
			elem.click()
			elem = self.browser.find_element_by_xpath('//input[../div/text()="Enter or paste a link"]')
			elem.send_keys(queueitem['link'])
			elem = self.browser.find_element_by_xpath('//div[text()="Add"]')
			elem.click()
			sleep(10)
			elem = self.browser.find_element_by_xpath('//div[2][../div/text()="Share what\'s new..."]')
			content = addhashtag(queueitem['content'], queueitem['tags'], mode = 1)
			elem.send_keys(content)
		# merge
		elem = self.browser.find_element_by_xpath('//div[text()="Share"]')
		elem.click()
		sleep(5)
