# coding: utf-8

from __future__ import absolute_import
from dropbox import client

class DropboxProvider(object):

    def __init__(self, access_token):
        self.access_token = access_token
        self.client       = client.DropboxClient(self.access_token)
        self.account_info = self.client.account_info()

    def user_id(self):
        return self.account_info['uid']

    def display_name(self):
        return self.account_info['display_name']

    def email(self):
        return self.account_info['email']
