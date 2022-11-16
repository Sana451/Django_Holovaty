from django.urls import path, re_path
from holovaty_site.views import hello, my_homepage_view, current_datetime, hours_ahead, sqlite3_connect, \
    mySQLdb_connect, display_request_META
from books import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^time/$", current_datetime),
    re_path(r'^hello/$', hello),
    path(r"", my_homepage_view),  # re_path(r'^$', my_homepage_view),
    re_path(r"^time/plus/(\d{1,2})/$", hours_ahead),
    re_path(r"^time/$", current_datetime),
    re_path(r"sqlite", sqlite3_connect),
    re_path(r"mysql", mySQLdb_connect),
    re_path(r"display_request_meta", display_request_META),
    # re_path(r"^search-form/$", views.search_form),
    re_path(r"^search/$", views.search),
    re_path(r"^contact/$", views.contact),
    re_path(r"^contact/thanks/$", views.thanks),
]
