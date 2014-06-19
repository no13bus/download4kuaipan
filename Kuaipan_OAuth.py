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
# @file: Kuaipan_OAuth.py
# @date: 2013-11-7

'''
This example implements Kuaipan OAuth. (http://www.kuaipan.cn/developers/document_oauth.htm)

Requirement :
    * Python oauth2 (https://pypi.python.org/pypi/oauth2/)
    * Python poster (https://pypi.python.org/pypi/poster/)

Howto -
Step 1:
    Set proper "consumer_key" and "consumer_secret" for your account
    You may get "consumer_key" and "consumer_secret" at URL "http://www.kuaipan.cn/developers/list.htm"

Step 2:
    Run "python Kuaipan_OAuth.py" in your environment

Step 3:
    If you work on Windows system, the authentication URL would be open in you default browser directly. Otherwise, you should copy/paste the URL printed on console screen.

Step 4:
    If everything work well, you should get the autenticated key-paire at final step.

'''


# For both Python 2.x and 3.x
try:
    read_input = raw_input
except NameError:
    read_input = input
###############################################

import Kuaipan

consumer_key = 'xcq3lc7bWR1RMI8A'
consumer_secret = '8uKHM7lLyE9CCAFM'

kuaipan_oauth = Kuaipan.KuaipanOAuth(consumer_key, consumer_secret)

# Step 1: Get a request token. This is a temporary token that is used for
# having the user authorize an access token and to sign the request to obtain
# said access token.
request_token = kuaipan_oauth.GetRequestToken()
print "Request Token:"
print "    - oauth_token        = %s" % request_token['oauth_token']
print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
print

# Step 2: Redirect to the provider. Since this is a CLI script we do not
# redirect. In a web application you would redirect the user to the URL
# below.
print "Go to the following link in your browser:"
print kuaipan_oauth.AuthenticationUrl
print

# Opne URL in your default browser (For Windows only)
import platform
if cmp(platform.system(), "Windows")==0 :
    import webbrowser
    webbrowser.open(kuaipan_oauth.AuthenticationUrl)

# After the user has granted access to you, the consumer, the provider will
# redirect you to whatever URL you have told them to redirect to. You can
# usually define this in the oauth_callback argument as well.
accepted = 'n'
while accepted.lower() == 'n':
    accepted = read_input('Have you authorized me? (y/n) ')
oauth_verifier = read_input('What is the PIN? ')

# Step 3: Once the consumer has redirected the user back to the oauth_callback
# URL you can request the access token the user has approved. You use the
# request token to sign this request. After this is done you throw away the
# request token and use the access token returned. You should store this
# access token somewhere safe, like a database, for future use.

access_token = kuaipan_oauth.GetAccessToken(oauth_verifier)

print "Access Token:"
print "    - oauth_token        = %s" % access_token['oauth_token']
print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
print
print "You may now access protected resources using the access tokens above."
print
