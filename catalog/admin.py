from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)



# Created this fucntion for inlines books for particular author (books having same author)
class BooksInline(admin.TabularInline):
    model = Book
    # By default this above class display the all books of particular author
    # "with extra blank placeholder to add more" to delete this add the following code
    extra = 0
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    pass

    # which field should display and with what order in "author field"
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    
    # which field should display and with what order "inside particular author" (displaying single author)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    # Displaying all the books having same author
    inlines = [BooksInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Created this fucntion for inlines book instances for particular book (book having same names etc)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    # By default this above class display the all instances of particular book
    # "with extra blank placeholder to add more" to delete this add the following code
    extra = 0

# Register the Admin classes for Book using the decorator
# "@admin.register(Book)" is same as "admin.site.register(Book, BookAdmin)"
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

    list_display = ('title', 'author', 'language', 'display_genre')

    # Displaying all the instances (book having same name) of this book with differnet id which is self generated during add bookinstance
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    pass

    list_display = ('book', 'status', 'borrower', 'due_back')

    # will create a filter desk for status and due_back, like 60%, 30%, < 30% for mark checking very usefull
    list_filter = ('status', 'due_back')

    # which field should display and with what order in "inside particular bookinstance" (displaying single bookinstance)
    # None if we don't what a name for the field
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'borrower', 'due_back')
        }),
    )




