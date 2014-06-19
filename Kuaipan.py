#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Deren Wu <deren.g@gmail.com> (author).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# @file: Kuaipan.py
# @date: 2013-11-7

'''
支援金山快盘 Open API 操作

Core lib for Kuaipan implementation. (http://www.kuaipan.cn/developers)

Requirement :
    * Python oauth2 (https://pypi.python.org/pypi/oauth2/)
    * Python poster (https://pypi.python.org/pypi/poster/)

'''

__author__ = 'deren.g@gmail.com (Deren Wu)'

import os, sys
import oauth2 as oauth
import urllib
import urllib2
import poster
import json

class Kuaipan(object):
    """docstring for Kuaipan"""
    def __init__(self):
        super(Kuaipan, self).__init__()

class KuaipanFile(object):
    """
    Support all functions for Kuaipan fileops. You may add/delete/remove/edit your file on Kuaipan with simple functino calls

    Example:

    If you want to get your account info, write down codes as below.

        kuaipan_file = Kuaipan.KuaipanFile(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
        print kuaipan_file.account_info()

    PS : Before file operation, please get your oauth_token/oauth_token_secret first. (Refer to Kuaipan_OAuth.py)

    """
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        super(KuaipanFile, self).__init__()
        self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        self.token = oauth.Token(oauth_token, oauth_token_secret)
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)

    def SetUrlHandler(self, UsePoster=False, UseCookie=False, PacketDebug=False):
        opener = urllib2._opener
        if opener == None:
            #opener = urllib2.OpenerDirector()
            opener = urllib2.build_opener()
            '''
            opener.add_handler(urllib2.ProxyHandler())
            opener.add_handler(urllib2.UnknownHandler())
            opener.add_handler(urllib2.HTTPHandler())
            opener.add_handler(urllib2.HTTPDefaultErrorHandler())
            opener.add_handler(urllib2.HTTPSHandler())
            opener.add_handler(urllib2.HTTPErrorProcessor())
            '''

        if UseCookie is True:
            opener.add_handler(urllib2.HTTPCookieProcessor())
            #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

        if PacketDebug is True:
            opener.add_handler(urllib2.HTTPHandler(debuglevel=1))
            opener.add_handler(urllib2.HTTPSHandler(debuglevel=1))
            #opener = urllib2.build_opener(httpHandler, httpsHandler)

        if UsePoster is True:
            from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
            opener.add_handler(StreamingHTTPHandler())
            opener.add_handler(StreamingHTTPRedirectHandler())
            opener.add_handler(StreamingHTTPSHandler())
        urllib2.install_opener(opener)
        return opener

    def GetOauthUrl(self, url, method='GET', parameters=None):
        oauth_request = oauth.Request.from_consumer_and_token(self.consumer,
                                                                    token=self.token,
                                                                    http_method=method,
                                                                    http_url=url,
                                                                    parameters=parameters,
                                                                    is_form_encoded=True)
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
        return oauth_request.to_url()

    def DoHttpRequst(self, url):
        response = urllib2.urlopen(url)
        if response.code != 200:
            raise Exception("Invalid response %s." % vars(response))
        content = response.read()
        return content

    def oauth_http_and_json_parse(self, url, method='GET', parameters=None):
        oauth_url = self.GetOauthUrl(url, method=method, parameters=parameters)
        content = self.DoHttpRequst(oauth_url)
        return KuaipanUtil.json_decoder(content)


    def account_info(self):
        """
        Description : 查看用户信息
        Reference link :
            http://www.kuaipan.cn/developers/document_apiinfo.htm
        """
        url = 'http://openapi.kuaipan.cn/1/account_info'
        return self.oauth_http_and_json_parse(url, method='GET', parameters=None)

    def metadata(self, filepath, root='app_folder', \
                                    list=None, \
                                    file_limit=None, \
                                    page=None, \
                                    page_size=None, \
                                    filter_ext=None, \
                                    sort_by=None):
        """
        Description : 获取单个文件，文件夹信息
        Reference link :
            http://www.kuaipan.cn/developers/document_apimetadata.htm
        """
        url = 'http://openapi.kuaipan.cn/1/metadata/%s/%s'
        url = url % (root, filepath)
        parameters = {}
        if list != None:
            parameters['list'] = list
        if file_limit != None:
            parameters['file_limit'] = file_limit
        if page != None:
            parameters['page'] = page
        if page_size != None:
            parameters['page_size'] = page_size
        if filter_ext != None:
            parameters['filter_ext'] = filter_ext
        if sort_by != None:
            parameters['sort_by'] = sort_by
        return self.oauth_http_and_json_parse(url, method='GET', parameters=None)

    def history(self, path, root='app_folder'):
        """
        Description : 文件的历史版本
        Reference link :
            http://www.kuaipan.cn/developers/document_apihistory.htm
        """
        url = 'http://openapi.kuaipan.cn/1/history/%s/%s'
        url = url % (root, path)
        return self.oauth_http_and_json_parse(url, method='GET', parameters=None)

    def fileops_create_folder(self, path, root='app_folder'):
        """
        Description : 新建文件夹
        Reference link :
            http://www.kuaipan.cn/developers/document_apicreate.htm
        """
        url = 'http://openapi.kuaipan.cn/1/fileops/create_folder'
        parameters = {}
        parameters['root'] = root
        parameters['path'] = path
        return self.oauth_http_and_json_parse(url, method='GET', parameters=parameters)

    def fileops_delete(self, path, root='app_folder', to_recycle=True):
        """
        Description : 删除文件，文件夹，以及文件夹下所有文件到回收站。删除有风险，操作需谨慎。
        Reference link :
            http://www.kuaipan.cn/developers/document_apidelete.htm
        """
        url = 'http://openapi.kuaipan.cn/1/fileops/delete'
        parameters = {}
        parameters['root'] = root
        parameters['path'] = path
        parameters['to_recycle'] = to_recycle
        return self.oauth_http_and_json_parse(url, method='GET', parameters=parameters)

    def fileops_move(self, from_path, to_path, root='app_folder'):
        """
        Description : 移动文件，文件夹，不能移动带共享的文件，当然也不支持其他不能移动的情况（如形成环路）
        Reference link :
            http://www.kuaipan.cn/developers/document_apimove.htm
        """
        url = 'http://openapi.kuaipan.cn/1/fileops/move'
        parameters = {}
        parameters['root'] = root
        parameters['from_path'] = from_path
        parameters['to_path'] = to_path
        return self.oauth_http_and_json_parse(url, method='GET', parameters=parameters)

    def fileops_copy(self, from_path, to_path, root='app_folder', from_copy_ref=None):
        """
        Description : 复制文件，文件夹
        Reference link :
            http://www.kuaipan.cn/developers/document_apicopy.htm
        """
        url = 'http://openapi.kuaipan.cn/1/fileops/copy'
        parameters = {}
        parameters['root'] = root
        parameters['from_path'] = from_path
        parameters['to_path'] = to_path
        if from_copy_ref != None:
            parameters['from_copy_ref'] = from_copy_ref
        return self.oauth_http_and_json_parse(url, method='GET', parameters=parameters)

    def fileops_thumbnail(self, width, height, path, root='app_folder'):
        """
        Description : 缩略图
        Reference link :
            http://www.kuaipan.cn/developers/document_apithumbnail.htm
        """
        url = 'http://conv.kuaipan.cn/1/fileops/thumbnail'
        parameters = {}
        parameters['root'] = root
        parameters['path'] = path
        parameters['width'] = width
        parameters['height'] = height
        oauth_url = self.GetOauthUrl(url, method='GET', parameters=parameters)
        self.SetUrlHandler(UseCookie=True)
        content = self.DoHttpRequst(oauth_url)
        return content

    def fileops_documentView(self, path, root='app_folder', view='normal', type=None, zip=0):
        """
        Description : 文档转换產生網頁預覽圖
        Reference link :
            http://www.kuaipan.cn/developers/document_apidocview.htm
        """
        url = 'http://conv.kuaipan.cn/1/fileops/documentView'
        parameters = {}
        parameters['root'] = root
        parameters['path'] = path
        parameters['view'] = view
        parameters['zip'] = zip
        parameters['type'] = type
        if parameters['type']==None:
            parameters['type'] = os.path.splitext(path)[1].split('.')[-1]
        oauth_url = self.GetOauthUrl(url, method='GET', parameters=parameters)
        self.SetUrlHandler(UseCookie=True)
        content = self.DoHttpRequst(oauth_url)
        return content

    def copy_ref(self, filepath, root='app_folder'):
        """
        Description : 产生一个复制引用（ref），别的帐号可以使用这个引用作为copy接口的参数来复制文件。复制的版本是文件的最新版本，与引用产生的时间无关。
        Reference link :
            http://www.kuaipan.cn/developers/document_apicopyref.htm
        """
        url = 'http://openapi.kuaipan.cn/1/copy_ref/%s/%s'
        url = url % (root, filepath)
        return self.oauth_http_and_json_parse(url, method='GET', parameters=None)

    def shares(self, filepath, root='app_folder', name=None, access_code=None):
        """
        Description : 创建并获取一个文件的分享链接。发布外链的文件会接受审核。
        Reference link :
            http://www.kuaipan.cn/developers/document_apishare.htm
        """
        url = 'http://openapi.kuaipan.cn/1/shares/%s/%s'
        url = url % (root, filepath)
        parameters = {}
        if name != None:
            parameters['name'] = name
        if access_code != None:
            parameters['access_code'] = access_code
        return self.oauth_http_and_json_parse(url, method='GET', parameters=parameters)

    def upload_file(self, localfile, kuaipan_path, ForceOverwrite=True):
        """
        Description : 上传文件
        Args:
            localfile: 本地文件路径
            kuaipan_path: 快盘的路径
        Reference link :
            http://www.kuaipan.cn/developers/document_apiupload.htm
        """
        url = '%s1/fileops/upload_file'
        url = url % (self.upload_locate()['url'])
        parameters = {'path': kuaipan_path,
                        'root': 'app_folder',
                        'overwrite' : ForceOverwrite
                    }
        target_url = self.GetOauthUrl(url, method='POST', parameters=parameters)
        #poster.streaminghttp.register_openers()
        self.SetUrlHandler(UsePoster=True)
        data, headers = poster.encode.multipart_encode({"file": open(localfile, "rb")})
        request = urllib2.Request(target_url, data=data, headers=headers)
        try:
            response = urllib2.urlopen(request)
            content = response.read()
            if response.code != 200:
                raise Exception("Invalid response %s." % vars(response))
        except urllib2.HTTPError, error:
            content = error.read()
            raise Exception("urllib2.HTTPError %s." % content)
        return KuaipanUtil.json_decoder(content)

    def upload_locate(self):
        """
        Description : 获取文件上传地址
        Reference link :
            http://www.kuaipan.cn/developers/document_apiupload.htm
        """
        url = 'http://api-content.dfs.kuaipan.cn/1/fileops/upload_locate'
        return self.oauth_http_and_json_parse(url, method='GET', parameters=None)

    def download_file(self, kuaipan_filepath, root="app_folder", local_filepath=None, show_status=False): # root = app_folder or kuaipan
        """
        Description : 下载文件（支持HTTP Range Retrieval Requests）
        Reference link :
            http://www.kuaipan.cn/developers/document_apidownload.htm
        """
        url = 'http://api-content.dfs.kuaipan.cn/1/fileops/download_file'
        filename = local_filepath
        if filename is None:
            filename = os.path.basename(kuaipan_filepath)
        parameters = {'path': kuaipan_filepath,
                        'root': root}
        oauth_url = self.GetOauthUrl(url, method='GET', parameters=parameters)
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        opener = self.SetUrlHandler(UseCookie=True)
        response = opener.open(oauth_url)
        if response.code != 200:
            raise Exception("Invalid response %s." % vars(response))
        total_size = int(response.headers['content-length'])
        if show_status is True:
            print 'File length : '+str(total_size)
            sys.stdout.write('Downdloading')
        with open(filename, 'wb') as f:
            while 1:
                content = response.read(1024*8)
                if not content:
                    response.close()
                    #print
                    break
                if show_status is True:
                    sys.stdout.write('.')
                f.write(content)
        if show_status is True:
            print 'Success!'

class KuaipanUtil(object):
    """docstring for KuaipanUtil"""
    def __init__(self):
        super(KuaipanUtil, self).__init__()
    @staticmethod
    def json_decoder(value):
        json_acceptable_string = value.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        return d


class KuaipanOAuth(object):
    """docstring for KuaipanOAuth"""
    request_token_url = 'https://openapi.kuaipan.cn/open/requestToken'
    access_token_url = 'https://openapi.kuaipan.cn/open/accessToken'
    kuaipanApiUrl = 'https://www.kuaipan.cn/api.php'

    def __init__(self, consumer_key, consumer_secret):
        super(KuaipanOAuth, self).__init__()
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.client = oauth.Client(self.consumer)

    def GetRequestToken(self):
        resp, content = self.client.request(self.request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])
        self.request_token = KuaipanUtil.json_decoder(content)
        self.AuthenticationUrl = "%s?ac=open&op=authorise&oauth_token=%s" % (self.kuaipanApiUrl, self.request_token['oauth_token'])
        return self.request_token

    def GetAccessToken(self, oauth_verifier):
        token = oauth.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(self.consumer, token)
        resp, content = client.request(self.access_token_url, "GET")
        self.access_token = KuaipanUtil.json_decoder(content)
        return self.access_token
