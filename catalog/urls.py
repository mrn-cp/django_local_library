from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.BookListView.as_view(), name='books'),
    #path('book/id', views.BookDetailView, name='book-detail'), # int = integer, pk = primary key
    # This below code same as above but the view function has a respose if the book does not exit
    re_path(r'^book/(\d+)$', views.BookDetailView, name='book-detail'),
    path('author/', views.AuthorListView.as_view(), name='author'),
    re_path(r'^author/(\d+)$', views.AuthorDetailView, name='author-detail'),

]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('borrowed/', views.LoanedBooksByLibrarianView.as_view(), name='borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

# Admin style configuration for Author
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

# Admin style configuration path for Book
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]