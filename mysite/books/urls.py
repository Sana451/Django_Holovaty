from django.contrib.auth import login, logout

from django.urls import path, re_path, include
from .views import BooksListView, AboutPageView, PublisherListView, AboutView, BookCounterRedirectView, my_image, \
    hello_pdf, show_color, post_comment, set_color_get, login_view, user_is_auth, login_view2, logout_view, register, \
    Http_404

from books import views

urlpatterns = [
    # re_path(r"^search-form/$", views.search_form),
    re_path(r"^search/$", views.search),
    re_path(r"^contact/$", views.contact),
    re_path(r"^contact/thanks/$", views.thanks, {'template_name': 'thanks.html'}),
]

urlpatterns += [
    re_path(r"abo", AboutView.as_view(), name='abo'),
    re_path(r'^about/(?P<context_name>\w+)$', AboutPageView.as_view()),
    # re_path(r"^about/(\w+)/$", views.about_pages),
    re_path(r"^book_list/$", BooksListView.as_view()),
    re_path(r"^publishers/$", PublisherListView.as_view(), name='publishers'),
    re_path(r"qwe", BookCounterRedirectView.as_view())
]

urlpatterns += [
    re_path(r"my_image", my_image),
    re_path(r"hello_pdf", hello_pdf),
    re_path(r"set_color_get", set_color_get),
    re_path(r"show_color", show_color),
    re_path(r"post_comment", post_comment),
    re_path(r"^login_view$", login_view),
    re_path(r"user_is_auth", user_is_auth),
    re_path(r"^login_view2$", login_view2),
    re_path(r"^logout_view$", logout_view),
    re_path(r"^register_view$", register),
    re_path(r"^docs$", Http_404),
]



from django.contrib.auth.models import User