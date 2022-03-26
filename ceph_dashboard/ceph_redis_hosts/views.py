# -*- coding: utf-8 -*-
import json
from django_redis import get_redis_connection
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from ceph_dashboard.redis_conn.views import redisConn

class redisHosts(APIView):
    def post(self, request, format=None):
        # 链接redis
        conn = get_redis_connection('default')
        hostname = str(request.data["hostname"])
        hostaddr = str(request.data["hostaddr"])
        conn.set(hostname,hostaddr)    
        return HttpResponse("ok")


class redis_host(APIView):

    def post(self,reques,format=None):
        '''
            手动录入信息填充到redis
        '''
        # redis list lpush
        xx = reques.body
        print(xx)
        conn = redisConn()
        conn.sismember('ceph_host',xx)
        conn.sadd('ceph_host',xx)
        return HttpResponse("post")
    
    def get(self,reques,format=None):
        '''
            获取现存的redis中数据
        '''
        # 测试获取redis中的数据
        conn = redisConn()
        data = conn.smembers("ceph_host")
        new_data = []
        for i in data:
            new_data.append(eval(i.decode()))
        return Response(new_data)