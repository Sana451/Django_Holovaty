from django.urls import path, re_path
from holovaty_site.views import hello, my_homepage_view, current_datetime, hours_ahead, sqlite3_connect, mySQLdb_connect

urlpatterns = [
    re_path(r"^time/$", current_datetime),
    re_path(r'^hello/$', hello),
    # re_path(r'^$', my_homepage_view),
    path(r"", my_homepage_view),
    re_path(r"^time/plus/(\d{1,2})/$", hours_ahead),
    re_path(r"^time/$", current_datetime),
    re_path(r"sqlite", sqlite3_connect),
    re_path(r"mysql", mySQLdb_connect),
]
