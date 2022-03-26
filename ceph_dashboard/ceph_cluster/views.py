# -*- coding: utf-8 -*-
from urllib.parse import urljoin
from django.conf import settings
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from ceph_dashboard.ceph_auth.ceph_auth import ceph_auth


class ceph_healths(APIView):
    def ceph_health(self):
        session = requests.session()
        health = session.get(
            urljoin(settings.CEPH_URL, 'health/minimal'), headers=ceph_auth().get_token())
        return health.json()

    @swagger_auto_schema(operation_summary="获取集群状态")
    def get(self, reques, format=None):
        data = self.ceph_health()
        ceph_health = {"hosts": data["hosts"], "health": data["health"]}
        return Response(ceph_health)
