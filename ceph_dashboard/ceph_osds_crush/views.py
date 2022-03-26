# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from django.conf import settings
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from ceph_dashboard.ceph_auth.ceph_auth import ceph_auth


class osdCrush(APIView):
    def __init__(self):
        self.session = requests.session()
        self.osds = self.session.get(
            urljoin(settings.CEPH_URL, 'crush_map/osd_crush_map'), headers=ceph_auth().get_token())

    # 处理crush 格式形成text文件
    def crush_to_text(self, data):
        crush_map = self.session.post(urljoin(
            settings.CEPH_URL, 'crush_map/osd_new_crush'), headers=ceph_auth().get_token(), data=data)
        return crush_map.json()

    def get(self, rquest, format=None):
        osds_data = self.osds.json()

        # print(osds_data['health])
        return Response(osds_data)

    def post(self, request, format=None):
        data = json.dumps(request.data)
        crush_status = self.crush_to_text(data)
        return Response(crush_status)
