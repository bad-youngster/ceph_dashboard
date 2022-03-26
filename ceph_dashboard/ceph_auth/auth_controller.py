# -*- coding: utf-8 -*-
from django.conf import settings
import requests
import json

from urllib.parse import urljoin
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

# 连接ceph集群


class AuthCeph(APIView):

    def __init__(self):
        # 获取ceph jwt token
        self.ceph_url = settings.CEPH_URL
        self.ceph_args = {
            'username': settings.CEPH_USER,
            'password': settings.CEPH_PASSWORD
        }
        # session会话保持
        self.session = requests.session()
        # 配置头文件
        self.header = {
            'Content-Type': 'application/json'
        }
        # 连接
        self.Request = self.session.post(
            url=urljoin(self.ceph_url, 'auth'), data=json.dumps(self.ceph_args), headers=self.header)
        # 获取token
        self.ceph_token = json.loads(self.Request.text)['token']

        self.ceph_auth = {
            'Authorization': 'Bearer' + ' ' + self.ceph_token
        }

    @swagger_auto_schema(operation_summary="获取ceph auth token")
    def post(self, *args, **kwargs):
        # 获取token
        token = self.ceph_auth
        return Response(token)
