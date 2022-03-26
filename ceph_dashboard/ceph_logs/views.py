# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from django.conf import settings
import requests
import json
import os
import paramiko
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ceph_dashboard.ceph_auth.ceph_auth import ceph_auth
from django.http import StreamingHttpResponse, JsonResponse
from django.utils.encoding import escape_uri_path
from ceph_dashboard.redis_conn.views import redisConn


class ceph_logs(APIView):
    def ceph_log(self, data):
        session = requests.session()
        logs = session.post(
            urljoin(settings.CEPH_URL, 'logs/list_log_path'), headers=ceph_auth().get_token(), data=data)
        return logs.json()

    def ceph_log_all(self):
        session = requests.session()
        log_all = session.get(urljoin(
            settings.CEPH_URL, 'logs/all_log_path'), headers=ceph_auth().get_token())

        return log_all.json()

    @swagger_auto_schema(operation_summary="获取所有日志路径")
    def get(self, request, fomat=None):
        return Response(self.ceph_log_all())

    @swagger_auto_schema(operation_summary="获取日志路径", request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'model_name': openapi.Schema(type=openapi.TYPE_STRING),
        'filter': openapi.Schema(type=openapi.TYPE_STRING)}))
    def post(self, request, fomat=None):
        data = json.dumps(request.data)
        # 获取数据
        logs = self.ceph_log(data)
        return Response(logs)


class filedownload(APIView):
    @swagger_auto_schema(operation_summary="日志下载", manual_parameters=[
        openapi.Parameter(
            name='host',
            in_=openapi.IN_QUERY,
            description='主机IP',
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            name="remote_path",
            in_=openapi.IN_QUERY,
            description='远程文件路径',
            type=openapi.TYPE_STRING
        )
    ]
    )
    def post(self, request):
        host = request.query_params.get('host')
        remote_path = request.query_params.get('remote_path')

        # 获取redis种对应的IP地址
        conn = redisConn()
        data = conn.smembers("ceph_host")
        for i in data:
            redisCephHost = eval(i.decode())
            if redisCephHost["host_name"] == host:
                data = self.sftp_download(host=redisCephHost["host_ip"], port=redisCephHost["host_port"],
                                          username=redisCephHost["host_user"], password=redisCephHost["host_pass"])
                return data
            

    def sftp_download(self, host, port, username, password, remote_path):
        """
        :param host 主机IP
        :param remote_path 远程主机路径
        """
        try:
            # 远程主机 IP地址和端口号
            sftp = paramiko.Transport(host, port)
            # 远程主机 用户名和密码
            sftp.connect(username=username, password=password)
            sftpconn = paramiko.SFTPClient.from_transport(sftp)
            remote_name = remote_path.split('/')[-1]
            local_path_name = os.path.join('/tmp', remote_name)
            sftpconn.get(remote_path, local_path_name)
            sftpconn.close()

            response = self.big_file_download(local_path_name, remote_name)

            if response:
                return response
            return JsonResponse({'status': 'HttpResponse'})

        except Exception as e:
            return e

    def file_iterator(self, file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def big_file_download(self, download_file_path, filename):
        try:
            response = StreamingHttpResponse(
                self.file_iterator(download_file_path))
            # 增加headers
            response['Content-Type'] = 'application/octet-stream'
            response['Access-Control-Expose-Headers'] = "Content-Disposition, Content-Type"
            response['Content-Disposition'] = "attachment; filename={}".format(
                escape_uri_path(filename))
            return response
        except Exception:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
