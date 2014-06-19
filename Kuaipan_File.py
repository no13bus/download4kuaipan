#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Kuaipan
import pprint
import platform
import asyncore
import pyinotify
import time
from config import *

sysstr = platform.system()

''' Make sure we are running in UTF-8 encoding by default '''
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

''' Get main instance for file operation '''
kuaipan_file = Kuaipan.KuaipanFile(consumer_key, consumer_secret, oauth_token, oauth_token_secret)

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_ATTRIB  # watched events
path_name = ''

class EventHandler(pyinotify.ProcessEvent):
	def process_IN_CLOSE_WRITE(self, event):
		print "IN_CLOSE_WRITE:", event.pathname
		global path_name
		path_name = event.pathname
	def process_IN_ATTRIB(self, event):
		print "IN_ATTRIB:", event.pathname
		global path_name
		if path_name==event.pathname:
			time.sleep(0.5)
			myfilename = event.pathname.split('/')[-1]#文件名字 不包括路径  event.pathname是文件名字+路径
			myfile_kuaipan = '/'+kuaipan_dir+'/'+myfilename#myfile_kuaipan是在快盘里面要存储的路径+文件名
			pprint.pprint(kuaipan_file.upload_file(event.pathname, kuaipan_path=myfile_kuaipan, ForceOverwrite=True))

notifier = pyinotify.AsyncNotifier(wm, EventHandler())
wdd = wm.add_watch(download_dir, mask, rec=True)

asyncore.loop()