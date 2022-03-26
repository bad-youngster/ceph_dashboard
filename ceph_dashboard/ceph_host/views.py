# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from django.conf import settings
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from ceph_dashboard.ceph_auth.ceph_auth import ceph_auth


class ceph_host(APIView):
    def ceph_host(self):
        session = requests.session()
        host = session.get(urljoin(settings.CEPH_URL, 'host'),
                           headers=ceph_auth().get_token())
        return host.json()

    @swagger_auto_schema(operation_summary="获取主机信息")
    def get(self, reques, format=None):
        return Response(self.ceph_host())

