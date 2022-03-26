# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from django.conf import settings
import requests
import json


class ceph_auth:
    def __init__(self):

        # 获取ceph jwt 连接地址
        self.url = settings.CEPH_URL
        self.username = settings.CEPH_USER
        self.password = settings.CEPH_PASSWORD
        # 获取header
        self.header = {
            'Content-Type': 'application/json'
        }

        self.args = {
            'username': self.username,
            'password': self.password
        }
        # 采取session的方式
        self.session = requests.session()

        self.conn = self.session.post(
            urljoin(self.url, 'auth'), data=json.dumps(self.args), headers=self.header
        )

    def get_token(self):
        # 获取token
        ceph_token = {"Authorization": "Bearer" +
                      " " + json.loads(self.conn.text)['token']}
        # jwt health
        ceph_health = {
            "Content-Type": "application/json",
            "Authorization": ceph_token['Authorization']
        }
        
        return ceph_health