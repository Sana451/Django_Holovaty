from django.http import HttpResponse
from django.shortcuts import render

from books.models import Book


def search_form(request):
    return render(request, 'search_form.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)
        return render(request, 'search_results.html', {'books': books, 'query': q})
    else:
        return render(request, 'search_form.html', {'error': True})
