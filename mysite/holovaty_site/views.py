from django.http import HttpResponse, Http404
import datetime
from django.shortcuts import render
import sqlite3
import pyodbc
import MySQLdb
from django.db import connection


def my_homepage_view(request):
    return HttpResponse("HomePage")


def hello(request):
    return HttpResponse("Hello World")


def current_datetime(request):
    current_date = datetime.datetime.now()
    # print(locals())
    return render(request, "current_datetime.html", locals())


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    print(locals())
    return render(request, "hours_ahead.html", {"hour_offset": offset, "next_time": dt})


def sqlite3_connect(request):
    sqlite_connection = sqlite3.connect(":memory:")
    sqlite_connection.execute("CREATE TABLE lang(name, first_appeared)")
    data = [
        ("C++", 1985),
        ("Objective-C", 1984),
    ]
    sqlite_connection.executemany("INSERT INTO lang(name, first_appeared) VALUES(?, ?)", data)
    print("Success connect")
    cursor = sqlite_connection.cursor()
    sqlite_select_query = "SELECT * FROM lang"
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print(type(records))
    cursor.close()
    sqlite_connection.close()
    return render(request, "templ.html", {"records": records})


def mySQLdb_connect(request):
    cur = connection.cursor()
    select_query = "SELECT * FROM city"
    cur.execute(select_query)
    records = cur.fetchall()
    cur.close()
    return render(request, "templ.html", {"records": records})
