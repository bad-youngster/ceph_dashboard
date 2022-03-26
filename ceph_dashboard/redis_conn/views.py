# -*- coding: utf-8 -*-

from django_redis import get_redis_connection

def redisConn():
    redis_conn = get_redis_connection('default')
    return redis_conn