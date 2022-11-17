from django.urls import path, re_path
from .views import BooksListView, AboutPageView, PublisherListView, AboutView, BookCounterRedirectView

from books import views

urlpatterns = [
    # re_path(r"^search-form/$", views.search_form),
    re_path(r"^search/$", views.search),
    re_path(r"^contact/$", views.contact),
    re_path(r"^contact/thanks/$", views.thanks, {'template_name': 'thanks.html'}),
]

urlpatterns += [
    re_path(r'^about/(?P<context_name>\w+)$', AboutPageView.as_view()),
    re_path(r"abo", AboutView.as_view(), name='abo'),
    # re_path(r"^about/(\w+)/$", views.about_pages),
    re_path(r"^book_list/$", BooksListView.as_view()),
    re_path(r"^publishers/$", PublisherListView.as_view(), name='publishers'),
    re_path(r"qwe", BookCounterRedirectView.as_view())
]
