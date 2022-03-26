# -*- coding: utf-8 -*-
from unicodedata import name
from django.urls.conf import path
from ceph_dashboard.ceph_auth.auth_controller import AuthCeph
from ceph_dashboard.ceph_host import views as host_views
from ceph_dashboard.ceph_cluster import views as cluster_views
from ceph_dashboard.ceph_pools import views as pools_views
from ceph_dashboard.ceph_logs import views as logs_views
from ceph_dashboard.ceph_redis_hosts import views as redis_hosts_views
from ceph_dashboard.ceph_osds_crush import views as osds_views
from ceph_dashboard.ceph_errors_pgs import views as pgs_views
from ceph_dashboard.ceph_logs.test import views as test_views
from ceph_dashboard.ceph_web_login import views as login_views
urlpatterns = [
    path('authceph/', AuthCeph.as_view(), name="auth ceph models"),
    path('ceph_host/', host_views.ceph_host.as_view(), name="ceph host"),
    path('ceph_health/', cluster_views.ceph_healths.as_view(), name="ceph health"),
    path('ceph_pools/', pools_views.ceph_pools.as_view(), name="ceph pools"),
    path('ceph_logs/', logs_views.ceph_logs.as_view(), name="ceph logs path"),
    path('ceph_download_logs/', logs_views.filedownload.as_view(),
         name="ceph download logs"),
    path('ceph_hosts/', redis_hosts_views.redisHosts.as_view(), name="redis hosts"),
    path('ceph_redis_hosts/',redis_hosts_views.redis_host.as_view(), name='list redis hosts'),
    path('osds_crush/', osds_views.osdCrush.as_view(), name='osds crush'),
    path('ceph_pgs_errors/', pgs_views.pgsErrors.as_view(), name="ceph pgs errors"),
    path('ceph_web_login/', login_views.cephLogin.as_view(), name="ceph web login"),
    path('test/', test_views.index, name="test index")
]
