import datetime
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django_comments.views import comments

from .forms import ContactForm
from books.models import Book, Publisher, Author
from django.views.generic import TemplateView, ListView, View, RedirectView, CreateView
from django.shortcuts import get_object_or_404
import os.path
from reportlab.pdfgen import canvas
from django.contrib.messages.views import SuccessMessageMixin


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


def my_image(request):
    image_data = open(r"D:\pythonProjects\Django_Holovaty\mysite\templates\logo.png", errors='ignore').read()
    return HttpResponse(image_data, content_type="image/png")


def hello_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'
    p = canvas.Canvas(response)
    p.drawString(100, 100, 'Hello PDF')
    p.showPage()
    p.save()
    return response


def set_color_get(request):
    if "favorite_color" in request.GET:
        response = HttpResponse("Теперь ваш любимый цвет {}".format(request.GET["favorite_color"]))
        response.set_cookie("favorite_color", request.GET["favorite_color"])
        return response
    else:
        return HttpResponse("Вы не указали любимый цвет.")


def show_color(request):
    if "favorite_color" in request.COOKIES:
        return HttpResponse("Ваш любимый цвет {}".format(request.COOKIES["favorite_color"]))
    else:
        return HttpResponse("У вас нет любимого цвета.")


@csrf_exempt
def post_comment(request):
    if request.method != 'POST':
        raise Http404('Разрешены только POST-запросы')
    if "comment" not in request.POST:
        raise Http404('Отсутствует комментарий')
    if request.session.get('has_commented', False):
        return HttpResponse("Вы уже отправляли комментарий.")
    c = request.POST.get('comment')
    request.session['has_commented'] = True
    return HttpResponse('Спасибо за комментарий')


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse('Вы вошли в систему.')
        else:
            return HttpResponse("Включите поддержку cookies и попробуйте еще раз.")
    request.session.set_test_cookie()
    return HttpResponse('test_cookie установлен')


def user_is_auth(request):
    if request.user.is_authenticated:
        print(request.user)
        print(request.user.get_full_name())
        print(request.user.get_all_permissions())
        # print(request.user.email_user("Subject: View", "I am user_is_auth_view"))

        return HttpResponse('User is auth')
    else:
        return HttpResponse('Other user')


@csrf_exempt
def login_view2(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        # return HttpResponseRedirect('/account/loggedin')
        return HttpResponse('you are logged in')
    else:
        # return HttpResponseRedirect('/account/invalid')
        return HttpResponse('invalid username/password')


def logout_view(request):
    auth.logout(request)
    return HttpResponse('You are logged out')
    # return HttpResponseRedirect('/account/loggedout')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponse('user created')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form': form})


def Http_404(request):
    raise Http404
