# -*- coding: utf-8 -*-

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class cephLogin(APIView):

    def post(self, request):
        conn = get_redis_connection('default')
        # 获取密码
        redisPass = (conn.get('admin')).decode("utf-8")
        requestUser = request.data["user"]
        requestPass = request.data["pass"]
        redisUser = "admin"
        if requestUser == redisUser and requestPass == redisPass:

            return Response({"status": status.HTTP_200_OK, "message": "登录成功"})
        else:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "用户名或密码不正确"})
