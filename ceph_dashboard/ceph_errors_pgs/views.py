# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from django.conf import settings
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from ceph_dashboard.ceph_auth.ceph_auth import ceph_auth


class pgsErrors(APIView):

    def __init__(self):
        self.session = requests.session()
        self.getData = self.session.get(
            urljoin(settings.CEPH_URL, 'health/minimal'), headers=ceph_auth().get_token())

    def pg_errors(self, data):
        postData = self.session.post(
            urljoin(settings.CEPH_URL, 'pg_errors/pg_error'), headers=ceph_auth().get_token(), data=data)
        return postData.json()

    def get(self, request):
        ceph_health = self.getData.json()
        ceph_health_checks = ceph_health["health"]["checks"]
        ceph_health_pg_message = []
        for i in ceph_health_checks:
            for y in i["detail"]:
                if ((y["message"]).startswith("pg")):
                    ceph_health_pg_message.append(
                        {"pgs": y["message"][3:8], "message": y["message"]})

        return Response(ceph_health_pg_message)

    def post(self, request, format=None):
        # 修复pgs errors
        # {"type":
        #
        # }
        # 回滚pgs errors
        # 删除pgs errors
        post_data = json.dumps(request.data)
        pgErrors_status = self.pg_errors(data=post_data)
        return Response(pgErrors_status)
