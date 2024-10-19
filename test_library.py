## Import libraries
import pandas as pd
from digital_library import Book, Library

## Read in data (this code reads data directly from GitHub)
url = 'https://github.com/esnt/Data/raw/main/CleanData/library_books.csv'
data = pd.read_csv(url)

book = Book('1310', 'NewBook', 'NewAuthor', 'Mystery', 270, 2010)
library = Library(data)

def test_book_get_age():
    return (book.get_age() == 14)


def test_book_is_long():
    return (book.is_long() == False)


def test_book_summary():
    return (book.summary() == 'Book ID 1310: NewBook by NewAuthor has 270 pages. It was first published in 2010 and belongs to the Mystery genre.')


def test_library():
    print(f"Number of books: {library.size}")
    print(f"Number of unique authors: {library.authors}\n")


def test_summary():
    print(library.get_book_summary(1285))


def test_add_book():
    library.add_book(book)
    if book.book_id in library.data['book_id'].values:
        print(f"{book} has been added to the library. Library now has {library.size} books and {library.authors} unique authors.\n")
    else:
        print(f"add_book failed: lib size {library.size}")


def test_remove_book():
    library.remove_book(book.book_id)
    if book.book_id not in library.data['book_id'].values:
        print(f"{book} has been removed from the library. Library now has {library.size} books and {library.authors} unique authors.\n")
    else:
        print(f"remove_book failed: lib size {library.size}")


def test_get_books_by_author():
    auth = library.get_books_by_author("Shel Silverstein")
    if type(auth) == str:
        print(auth)
    elif type(auth) == pd.DataFrame:
        print(".get_books_by_author worked")
        print(auth)
    else:
        print("Error with get_books_by_author")

    
def test_get_genre_count():
    gen = library.get_genre_count()
    return type(gen) == pd.Series


def test_get_book_summary():
    summ = library.get_book_summary(1285)
    expected = 'Book ID 1285: Blue Fire by Janice Hardy has 373 pages. It was first published in 2010 and belongs to the Fantasy genre.'
    return summ == expected


def test_str():
    print(library)



if __name__ == "__main__":
    test_add_book()
    test_get_books_by_author()
    test_library()
    test_remove_book()
    test_str()
    test_summary()
