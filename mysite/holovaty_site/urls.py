from django.urls import path, re_path
from holovaty_site import views

urlpatterns = [
    re_path(r"^time/$", views.current_datetime),
    re_path(r'^hello/$', views.hello),
    re_path(r'^hello/(\w+)$', views.hello_name),
    path(r"", views.my_homepage_view),  # re_path(r'^$', my_homepage_view),
    re_path(r"^time/plus/$", views.hours_ahead),  # исп. значение offset по умолчанию (5), указано в view.hours_ahead
    re_path(r"^time/plus/(\d{1,2})/$", views.hours_ahead),  # re_path(r"^time/plus/(?P<offset>\d{1,2})/$", hours_ahead),
    re_path(r"^time/$", views.current_datetime),
    re_path(r"sqlite", views.sqlite3_connect),
    re_path(r"mysql", views.mySQLdb_connect),
    re_path(r"display_request_meta", views.display_request_META),
]
