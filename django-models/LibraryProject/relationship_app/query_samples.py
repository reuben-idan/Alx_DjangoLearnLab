from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
specific_author = Author.objects.get(name="George Orwell")
authors_books = Book.objects.filter(author=specific_author)
print("Books by George Orwell:", list(authors_books))

# List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
library_books = library.books.all()
print(f"Books in {library_name}:", list(library_books))

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(f"Librarian for {library_name}:", librarian.name) 