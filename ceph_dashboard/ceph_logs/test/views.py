# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django_redis import get_redis_connection


def index(rquest):
    conn = get_redis_connection("default")
    data = conn.smembers("ceph_host")
    for i in data:
        cc = eval(i.decode())
        if cc["host_name"] == "host0035":
            print(cc)
        
    return HttpResponse("zheshi")
