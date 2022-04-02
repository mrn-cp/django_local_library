from dataclasses import field, fields
from gettext import Catalog
from pyexpat import model
from sre_constants import SUCCESS
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre, Language

def index(request):
    """View function for home page of site."""
    # for sessions (just like cokeis, keep trap of users previous visits activity)
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Genre available
    num_genre = Genre.objects.count()

    # Book counts by Genres
    num_jewishlit = Book.objects.filter(genre__name__icontains='Jewish Literature').count()
    num_fiction = Book.objects.filter(genre__name__icontains='Fiction').count()
    num_persionaln_arrative = Book.objects.filter(genre__name__icontains='Persional Narrative').count()
    num_drama = Book.objects.filter(genre__name__icontains='Drama').count()
    num_autobiography = Book.objects.filter(genre__name__icontains='Autobiography').count()
    num_biography = Book.objects.filter(genre__name__icontains='Biography').count()
    num_Selfhelp = Book.objects.filter(genre__name__icontains='Self-help').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_jewishlit': num_jewishlit,
        'num_fiction': num_fiction,
        'num_persionaln_arrative': num_persionaln_arrative,
        'num_drama': num_drama,
        'num_autobiography': num_autobiography,
        'num_biography': num_biography,
        'num_Selfhelp': num_Selfhelp,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Class based view
from django.views import View, generic

class BookListView(generic.ListView):
    model = Book 
    paginate_by = 10  

#class BookDetailView(generic.DetailView):
    #model = Book

# This function same as above but has as return value if the book does not exit

def BookDetailView(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'catalog/book_detail.html', context={'book': book})

# Author View
class AuthorListView(generic.ListView):
    model = Author 
    paginate_by = 10  

def AuthorDetailView(request, primary_key):
    try:
        author = Author.objects.get(pk=primary_key)
        book = Book.objects.filter(author__id = primary_key)
    except Author.DoesNotExist:
        raise Http404('Author does not exist')

    return render(request, 'catalog/author_detail.html', context={'author': author, 'book': book})

# boo list by user ordered/loanded 
# "mixin" for put restriction over this site (only login user able to see their loaned books )
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# borrowed book list for librarian
# "mixin" for put restriction over this site (only login librarian able to see loaned books )
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
class LoanedBooksByLibrarianView(LoginRequiredMixin, generic.ListView):
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/borrowed_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')



# renew for book by librarian
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            #book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        #form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        form = RenewBookForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


#-----------------------------
#Admin style views (where we can create, update, delete)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# for Author

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author')



# for Book

from catalog.models import Book

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdate(UpdateView):
    model = Book
    #fields = '__all__'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
