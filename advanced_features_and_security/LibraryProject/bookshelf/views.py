from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.core.exceptions import PermissionDenied
from .forms import ExampleForm


def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        publication_date = request.POST['publication_date']
        isbn = request.POST['isbn']
        book = Book.objects.create(title=title, author=author, publication_date=publication_date, isbn=isbn)
        return redirect('book_list')
    return render(request, 'bookshelf/book_create.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.publication_date = request.POST['publication_date']
        book.isbn = request.POST['isbn']
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_update.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('book_list')
    
# This code provides views for listing, creating, updating, and deleting books in a Django application.