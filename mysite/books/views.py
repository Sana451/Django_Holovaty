import datetime

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
from books.models import Book, Publisher
from django.views.generic import TemplateView, ListView, View, RedirectView
from django.shortcuts import get_object_or_404


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Введите поисковый запрос.')
        elif len(q) > 20:
            errors.append('Введите не более 20 символов.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'search_results.html', {'books': books, 'query': q})
    return render(request, 'search_form.html', {'errors': errors})


# @csrf_exempt
# def contact(request):
#     errors = []
#     if request.method == 'POST':
#         if not request.POST.get('subject', ''):
#             errors.append('Введите тему.')
#         if not request.POST.get('message', ''):
#             errors.append('Введите сообщение.')
#         if request.POST.get('e-mail') and '@' not in request.POST['e-mail']:
#             errors.append('Введите правильный адрес e-mail')
#         if not errors:
#             send_mail(
#                 request.POST['subject'],
#                 request.POST['message'],
#                 request.POST.get('e-mail', 'sana451@mail.ru'),
#                 ['sana451@mail.ru'],
#                 fail_silently=False,
#             )
#             return HttpResponseRedirect('/contact/thanks/')
#     return render(request, 'contact_form.html', {
#         'errors': errors,
#         'subject': request.POST.get('subject', ''),
#         'message': request.POST.get('message', ''),
#         'email': request.POST.get('e-mail', ''),
#     }
#                   )


def thanks(request, template_name):
    return render(request, template_name)  # accepts template_name from urls.py (urlpatterns)


@csrf_exempt
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'sana451@mail.ru'),
                ['sana451@mail.ru'],
                fail_silently=False,
            )
            return HttpResponseRedirect('thanks/')
    else:
        form = ContactForm(
            initial={'subject': 'I like your site!', 'message': 'i am message'}
        )
    return render(request, 'contact_form.html', {'form': form})


class AboutView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('About us')


class AboutPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = datetime.date.today()
        context['context_name'] = context['context_name'].upper()
        return context


class BookCounterRedirectView(RedirectView):
    pattern_name = 'publishers'


class BooksListView(ListView):
    model = Book
    template_name = 'book_list.html'


class PublisherListView(ListView):
    model = Publisher
    template_name = 'publisher_list.html'
    context_object_name = "my_favorite_publishers"



