#coding: utf-8
from config import *
from fabric.api import local,cd,run,env

env.hosts=['user@ip:22',] #写上自己的vps的ip和用户
env.password = 'pwd' #写上vps用户的密码

# youtube的网址里面出现的=要变成\= 否则fabric无法解析 不知道为什么
def dl(url):
    with cd(download_dir):
    	cmd = 'youtube-dl --max-quality FORMAT %s' % url
        run(cmd)  #远程操作用run

def wget(url):
	with cd(download_dir):
		cmd = 'wget -c %s' % url
		run(cmd)